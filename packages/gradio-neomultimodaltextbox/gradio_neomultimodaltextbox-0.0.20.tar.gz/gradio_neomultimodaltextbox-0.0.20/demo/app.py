import time  # Pour tester les temps de chargement
import hmac
import hashlib
import base64
import os

import gradio as gr
from gradio_neomultimodaltextbox import NeoMultimodalTextbox
from rtmt_configuration import rtmt

example = NeoMultimodalTextbox().example_value()

def identity(i):
    return i

def generate_turn_credentials(shared_secret: str, ttl: int=3600):
    # Génère un username basé sur l'heure actuelle (en secondes) + TTL
    username = str(int(time.time()) + ttl)
    
    # Génère le password en utilisant HMAC-SHA1
    password = hmac.new(
        shared_secret.encode('utf-8'),  # Clé secrète
        username.encode('utf-8'),      # Message (username)
        hashlib.sha1                   # Algorithme HMAC-SHA1
    ).digest()
    
    # Encode le résultat en Base64
    password = base64.b64encode(password).decode('utf-8')
    
    return username, password


# Exemple d'utilisation
shared_secret = "my shared secret with spaces"  # Exemple de clé secrète
username, password = generate_turn_credentials(shared_secret)

rtc_configuration = {
    "iceServers": [
        {
            "urls": ["turn:turn.neo-onepoint.ai:5349"],
            "username": username,
            "credential": password
        },
    ],
    "iceTransportPolicy": "relay",   
}

with gr.Blocks() as demo:

    conversation = gr.Chatbot(
        type="messages",
    )
    box1 = NeoMultimodalTextbox(
        file_count="multiple",
        value={"text": "zouzou", "files": [], "audio": ""},
        interactive=True,
        audio_btn=True,
        mode="send-receive",
        modality="audio",
        rtmt=rtmt,
        rtc_configuration=rtc_configuration
    )  # interactive version of your component
    box2 = NeoMultimodalTextbox(
        upload_btn=False, interactive=False, stop_btn=True
    )  # static version of your component

    box1.submit(fn=identity, inputs=box1, outputs=box2)

    box1.start_recording(
        fn=lambda: gr.update(audio_btn=False, stop_audio_btn=True, submit_btn=False),
        outputs=[box1],
    )
    box1.stop_recording(
        fn=lambda: gr.update(audio_btn=True, stop_audio_btn=False, submit_btn=True),
        outputs=[box1],
    )

    box1.stream(
        inputs=[box1], 
        outputs=[box1]
    )

    box1.on_additional_outputs(
        fn=identity,
        outputs=[conversation]
    )


if __name__ == "__main__":
    demo.launch()
