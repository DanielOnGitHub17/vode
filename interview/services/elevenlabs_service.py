import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {"xi-api-key": self.api_key}
    
    def text_to_speech(self, text, voice_id="Rachel"):
        """Convert text to speech using Eleven Labs"""
        endpoint = f"{self.base_url}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.content  # Returns audio bytes
        except requests.exceptions.RequestException as e:
            logger.error(f"Eleven Labs error: {e}")
            raise
    
    def get_available_voices(self):
        """Get list of available voices"""
        endpoint = f"{self.base_url}/voices"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching voices: {e}")
            raise
