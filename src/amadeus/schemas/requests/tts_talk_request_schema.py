from typing import Literal
from pydantic import BaseModel, Field

class TTSRequestSchema(BaseModel):
    text: str
    tts_voice: str = "pt-BR-ThalitaMultilingualNeural"
    tts_speech_speed: int = Field(0, ge=-100, le=200)
    rvc_model: str = "miku_default_rvc"
    rvc_f0_method: Literal["rmvpe", "crepe", "harvest", "pm"] = "rmvpe"
    rvc_f0_up_key: int = Field(6, ge=-12, le=12)
    rvc_index_rate: float = Field(1, ge=0, le=1)
    rvc_protect: float = Field(0.33, ge=0, le=0.5)
