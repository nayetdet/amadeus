from edge_tts.typing import Voice
from src.amadeus.schemas.responses.tts_voice_response_schema import TTSVoiceResponseSchema

class TTSVoiceMapper:
    @classmethod
    def to_response(cls, voice: Voice) -> TTSVoiceResponseSchema:
        return TTSVoiceResponseSchema(
            name=voice["ShortName"],
            full_name=voice["Name"],
            locale=voice["Locale"]
        )
