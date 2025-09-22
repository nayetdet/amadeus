from fastapi import status
from src.amadeus.exceptions import BaseApplicationException

class TTSModelNotFoundException(BaseApplicationException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    MESSAGE = "Requested RVC model not found."

class TTSVoiceNotFoundException(BaseApplicationException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    MESSAGE = "Requested TTS voice not found."
