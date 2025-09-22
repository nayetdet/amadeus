import aiofiles
import torch
import fairseq.data
from io import BytesIO
from edge_tts import Communicate, list_voices
from typing import Set
from pathlib import Path
from rvc_python.infer import RVCInference
from src.amadeus.config import Config
from src.amadeus.exceptions.tts_exceptions import TTSModelNotFoundException, TTSVoiceNotFoundException

torch.serialization.add_safe_globals([fairseq.data.dictionary.Dictionary])

class TTSUtils:
    __device: str = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    async def tts(
            cls,
            text: str,
            tts_voice: str,
            tts_speech_speed: int,
            rvc_model: str,
            rvc_f0_method: str,
            rvc_f0_up_key: int,
            rvc_index_rate: float,
            rvc_protect: float
    ) -> BytesIO:
        tts_fp: BytesIO = await cls.__raw_tts(
            text=text,
            tts_voice=tts_voice,
            tts_speech_speed=tts_speech_speed
        )

        return await cls.__rvc(
            tts_fp=tts_fp,
            rvc_model=rvc_model,
            rvc_f0_method=rvc_f0_method,
            rvc_f0_up_key=rvc_f0_up_key,
            rvc_index_rate=rvc_index_rate,
            rvc_protect=rvc_protect
        )

    @classmethod
    async def __raw_tts(
            cls, text: str,
            tts_voice: str,
            tts_speech_speed: int
    ) -> BytesIO:
        voices: Set[str] = {x["ShortName"] for x in await list_voices()}
        if tts_voice not in voices:
            raise TTSVoiceNotFoundException()

        fp: BytesIO = BytesIO()
        communicate: Communicate = Communicate(text, voice=tts_voice, rate=f"{tts_speech_speed:+d}%")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fp.write(chunk["data"])

        fp.seek(0)
        return fp

    @classmethod
    async def __rvc(
            cls,
            tts_fp: BytesIO,
            rvc_model: str,
            rvc_f0_method: str,
            rvc_f0_up_key: int,
            rvc_index_rate: float,
            rvc_protect: float
    ) -> BytesIO:
        model_path: Path = Config.Paths.WEIGHTS / f"{rvc_model}.pth"
        if not model_path.is_file():
            raise TTSModelNotFoundException()

        rvc: RVCInference = RVCInference(device=cls.__device)
        rvc.f0method = rvc_f0_method
        rvc.f0up_key = rvc_f0_up_key
        rvc.index_rate = rvc_index_rate
        rvc.protect = rvc_protect
        rvc.load_model(str(model_path))

        async with aiofiles.tempfile.NamedTemporaryFile(suffix=".wav") as tmp_in_file:
            tts_fp.seek(0)
            await tmp_in_file.write(tts_fp.read())
            await tmp_in_file.flush()

            async with aiofiles.tempfile.NamedTemporaryFile(suffix=".wav") as tmp_out_file:
                rvc.infer_file(tmp_in_file.name, tmp_out_file.name)
                await tmp_out_file.seek(0)
                fp: BytesIO = BytesIO(await tmp_out_file.read())
                fp.seek(0)
                return fp
