from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI

from app.core.classifier import classify_message, load_model
from app.core.logging import app_logger
from app.models import GetMessageRequestModel, GetMessageResponseModel, IncomingMessage, Prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the text-classification model once, at startup, so /predict is fast.
    load_model()
    yield


app = FastAPI(lifespan=lifespan)


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
    Classify a single message and return the probability that it is from a bot.
    """

    is_bot_probability = classify_message(msg.text)

    return Prediction(
        id=uuid4(),
        message_id=msg.id,
        dialog_id=msg.dialog_id,
        participant_index=msg.participant_index,
        is_bot_probability=is_bot_probability,
    )
