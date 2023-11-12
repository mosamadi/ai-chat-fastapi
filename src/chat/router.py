from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db_session
from ..auth.services import get_auth_user
from ..auth.schemas import UserInfo
from ..auth.models import UserModel
from . import schemas as chat_schema,services as chat_services
from pydantic import TypeAdapter
from .models import Intraction
from .dependencies import get_AI_conselor

router = APIRouter()


@router.post('/interaction',response_model=chat_schema.InteractionResponseModel)
def new_interaction(interaction: chat_schema.InteractionBaseModel , user:UserModel= Depends(get_auth_user),db: Session = Depends(get_db_session)):
    return chat_services.create_chat_interation(db,chat_schema.InteractionCreationModel(**interaction.model_dump(),user_id=user.id))


@router.get('/interactions',response_model=List[chat_schema.InteractionResponseModel])
def get_user_all_interactions(user:UserModel= Depends(get_auth_user)) :
    interactions = user.interactions
    return  [chat_schema.InteractionResponseModel(**interaction.__dict__) for interaction in interactions]


@router.post('/interaction/message',response_model=chat_schema.IntractionMessageReponseModel)
async def new_interaction_message(interaction_message: chat_schema.BaseInteractionMessage, user:UserModel= Depends(get_auth_user) ,db: Session = Depends(get_db_session)):
    db_intraction = chat_services.get_intraction(interaction_message.intraction_id,db)

    if db_intraction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intraction not found")
    if db_intraction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action!")
    
    chat_services.create_interation_messages(db,chat_schema.InteractionMessage(**interaction_message.model_dump()))
    ai = get_AI_conselor()
    ai_intraction = ai.get_AI_consultancy(db_intraction.messages)
    ai_response = await chat_services.create_interation_messages(db,ai_intraction)

    return ai_response

@router.get('/interaction/{intraction_id}/messages',response_model=chat_schema.IntractionMessageListResponses)
async def get_all_intraction_messages(intraction_id, user:UserModel= Depends(get_auth_user) ,db: Session = Depends(get_db_session)):
    db_intraction   = chat_services.get_intraction(intraction_id,db)
    return  chat_schema.IntractionMessageListResponses( data= chat_schema.IntractionMessageListsData(
        messages=[{chat_schema.IntractionMessageReponseModel(**message.__dict__) for message in db_intraction.messages}],
        id = intraction_id, settings= get_AI_conselor().get_AI_settings()
        ))
    