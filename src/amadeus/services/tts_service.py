from datetime import datetime
from io import BytesIO
from typing import List
from edge_tts import list_voices
from edge_tts.typing import Voice
from starlette.responses import StreamingResponse
from src.amadeus.config import Config
from src.amadeus.mappers.tts_model_mapper import TTSModelMapper
from src.amadeus.mappers.tts_voice_mapper import TTSVoiceMapper
from src.amadeus.schemas.queries.base_query_schema import PageSchema, PageableSchema
from src.amadeus.schemas.queries.tts_model_query_schema import TTSModelQuerySchema
from src.amadeus.schemas.queries.tts_voice_query_schema import TTSVoiceQuerySchema
from src.amadeus.schemas.requests.tts_talk_request_schema import TTSRequestSchema
from src.amadeus.schemas.responses.tts_model_response_schema import TTSModelResponseSchema
from src.amadeus.schemas.responses.tts_voice_response_schema import TTSVoiceResponseSchema
from src.amadeus.utils.tts_utils import TTSUtils

class TTSService:
    @classmethod
    async def tts(cls, request: TTSRequestSchema) -> StreamingResponse:
        fp: BytesIO = await TTSUtils.tts(
            text=request.text,
            tts_voice=request.tts_voice,
            tts_speech_speed=request.tts_speech_speed,
            rvc_model=request.rvc_model,
            rvc_f0_method=request.rvc_f0_method,
            rvc_f0_up_key=request.rvc_f0_up_key,
            rvc_index_rate=request.rvc_index_rate,
            rvc_protect=request.rvc_protect
        )

        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename: str = f"output_{timestamp}.wav"
        return StreamingResponse(
            content=fp,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    @classmethod
    async def voices(cls, query: TTSVoiceQuerySchema) -> PageSchema[TTSVoiceResponseSchema]:
        voices: List[Voice] = await list_voices()
        start_idx: int = query.page * query.size
        return PageSchema[TTSVoiceResponseSchema](
            content=[TTSVoiceMapper.to_response(x) for x in voices[start_idx : start_idx + query.size]],
            pageable=PageableSchema(
                page_number=query.page,
                page_size=query.size,
                total_elements=len(voices)
            )
        )

    @classmethod
    def models(cls, query: TTSModelQuerySchema) -> PageSchema[TTSModelResponseSchema]:
        models: List[str] = [x.stem for x in Config.Paths.WEIGHTS.glob("*.pth")]
        start_idx: int = query.page * query.size
        return PageSchema[TTSModelResponseSchema](
            content=[TTSModelMapper.to_response(x) for x in models[start_idx : start_idx + query.size]],
            pageable=PageableSchema(
                page_number=query.page,
                page_size=query.size,
                total_elements=len(models)
            )
        )
