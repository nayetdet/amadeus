from fastapi import APIRouter, Depends
from src.amadeus.schemas.queries.base_query_schema import PageSchema
from src.amadeus.schemas.queries.tts_model_query_schema import TTSModelQuerySchema
from src.amadeus.schemas.queries.tts_voice_query_schema import TTSVoiceQuerySchema
from src.amadeus.schemas.requests.tts_talk_request_schema import TTSRequestSchema
from src.amadeus.schemas.responses.tts_model_response_schema import TTSModelResponseSchema
from src.amadeus.schemas.responses.tts_voice_response_schema import TTSVoiceResponseSchema
from src.amadeus.services.tts_service import TTSService

router = APIRouter()

@router.post("/")
async def tts(request: TTSRequestSchema):
    return await TTSService.tts(request)

@router.get("/voices", response_model=PageSchema[TTSVoiceResponseSchema])
async def voices(query: TTSVoiceQuerySchema = Depends()):
    return await TTSService.voices(query)

@router.get("/models", response_model=PageSchema[TTSModelResponseSchema])
def models(query: TTSModelQuerySchema = Depends()):
    return TTSService.models(query)
