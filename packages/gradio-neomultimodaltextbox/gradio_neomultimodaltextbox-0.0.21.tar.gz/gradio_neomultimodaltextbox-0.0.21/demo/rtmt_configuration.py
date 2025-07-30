import logging

from azure.core.credentials import AzureKeyCredential
from gradio_neomultimodaltextbox import RTMiddleTier
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice_assistant")
from datetime import datetime

llm_credential = AzureKeyCredential("bae463d896c043689d18f97875c588ac")

# Example of _search_tool_schema_for_internet
# _search_tool_schema = {
#     "type": "function",
#     "name": "search",
#     "description": "Search the knowledge on internet.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "query": {
#                 "type": "string",
#                 "description": "Search query"
#             }
#         },
#         "required": ["query"],
#         "additionalProperties": False
#     }
# }

# rtmt = RTMiddleTier(
#     credentials=llm_credential,
#     endpoint="https://neo-conversation-sweden-azopenai-dev.openai.azure.com/",
#     deployment="gpt-4o-realtime-preview",
#     voice_choice="shimmer"
#     )


# # Obtenir la date actuelle
# date_actuelle = datetime.now()

# rtmt.system_message =   "You are a helpful assistant named Neo. " + \
#                         "The user is listening to answers with audio, so it's *super* important that answers are as short as possible, a single sentence if at all possible. " + \
#                         "Never read file names or source names or keys out loud. " + \
#                         f"The actual date is {date_actuelle.strftime('%d %B %Y')}. " + \
#                         "Produce an answer that's as short as possible. If the answer isn't in the knowledge base, say you don't know."

#                         # "We are actually in 2024. If someone asks for informations after 2023, use the 'search' tool to get the knowledge" + \
#                         # "Always use the following step-by-step instructions to respond: \n" + \
#                         # "1. Always use the 'search' tool to check the knowledge that is recent \n" + \
#                         # "2. When you have to use a tool, always say which tool you are using before using it and then that you give me the response when you recieve it from the tool\n" + \
#                         # "3. Produce an answer that's as short as possible"


rtmt = RTMiddleTier(
    credentials=llm_credential,
    endpoint="https://neo-models-sweden-azopenai-dev.openai.azure.com/",
    deployment="gpt-4o-realtime-preview",
    voice_choice="shimmer",
    turn_detection={
        "type": "semantic_vad",
        "create_response": False,
    },
    stop_words = [
        "ok neo", "okay neo"
    ]
)

# Obtenir la date actuelle
date_actuelle = datetime.now()

system_message = (
    "You are a helpful assistant named Neo, créé par l'AI Office de Onepoint."
    + "Ton rôle est de repeter ce que l'utilisateur dit, mais en le traduisant TOUJOURS en français. Ne fait que repeter ce que l'utilisateur dit, sans ajouter de contenu."
)
