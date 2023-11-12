from typing import List
import openai
from src.config import settings
from . import schemas as chat_schemas,models as chat_models

print(settings.ChatGPT_API_KEY ,"salamd")

openai.api_key = settings.ChatGPT_API_KEY





class IAI_IFS_Conselor:
    @classmethod
    def get_AI_settings(cls) -> chat_schemas.AISettings:
        pass
    def get_AI_consultancy(self,prior_messages: List[chat_models.InteractionMessage]) -> chat_schemas.InteractionMessage:
        pass

def get_AI_conselor() -> IAI_IFS_Conselor:
    return ChatgptIFSConselor()

class ChatgptIFSConselor(IAI_IFS_Conselor):

    @classmethod
    def get_AI_settings(cls) -> chat_schemas.AISettings:
        return chat_schemas.AISettings( **{
                "model_name": "GPT4",
                "role": "System",
                "prompt": cls.get_system_prompt()
                })

    @classmethod
    def get_system_prompt(cls) -> str:
        return "As a helpful IFS therapist chatbot, your role is to guide users through a simulated IFS session in a safe and supportive manner with a few changes to the exact steps of the IFS model."


    def get_AI_consultancy(self,prior_messages: List[chat_schemas.InteractionMessage]) -> chat_schemas.InteractionMessage :
        if not prior_messages:
            return None
        messages = [ {"role": "system", "content": self.get_system_prompt()} ]
        for message in prior_messages:
            if message: 
                messages.append( 
                    {"role": message.role, "content": message.content}, 
                ) 
        try:
            chat = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo", messages=messages 
            ) 
            
            reply = chat.choices[0].message.content 
        except:
            reply  = "I am currently go out of token!"
        return chat_schemas.InteractionMessage(content=reply,intraction_id=prior_messages[0].intraction_id,role=chat_models.IntractionRoleEnum.AI)