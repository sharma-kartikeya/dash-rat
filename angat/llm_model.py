import requests
from typing import List, Any, Optional, Union
from transformers import pipeline
from .db_helper import DB_Helper
from .models.Message import Message, ROLE_TYPE
from .models.Chat import Chat
from .prompts.system_prompts import system_prompt
# Load model directly
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat_model import ChatModel
from dotenv import load_dotenv
import os

load_dotenv()

class LLM_Model:
    API_URL = 'https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407/v1/chat/completions'
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    model_name = 'mistralai/Mistral-Nemo-Instruct-2407'

    @classmethod
    def llm_call(self, chat_id: str, query: str):
        query_result = DB_Helper.query(query=query)
        contexts = [result[0] for result in list(query_result)]
        joined_context = "\n".join(contexts)
        current_chat = Chat.objects.get(id=chat_id)
        Message(chat=current_chat, role_type=ROLE_TYPE.USER, msg=query, context=joined_context).save()
        messages = DB_Helper.get_chat_messages(chat_id)
        payload = {
            "messages": messages,
            'max_tokens': 1000,
            'stream': False
        }
        response = requests.post(url=self.API_URL, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
        else:
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
            Message(chat=current_chat, role_type=ROLE_TYPE.ASSISTANT, msg=response_text).save()
            return response_json
        
class LocalLLM:
    API_URL = 'https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407/v1/chat/completions'
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    @classmethod
    def call(self) -> Any:
        messages = [ {"role": 'system', "content": system_prompt}]

        payload = {
            "messages": messages,
            'max_tokens': 10000,
            'stream': False
        }
        
        response = requests.post(url=self.API_URL, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
        else:
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
            return response_json

class OpenAiChat:
    def __init__(self, model: Union[str, ChatModel], system_prompt: Optional[str]) -> None:
        self.openai_client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        self.model = model
        self.messages: List[ChatCompletionMessageParam] = []
        self.chat_started: bool = False
        if system_prompt:
            self.messages.append({
                'role': 'system',
                'content': system_prompt
            })

    def cold_start(self, force: bool) -> None:
        if self.chat_started and not force:
            print("Chat already started!")
        else:
            self.messages = [self.messages[0]]
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            self.messages.append({
                'role': 'assistant',
                'content': response.choices[0].message.content
            })
            self.chat_started = True


    def user_message(self, user_message: str) -> None:
        self.messages.append({
            'role': 'user',
            'content': user_message
        })
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        self.messages.append({
            'role': 'assistant',
            'content': response.choices[0].message.content
        })
        if not self.chat_started:
            self.chat_started = True


openAiChat = OpenAiChat(model='gpt-3.5-turbo', system_prompt=system_prompt)

class ProgramGraphAgent:
    def __init__(self, system_prompt: str, model: Union[str, ChatModel]) -> None:
        self.openai_client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        self.model = model
        self.messages: List[ChatCompletionMessageParam] = []
        self.chat_started: bool = False
        if system_prompt:
            self.messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
    