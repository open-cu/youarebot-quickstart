from uuid import UUID

from pydantic import UUID4, BaseModel, StrictStr


class CustomBaseModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data


class GetMessageRequestModel(CustomBaseModel):
    """
    Validates incoming data on /get_message endpoint

    Attributes:
        dialog_id (UUID4): ID of the dialog where the message was sent
        last_msg_text (str): text of the message
        last_message_id (UUID4 | None): ID of this message
    """

    dialog_id: UUID4
    last_msg_text: StrictStr
    last_message_id: UUID4 | None


class GetMessageResponseModel(CustomBaseModel):
    """
    Model of message returned by /get_message endpoint

    Attributes:
        new_msg_text (str): Bot's response
        dialog_id (str): dialog ID
    """

    new_msg_text: StrictStr
    dialog_id: UUID4


class IncomingMessage(BaseModel):
    """
    Input schema for a single message that needs to be saved
    and used for dialog classification.
    """
    text: StrictStr
    dialog_id: UUID4
    id: UUID4
    participant_index: int


class Prediction(BaseModel):
    """
    Classification result:
    - id: unique identifier of the prediction
    - message_id: UUID of the message being responded to
    - dialog_id: ID of the dialog
    - participant_index: participant index
    - is_bot_probability: probability that this message is from bot
    """
    id: UUID4
    message_id: UUID4
    dialog_id: UUID4
    participant_index: int
    is_bot_probability: float

