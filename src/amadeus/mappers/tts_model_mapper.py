from src.amadeus.schemas.responses.tts_model_response_schema import TTSModelResponseSchema

class TTSModelMapper:
    @classmethod
    def to_response(cls, name) -> TTSModelResponseSchema:
        return TTSModelResponseSchema(name=name)
