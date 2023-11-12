import enum
from sqlalchemy.orm import Session
from . import models,schemas as chat_schemas




def create_chat_interation(db: Session, interaction: chat_schemas.InteractionCreationModel) -> chat_schemas.InteractionResponseModel:    
    db_chat_intraction = models.Intraction( **interaction.model_dump())
    db.add(db_chat_intraction)
    db.commit()
    db.refresh(db_chat_intraction)
    response = chat_schemas.InteractionResponseModel(**db_chat_intraction.__dict__)

    return response


def get_intraction(id:int,db: Session,)-> models.Intraction:
    return db.query(models.Intraction).filter_by(id = id).first()




async def create_interation_messages(db: Session, interaction_message: chat_schemas.InteractionMessage) -> chat_schemas.IntractionMessageReponseModel:    
    db_chat_intraction_message = models.InteractionMessage( **interaction_message.model_dump())
    db.add(db_chat_intraction_message)
    db.commit()
    db.refresh(db_chat_intraction_message)
    response = chat_schemas.IntractionMessageReponseModel(**db_chat_intraction_message.__dict__)

    return response

