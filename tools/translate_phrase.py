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
                "japanese": {"text": "ありがとう (Arigatou)", "pronunciation": "ah-ree-gah-toh"},
                "mandarin": {"text": "谢谢 (Xièxiè)", "pronunciation": "shyeh-shyeh"},
                "arabic": {"text": "شكرا (Shukran)", "pronunciation": "shoo-kran"},
                "russian": {"text": "Спасибо (Spasibo)", "pronunciation": "spah-see-boh"},
                "portuguese": {"text": "Obrigado/a", "pronunciation": "oh-bree-gah-doo/dah"},
                "thai": {"text": "ขอบคุณ (Khop khun)", "pronunciation": "kop-koon"}
            },
            "excuse me": {
                "spanish": {"text": "Disculpe", "pronunciation": "dees-kool-peh"},
                "french": {"text": "Excusez-moi", "pronunciation": "ex-koo-zay mwah"},
                "italian": {"text": "Scusi", "pronunciation": "skoo-zee"},
                "german": {"text": "Entschuldigung", "pronunciation": "ent-shool-di-goong"},
                "japanese": {"text": "すみません (Sumimasen)", "pronunciation": "soo-mee-mah-sen"},
                "mandarin": {"text": "对不起 (Duìbùqǐ)", "pronunciation": "dway-boo-chee"},
                "arabic": {"text": "عفوا (Afwan)", "pronunciation": "af-wan"},
                "russian": {"text": "Извините (Izvinite)", "pronunciation": "eez-vee-nee-tye"},
                "portuguese": {"text": "Com licença", "pronunciation": "com lee-sen-sah"},
                "thai": {"text": "ขอโทษ (Kho thot)", "pronunciation": "kor-toht"}
            },
            "where is the bathroom": {
                "spanish": {"text": "¿Dónde está el baño?", "pronunciation": "don-deh es-tah el ban-yo"},
                "french": {"text": "Où sont les toilettes?", "pronunciation": "oo son lay twa-let"},
                "italian": {"text": "Dov'è il bagno?", "pronunciation": "doh-veh eel ban-yo"},
                "german": {"text": "Wo ist die Toilette?", "pronunciation": "vo ist dee twa-let-te"},
                "japanese": {"text": "トイレはどこですか (Toire wa doko desu ka)", "pronunciation": "toy-reh wah doh-koh des-kah"},
                "mandarin": {"text": "厕所在哪里 (Cèsuǒ zài nǎlǐ)", "pronunciation": "tsuh-swor dzeye nah-lee"},
                "arabic": {"text": "أين الحمام (Ayna al-hammam)", "pronunciation": "eye-nah al-ham-mam"},
                "russian": {"text": "Где туалет (Gde tualet)", "pronunciation": "g-dyeh too-ah-lyet"},
                "portuguese": {"text": "Onde fica o banheiro?", "pronunciation": "on-jee fee-ka oo ban-yay-roo"},
                "thai": {"text": "ห้องน้ำอยู่ที่ไหน (Hong nam yu tee nai)", "pronunciation": "hong nam yoo tee nai"}
            },
            "how much": {
                "spanish": {"text": "¿Cuánto cuesta?", "pronunciation": "kwan-toh kwes-tah"},
                "french": {"text": "Combien ça coûte?", "pronunciation": "kom-bee-en sa koot"},
                "italian": {"text": "Quanto costa?", "pronunciation": "kwan-toh kos-tah"},
                "german": {"text": "Wie viel kostet das?", "pronunciation": "vee feel kos-tet das"},
                "japanese": {"text": "いくらですか (Ikura desu ka)", "pronunciation": "ee-koo-rah des-kah"},
                "mandarin": {"text": "多少钱 (Duōshǎo qián)", "pronunciation": "dwor-shaow chyen"},
                "arabic": {"text": "كم الثمن (Kam althaman)", "pronunciation": "kam al-tha-man"},
                "russian": {"text": "Сколько это стоит (Skol'ko eto stoit)", "pronunciation": "skol-ka eh-ta stoh-eet"},
                "portuguese": {"text": "Quanto custa?", "pronunciation": "kwan-too koos-tah"},
                "thai": {"text": "ราคาเท่าไหร่ (Raka tao rai)", "pronunciation": "ra-ka tao-rai"}
            }
        }

    def forward(self, text: str, language: str) -> str:
        try:
            # Try to use a real translation API if the API key is available
            if self.api_key:
                try:
                    url = "https://libretranslate.de/translate"
                    payload = {
                        "q": text,
                        "source": "auto",
                        "target": language.lower()[:2],  # Use first 2 chars as language code
                        "format": "text"
                    }
                    
                    response = requests.post(url, data=payload)
                    data = response.json()
                    
                    if 'translatedText' in data:
                        return f"🗣️ '{text}' in {language.capitalize()}:\n\n{data['translatedText']}"
                    else:
                        # Fall back to stored phrases if API call fails
                        return self._translate_with_stored_phrases(text, language)
                
                except Exception:
                    # Fall back to stored phrases if any error occurs
                    return self._translate_with_stored_phrases(text, language)
            
            # If no API key is available, use the stored phrases
            return self._translate_with_stored_phrases(text, language)
        
        except Exception as e:
            return f"Error translating text: {str(e)}"
    
    def _translate_with_stored_phrases(self, text: str, language: str) -> str:
        # Normalize inputs
        text_lower = text.lower().strip()
        language = language.lower().strip()
        
        # Find the phrase key that most closely matches the input text
        matched_phrase = None
        for phrase in self.phrase_translations:
            if phrase in text_lower or text_lower in phrase:
                matched_phrase = phrase
                break
        
        if not matched_phrase:
            return f"I don't have a translation for '{text}'. Try common travel phrases like 'hello', 'thank you', 'excuse me', etc."
        
        # Find the language that most closely matches the input language
        matched_language = None
        for lang in self.phrase_translations[matched_phrase]:
            if lang in language or language in lang:
                matched_language = lang
                break
        
        if not matched_language:
            return f"I don't have translations for {language}. Try languages like Spanish, French, Italian, German, Japanese, etc."
        
        # Get the translation
        translation = self.phrase_translations[matched_phrase][matched_language]
        
        return f"🗣️ '{text}' in {matched_language.capitalize()}:\n\n{translation['text']}\n\nPronunciation: {translation['pronunciation']}"