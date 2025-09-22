from typing import Optional
from pydantic import BaseModel

class TTSVoiceResponseSchema(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    locale: Optional[str] = None
