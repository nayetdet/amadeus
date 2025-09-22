from typing import Optional
from pydantic import BaseModel

class TTSModelResponseSchema(BaseModel):
    name: Optional[str] = None
