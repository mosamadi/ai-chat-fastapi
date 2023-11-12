from typing import List
from datetime import datetime
from fastapi import HTTPException,status
from pydantic import BaseModel,ConfigDict,validator
from .models import IntractionRoleEnum
from ..auth.services import get_auth_user
from ..auth.models import UserModel

class InteractionBaseModel(BaseModel):
    name: str


class InteractionCreationModel(InteractionBaseModel):
    user_id: int
    

class InteractionResponseModel(InteractionBaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    

class BaseInteractionMessage(BaseModel):
    intraction_id : int
    content : str
    created_at : datetime = datetime.utcnow()

class InteractionMessage(BaseInteractionMessage):
    role : IntractionRoleEnum = IntractionRoleEnum.HUMAN

class AISettings(BaseModel):
    model_name: str 
    role: IntractionRoleEnum = IntractionRoleEnum.SYSTEM
    prompt: str 

class IntractionMessageReponseModel(InteractionMessage):
    model_config = ConfigDict(from_attributes=True)
    id:int
    



class IntractionMessageListsData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    messages: List[IntractionMessageReponseModel]
    settings : AISettings

class IntractionMessageListResponses(BaseModel):
    data : IntractionMessageListsData
    
    
