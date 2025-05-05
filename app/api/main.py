from fastapi import FastAPI, HTTPException

from app.core.logging import app_logger
from app.models import GetMessageRequestModel, GetMessageResponseModel, IncomingMessage, Prediction
from random import random
from uuid import uuid4

app = FastAPI()


@app.post("/get_message", response_model=GetMessageResponseModel)
async def get_message(body: GetMessageRequestModel):
    """
    This functions receives a message from HumanOrNot and returns a response
        Parameters (JSON from POST-request):
            body (GetMessageRequestModel): model with request data
                dialog_id (UUID4): ID of the dialog where the message was sent
                last_msg_text (str): text of the message
                last_message_id (UUID4): ID of this message

        Returns (JSON from response):
            GetMessageResponseModel: model with response data
                new_msg_text (str): Ответ бота
                dialog_id (str): ID диалога
    """

    app_logger.info(
        f"Received message dialog_id: {body.dialog_id}, last_msg_id: {body.last_message_id}"
    )
    return GetMessageResponseModel(
        new_msg_text=body.last_msg_text, dialog_id=body.dialog_id
    )

@app.post("/predict", response_model=Prediction)
def predict(msg: IncomingMessage) -> Prediction:
    """
    Endpoint to save a message and get the probability
    that this message if from bot .

    Returns a `Prediction` object.
    """

    is_bot_probability = random()  # Simulate a probability for the sake of example
    prediction_id = uuid4()

    return Prediction(
        id=prediction_id,
        message_id=msg.id,
        dialog_id=msg.dialog_id,
        participant_index=msg.participant_index,
        is_bot_probability=is_bot_probability
    )