import asyncio
import json
import logging
from enum import Enum
from typing import Any, Callable, Optional, cast, Protocol, Literal
import base64
import av
import aiohttp
import numpy as np
import re

from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from aiortc import MediaStreamTrack
from aiortc.contrib.media import AudioFrame
from aiortc.mediastreams import MediaStreamError
from fastapi import WebSocket

logger = logging.getLogger("voicerag")

AUDIO_PTIME = 0.02


class ToolResultDirection(Enum):
    TO_SERVER = 1
    TO_CLIENT = 2


class ToolResult:
    text: str
    destination: ToolResultDirection

    def __init__(self, text: str, destination: ToolResultDirection):
        self.text = text
        self.destination = destination

    def to_text(self) -> str:
        if self.text is None:
            return ""
        return self.text if type(self.text) == str else json.dumps(self.text)


class AdditionalOutputs:
    def __init__(self, *args) -> None:
        self.args = args


class DataChannel(Protocol):
    def send(self, message: str) -> None: ...


class Tool:
    target: Callable[..., ToolResult]
    schema: Any

    def __init__(self, target: Any, schema: Any):
        async def async_target(args):
            result = await target.ainvoke(args)
            return ToolResult(result, ToolResultDirection.TO_SERVER)
        self.target = async_target
        self.schema = schema


class RTToolCall:
    tool_call_id: str
    previous_id: str

    def __init__(self, tool_call_id: str, previous_id: str):
        self.tool_call_id = tool_call_id
        self.previous_id = previous_id


class Message:
    id: str
    role: Literal["input", "output", "function_call", "function_call_output"]

    def __init__(self, id, role):
        self.id = id
        self.role = role


class RTMiddleTier:
    endpoint: str
    deployment: str
    key: Optional[str] = None
    
    tools: dict[str, Tool] = {}
    model: Optional[str] = None
    system_message: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    disable_audio: Optional[bool] = None
    voice_choice: Optional[str] = None
    api_version: str = "2024-10-01-preview"
    _tools_pending = {}
    _token_provider = None

    def __init__(
            self,
            endpoint: str,
            deployment: str,
            credentials: AzureKeyCredential | DefaultAzureCredential,
            voice_choice: Optional[str] = None,
            expected_layout: Literal["mono", "stereo"] = "mono",
            model_sample_rate: int = 24000,
            input_output_sample_rate: int = 48000,
            username: str = "anonymous@groupeonepoint.com",
            turn_detection: Optional[dict[str, Any]] = None,
            transcription_params: Optional[dict[str, Any]] = None,
            input_audio_noise_reduction: Optional[str] = None,
            stop_words: Optional[list[str]] = None,
        ):
        self.username = username
        self.endpoint = endpoint
        self.deployment = deployment
        self.voice_choice = voice_choice
        self.pts = 0
        self.item_list = []  # Utile pour conserver l'ordre des échanges
        self.message_history = {}  # Conserve les messages à partir des Ids
        self.message_completed = {} # Détermine si un message a été complété à partir des Ids
        if voice_choice is not None:
            logger.info("Realtime voice choice set to %s", voice_choice)
        if isinstance(credentials, AzureKeyCredential):
            self.key = credentials.key
        else:
            self._token_provider = get_bearer_token_provider(credentials, "https://cognitiveservices.azure.com/.default")
            self._token_provider()
        self.expected_layout = expected_layout
        self.model_sample_rate = model_sample_rate
        self.input_output_sample_rate = input_output_sample_rate
        if turn_detection and isinstance(turn_detection, dict):
            self.turn_detection = turn_detection
        else:
            # Default turn detection parameters
            # You can adjust these parameters based on your requirements
            # Options: "server_vad", "semantic_vad", "none"
            self.turn_detection = {
                "type": "server_vad",
                "silence_duration_ms": 600,
                "threshold": 0.6,
            }
        if transcription_params and isinstance(transcription_params, dict):
            self.transcription_params = transcription_params
        else:
            # Default transcription parameters
            # You can adjust these parameters based on your requirements
            # For example, you might want to change the model or add other parameters
            # models : "gpt-4o-transcribe", "gpt-4o-mini-transcribe", "whisper-1"
            self.transcription_params = {
                "model": "whisper-1",
            }
        # Noise reduction for input audio
        # Options: "none", "near_field", "far_field"
        self.input_audio_noise_reduction = input_audio_noise_reduction
        self.stop_words = stop_words

    async def update_session(self, msg: str, target_ws: WebSocket) -> None:
        message = json.loads(msg)
        if message is not None:
            match message["type"]:
                case "session.created":
                    # Créer la commande
                    message = {
                        "type": "session.update",
                        "session": {
                            "turn_detection": self.turn_detection,
                            "input_audio_transcription": self.transcription_params,
                        }
                    }
                    session = message["session"]
                    if self.input_audio_noise_reduction is not None:
                        session["input_audio_noise_reduction"] = self.input_audio_noise_reduction
                    if self.system_message is not None:
                        session["instructions"] = self.system_message
                    if self.temperature is not None:
                        session["temperature"] = self.temperature
                    if self.max_tokens is not None:
                        session["max_response_output_tokens"] = self.max_tokens
                    if self.disable_audio is not None:
                        session["disable_audio"] = self.disable_audio
                    if self.voice_choice is not None:
                        session["voice"] = self.voice_choice
                    session["tool_choice"] = "auto" if len(self.tools) > 0 else "none"
                    session["tools"] = [tool.schema for tool in self.tools.values()]
                    updated_message = json.dumps(message)
                    await target_ws.send_str(updated_message)

    async def _forward_messages(
            self,
            mediastreamtrack: MediaStreamTrack,
            thread_quit: asyncio.Event,
            queue: asyncio.Queue,
            channel: Callable[[], DataChannel | None] | None,
            set_additional_outputs: Callable | None,
        ) -> None:

        # _resampler from the input frequency to the model frequency 
        _resampler = av.AudioResampler(  # type: ignore
            format="s16",
            layout=self.expected_layout,
            rate=self.model_sample_rate,
        )
        # _resampler_back from the model frequency to the output frequency 
        _resampler_back = av.AudioResampler(
            format="s16",
            layout="mono",
            rate=self.model_sample_rate,
            frame_size=int(self.model_sample_rate * AUDIO_PTIME),
        )

        async with aiohttp.ClientSession(base_url=self.endpoint) as session:
            params = {"api-version": self.api_version, "deployment": self.deployment}
            headers = {}
            if self.username:
                headers["x-ms-client-request-id"] = self.username
            if self.key is not None:
                headers["api-key"] = self.key
            else:
                headers["Authorization"] = f"Bearer {await self._token_provider()}"
            
            async with session.ws_connect("/openai/realtime", headers=headers, params=params) as target_ws:

                async def from_client_to_server():
                    # Assumes you have a method to get audio data from the MediaStreamTrack
                    async for audio_data in self._get_audio_data(mediastreamtrack, thread_quit):
                        new_msg = await self._process_audio_to_server(audio_data, _resampler)
                        if new_msg is not None:
                            await target_ws.send_str(new_msg)

                    if target_ws:
                        print("Closing OpenAI's realtime socket connection.")
                        await target_ws.close()
                        
                async def from_server_to_client():
                    async for msg in target_ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            asyncio.create_task(self._process_audio_from_server( 
                                msg=msg.data,
                                queue=queue,
                                channel=channel,
                                set_additional_outputs=set_additional_outputs,
                                _resampler_back=_resampler_back,
                                target_ws=target_ws,
                            ))
                            if "session.created" in msg.data:
                                await self.update_session(msg.data, target_ws)
                        else:
                            print("Error: unexpected message type:", msg.type)

                try:
                    await asyncio.gather(from_client_to_server(), from_server_to_client())
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                finally:
                    # Assure-toi que les ressources sont libérées correctement
                    if target_ws:
                        await target_ws.close()
                    print("Cleaned up resources.")

    async def _get_audio_data(self, mediastreamtrack: MediaStreamTrack, thread_quit: asyncio.Event):
        """"""
        while not thread_quit.is_set():
            try:
                frame = await mediastreamtrack.recv()
                yield frame

            except MediaStreamError:
                logger.debug("MediaStreamError in process_input_frames")
                break

    async def _process_audio_to_server(self, audio_data: AudioFrame, _resampler: av.AudioResampler) -> Optional[bytes]:
        # Simule le traitement des données audio en ajoutant des métadonnées de session
        # Convertir les paramètres de session en un format approprié pour l'envoi
        new_message = {"type": "input_audio_buffer.append"}

        # Convertir le frame en nd_array
        nd_array = _resampler.resample(audio_data)[0].to_ndarray()
        # Convertis le tableau numpy en bytes
        buffer = nd_array.tobytes()
        # Encoder en Base64
        base64_encoded  = base64.b64encode(buffer).decode('utf-8')
        new_message["audio"] = base64_encoded
        new_message_json = json.dumps(new_message)

        return new_message_json

    async def _process_audio_from_server(
            self,
            msg: str,
            queue: asyncio.Queue,
            channel: Callable[[], DataChannel | None] | None,
            set_additional_outputs: Callable | None,
            _resampler_back: av.AudioResampler,
            target_ws: WebSocket,
        ):
        # Process the audio data received from the server

        message = json.loads(msg)

        # if "delta" not in message["type"]:
        #     print()
        #     print("~~" * 10)
        #     print()
        #     print(message['type'])
        #     print(message)

        match message["type"]:

            case "response.audio.delta":
                # The output sound answer added
                if self.actual_response != message['item_id']:
                    # On est déjà passé à un échange ultérieur
                    # Le son ne nous intéresse donc pas
                    return 
                
                audio_frame = await self.regenerate_audio_frame(message)
                # resample audioframe to make them readable for the client
                for audio_frames_processed in _resampler_back.resample(audio_frame):
                    await queue.put(audio_frames_processed)

            case "response.audio_transcript.done":
                if self.actual_response != message['item_id']:
                    # On est déjà passé à un échange ultérieur
                    # Le son ne nous intéresse donc pas
                    return 

                # Création d'un 'item', cad un input où output
                item = Message(message['item_id'], role="assistant")

                # On l'ajoute à la liste des messages pour conserver l'ordre d'interaction
                self.item_list.append(item)
                # The output complete response
                self.message_history[message["item_id"]] = message["transcript"]
                self.message_completed[message["item_id"]] = True
                set_additional_outputs(self.format_additional_outputs())
                cast(DataChannel, channel()).send("change")

            case "conversation.item.input_audio_transcription.completed":
                #The input transcript of our audio
                self.message_history[message["item_id"]] = message["transcript"]
                self.message_completed[message["item_id"]] = True
                set_additional_outputs(self.format_additional_outputs())
                cast(DataChannel, channel()).send("change")
                text = message["transcript"].lower().strip().replace('é', 'e').replace('è', 'e').replace('.', '').replace(',', '')
                for stop_word in self.stop_words:
                    if stop_word in text:
                        print(f"Stop word found in response: {stop_word}")
                        await target_ws.send_json({
                            "type": "response.create"
                        })

            case "input_audio_buffer.speech_started":
                # Une nouvelle question commence à être posé
                self.actual_response = None
                # Vide la queue afin de laisser la place aux nouvelles frames audio. 
                while not queue.empty():
                    try:
                        item = queue.get_nowait()
                        # Traite l'item si nécessaire
                    except asyncio.QueueEmpty:
                        break

            case "response.output_item.added":
                # Une nouvelle réponse est créée
                self.actual_response = message['item']['id']
                # Vide la queue afin de laisser la place aux nouvelles frames audio. 
                while not queue.empty():
                    try:
                        item = queue.get_nowait()
                        # Traite l'item si nécessaire
                    except asyncio.QueueEmpty:
                        break

            case "conversation.item.created":
                if "item" in message and message["item"]["type"] == "function_call":
                    item_call = message["item"]
                    if item_call["call_id"] not in self._tools_pending:
                        self._tools_pending[item_call["call_id"]] = RTToolCall(item_call["call_id"], message["previous_item_id"])
                    # updated_message = None

                elif "item" in message and message["item"]["type"] == "function_call_output":
                    # updated_message = None
                    self._tools_pending.pop(message["item"]["call_id"])
                    if len(self._tools_pending) == 0:
                        # self._tools_pending.clear()
                        await target_ws.send_json({
                            "type": "response.create"
                        })
                    return
                
                role = message["item"].get('role', 'function_call')
                if role != "user":
                    return
                # Création d'un 'item', cad un input où output
                item = Message(message['item']['id'], "user")
                # On crée une instance vide de l'échange afin de la remplir a postériori
                self.message_history[message["item"]['id']] = ""
                self.message_completed[message["item"]['id']] = False

                # On l'ajoute à la liste des messages pour conserver l'ordre d'interaction
                self.item_list.append(item)

            case "response.function_call_arguments.delta":
                # updated_message = None
                pass

            case "response.function_call_arguments.done":
                # updated_message = None
                # Création d'un 'item', cad un input où output
                item = Message(message['item_id'], "function_call")

                # On l'ajoute à la liste des messages pour conserver l'ordre d'interaction
                self.item_list.append(item)

                self.message_history[message["item_id"]] = {
                    "name": message["name"],
                    "args": message['arguments']
                }
                self.message_completed[message["item_id"]] = True

                if self.message_completed[self.item_list[-2].id]:
                    # On ne déclenche l'event de change que si l'input a déjà été transcript
                    set_additional_outputs(self.format_additional_outputs())
                    cast(DataChannel, channel()).send("change")
                # On ajoute l'output 
                item = Message(message['item_id'] + "_output", "function_call_output")
                self.message_history[message["item_id"] + "_output"] = ""
                self.message_completed[message["item_id"] + "_output"] = False
                self.item_list.append(item)

            case "response.output_item.done":
                if "item" in message and message["item"]["type"] == "function_call":
                    item = message["item"]
                    tool = self.tools[item["name"]]
                    args = item["arguments"]
                    result = await tool.target(json.loads(args))
                    self.message_history[message["item"]["id"] + "_output"] = {"name": item["name"], "output": result.to_text()}
                    self.message_completed[message["item"]["id"] + "_output"] = True
                    set_additional_outputs(self.format_additional_outputs())
                    cast(DataChannel, channel()).send("change")
                    await target_ws.send_json({
                        "type": "conversation.item.create",
                        "item": {
                            "type": "function_call_output",
                            "call_id": item["call_id"],
                            "output": result.to_text() if result.destination == ToolResultDirection.TO_SERVER else ""
                        }
                    })

        return 

    async def regenerate_audio_frame(self, message):
        """Crée les audios frames à partir du message textuel renvoyé de la WS"""
        base64_encoded = message.get("delta")
        # Décoder la chaîne Base64 en bytes
        decoded_buffer = base64.b64decode(base64_encoded)

        # Convertir les bytes en un tableau NumPy
        nd_array = np.frombuffer(decoded_buffer, dtype=np.int16)  # Assure-toi que le dtype correspond à ton audio original

        # Recréer l'AudioFrame à partir du tableau NumPy
        nd_array_reshaped = nd_array.reshape(1, -1)  # Ajoute une dimension pour l'audio mono

        audio_frame = av.AudioFrame.from_ndarray(
            nd_array_reshaped, format='s16', layout='mono'
        )  # Ajuste le format et le layout
        audio_frame.sample_rate = self.model_sample_rate
        audio_frame.pts = self.pts
        self.pts += audio_frame.samples
        return audio_frame

    def format_additional_outputs(self):
        conversation = []
        last_role = None
        for message in self.item_list:
            try:
                if last_role != message.role:
                    conversation.append({"role": message.role, "content": self.message_history[message.id], "completed": self.message_completed[message.id]})
                    last_role = message.role
                else:
                    conversation[-1]['content'] = conversation[-1]['content'] + self.message_history[message.id]
            except Exception as e:
                logger.info(e)
                pass
        return AdditionalOutputs(conversation)
