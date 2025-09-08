import uuid
from pydantic import BaseModel


class ChatbotAppointmentCreateDto(BaseModel):
    department_id: uuid.UUID
    start_time: str