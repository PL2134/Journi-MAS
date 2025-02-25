from typing import Any, Optional
from smolagents.tools import Tool
import os
import requests

class TranslatePhraseTool(Tool):
    name = "translate_phrase"
    description = "Translates common travel phrases to a local language."
    inputs = {
        'text': {'type': 'string', 'description': 'Text to translate (e.g., "Hello", "Thank you", "Where is the bathroom?")'},
        'language': {'type': 'string', 'description': 'Target language (e.g., "Spanish", "Japanese", "French")'}
    }
    output_type = "string"

    def __init__(self, api_key=None):
        super().__init__()
        # You can set an API key for a real translation API
        self.api_key = api_key or os.environ.get("TRANSLATION_API_KEY")
        
        # Common travel phrases in various languages (for demo/fallback purposes)
        self.phrase_translations = {
            "hello": {
                "spanish": {"text": "Hola", "pronunciation": "oh-lah"},
                "french": {"text": "Bonjour", "pronunciation": "bohn-zhoor"},
                "italian": {"text": "Ciao", "pronunciation": "chow"},
                "german": {"text": "Hallo", "pronunciation": "hah-loh"},
                "japanese": {"text": "こんにちは (Konnichiwa)", "pronunciation": "kohn-nee-chee-wah"},
                "mandarin": {"text": "你好 (Nǐ hǎo)", "pronunciation": "nee how"},
                "arabic": {"text": "مرحبا (Marhaba)", "pronunciation": "mar-ha-ba"},
                "russian": {"text": "Здравствуйте (Zdravstvuyte)", "pronunciation": "zdrah-stvooy-tye"},
                "portuguese": {"text": "Olá", "pronunciation": "oh-lah"},
                "thai": {"text": "สวัสดี (Sawatdee)", "pronunciation": "sa-wat-dee"}
            },
            "thank you": {
                "spanish": {"text": "Gracias", "pronunciation": "grah-see-ahs"},
                "french": {"text": "Merci", "pronunciation": "mair-see"},
                "italian": {"text": "Grazie", "pronunciation": "graht-see-eh"},
                "german": {"text": "Danke", "pronunciation": "dahn-kuh"},
                "japanese": {"text": "ありがとう (Arigatou)", "pronunciation": "ah-