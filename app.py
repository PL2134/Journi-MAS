# Travel Companion AI Agent
# This agent helps travelers with destination information, local time, weather forecasts,
# currency conversion, language translation, and visual destination previews.

from smolagents import CodeAgent, HfApiModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
import random
import json
import os
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI

# Load the image generation tool once, outside the function
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# ==================== ORIGINAL TOOLS (ENHANCED) ====================

@tool
def generate_destination_preview(destination: str) -> str:
    """Generates a vibrant, artistic preview image of a travel destination.
    
    Args:
        destination: The travel destination to visualize (e.g., 'Paris', 'Tokyo', 'Bali').
        
    Returns:
        A link to the generated destination preview image.
    """
    # List of visual styles for variety
    styles = [
        "sunrise golden hour", 
        "blue hour twilight", 
        "vibrant daytime", 
        "dramatic sunset", 
        "night lights"
    ]
    
    # Select a random style for variety
    style = random.choice(styles)
    
    # Construct a detailed prompt for the AI model
    prompt = f"A beautiful travel photograph of {destination}, {style}, photorealistic, high-resolution, travel photography, highly detailed landmark view"
    
    # Use the pre-loaded image generation tool
    try:
        image_url = image_generation_tool(prompt)
        return f"Here's a preview of {destination}: {image_url}"
    except Exception as e:
        return f"Error generating image of {destination}: {str(e)}"


@tool
def get_local_time(destination: str) -> str:
    """Get the current local time at a travel destination.
    
    Args:
        destination: A city or location name (e.g., 'Paris', 'Tokyo', 'New York').
        
    Returns:
        The current local time at the specified destination.
    """
    # Map of common tourist destinations to their timezones
    destination_timezones = {
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "rome": "Europe/Rome",
        "madrid": "Europe/Madrid",
        "berlin": "Europe/Berlin",
        "amsterdam": "Europe/Amsterdam",
        "athens": "Europe/Athens",
        "istanbul": "Europe/Istanbul",
        "dubai": "Asia/Dubai",
        "new delhi": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "bangkok": "Asia/Bangkok",
        "singapore": "Asia/Singapore",
        "tokyo": "Asia/Tokyo",
        "seoul": "Asia/Seoul",
        "beijing": "Asia/Shanghai",
        "shanghai": "Asia/Shanghai",
        "hong kong": "Asia/Hong_Kong",
        "sydney": "Australia/Sydney",
        "melbourne": "Australia/Melbourne",
        "auckland": "Pacific/Auckland",
        "fiji": "Pacific/Fiji",
        "honolulu": "Pacific/Honolulu",
        "anchorage": "America/Anchorage",
        "los angeles": "America/Los_Angeles",
        "san francisco": "America/Los_Angeles",
        "las vegas": "America/Los_Angeles",
        "denver": "America/Denver",
        "chicago": "America/Chicago",
        "houston": "America/Chicago",
        "new york": "America/New_York",
        "miami": "America/New_York",
        "toronto": "America/Toronto",
        "mexico city": "America/Mexico_City",
        "rio de janeiro": "America/Sao_Paulo",
        "sao paulo": "America/Sao_Paulo",
        "buenos aires": "America/Argentina/Buenos_Aires",
        "cairo": "Africa/Cairo",
        "cape town": "Africa/Johannesburg",
        "johannesburg": "Africa/Johannesburg",
        "nairobi": "Africa/Nairobi"
    }
    
    try:
        # Normalize the destination name
        normalized_dest = destination.lower().strip()
        
        # Find the closest matching timezone
        timezone = None
        for city, tz in destination_timezones.items():
            if city in normalized_dest or normalized_dest in city:
                timezone = tz
                break
        
        if not timezone:
            return f"I don't have timezone information for {destination}. Please try a major city nearby."
        
        # Get current time in that timezone
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz)
        
        # Format the result
        formatted_time = local_time.strftime("%I:%M %p on %A, %B %d, %Y")
        time_diff = local_time.utcoffset().total_seconds() / 3600
        sign = "+" if time_diff >= 0 else ""
        
        return f"The current local time in {destination} is {formatted_time} (UTC{sign}{int(time_diff)})"
    
    except Exception as e:
        return f"Error getting local time for {destination}: {str(e)}"

# ==================== NEW TRAVEL-SPECIFIC TOOLS ====================

@tool
def get_weather_forecast(destination: str, days: int = 3) -> str:
    """Get the weather forecast for a travel destination.
    
    Args:
        destination: City or location name
        days: Number of days to forecast (default: 3)
        
    Returns:
        Weather forecast information for trip planning
    """
    try:
        # In a production environment, you would use a real API key
        API_KEY = os.environ.get("WEATHER_API_KEY", "demo_key")
        
        # For demo purposes, we'll generate simulated weather data
        # In a real implementation, you would call an actual weather API
        weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Thunderstorms", "Windy", "Foggy", "Snow", "Clear"]
        
        # Create a deterministic but seemingly random forecast based on destination name
        seed = sum(ord(c) for c in destination)
        random.seed(seed)
        
        # Generate forecast data
        forecast_text = f"🌦️ Weather forecast for {destination}:\n\n"
        
        today = datetime.datetime.now()
        for i in range(days):
            day = today + datetime.timedelta(days=i)
            day_name = day.strftime("%A")
            date = day.strftime("%b %d")
            
            # "Random" but deterministic weather for the demo
            condition = weather_conditions[random.randint(0, len(weather_conditions)-1)]
            temp_high = random.randint(15, 35)  # Celsius
            temp_low = temp_high - random.randint(5, 15)
            precipitation = random.randint(0, 100) if "Rain" in condition or "Snow" in condition or "Thunder" in condition else 0
            
            forecast_text += f"• {day_name}, {date}: {condition}, {temp_low}°C to {temp_high}°C"
            if precipitation > 0:
                forecast_text += f", {precipitation}% chance of precipitation"
            forecast_text += "\n"
        
        # Add packing recommendations based on conditions
        coldest = min([forecast_text.count("Snow"), forecast_text.count("0°C")])
        rainiest = forecast_text.count("Rain") + forecast_text.count("Thunder")
        
        forecast_text += "\n🧳 Packing tips: "
        if coldest > 0:
            forecast_text += "Bring warm layers and a heavy jacket. "
        elif "5°C" in forecast_text or "6°C" in forecast_text or "7°C" in forecast_text:
            forecast_text += "Pack a warm jacket and layers. "
        
        if rainiest > 0:
            forecast_text += "Don't forget an umbrella and waterproof footwear. "
        
        if "Sunny" in forecast_text and "30°C" in forecast_text:
            forecast_text += "Bring sunscreen, sunglasses, and light clothing. "
            
        return forecast_text
    
    except Exception as e:
        return f"Error retrieving weather data for {destination}: {str(e)}"


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount between currencies for travel budgeting.
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (e.g., USD, EUR)
        to_currency: Target currency code (e.g., JPY, GBP)
        
    Returns:
        Converted amount and exchange rate information
    """
    try:
        # In a production environment, you would use a real API key
        # For demo purposes, we'll use fixed exchange rates
        # In a real implementation, you would call an actual currency API
        
        # Common exchange rates (as of early 2025, for demo purposes)
        exchange_rates = {
            "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 149.50, "CAD": 1.35, "AUD": 1.52, "CNY": 7.20, "INR": 83.20, "MXN": 17.05},
            "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 163.00, "CAD": 1.47, "AUD": 1.66, "CNY": 7.85, "INR": 90.70, "MXN": 18.60},
            "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 189.30, "CAD": 1.71, "AUD": 1.92, "CNY": 9.10, "INR": 105.30, "MXN": 21.60},
            "JPY": {"USD": 0.0067, "EUR": 0.0061, "GBP": 0.0053, "CAD": 0.0090, "AUD": 0.0102, "CNY": 0.0482, "INR": 0.5565, "MXN": 0.1141},
            "CAD": {"USD": 0.74, "EUR": 0.68, "GBP": 0.58, "JPY": 110.70, "AUD": 1.13, "CNY": 5.33, "INR": 61.60, "MXN": 12.60},
            "AUD": {"USD": 0.66, "EUR": 0.60, "GBP": 0.52, "JPY": 98.40, "CAD": 0.89, "CNY": 4.73, "INR": 54.70, "MXN": 11.20},
            "CNY": {"USD": 0.14, "EUR": 0.13, "GBP": 0.11, "JPY": 20.80, "CAD": 0.19, "AUD": 0.21, "INR": 11.60, "MXN": 2.37},
            "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095, "JPY": 1.80, "CAD": 0.016, "AUD": 0.018, "CNY": 0.086, "MXN": 0.205},
            "MXN": {"USD": 0.059, "EUR": 0.054, "GBP": 0.046, "JPY": 8.77, "CAD": 0.079, "AUD": 0.089, "CNY": 0.422, "INR": 4.88}
        }
        
        # Normalize currency codes
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        
        # Validate currencies
        if from_currency not in exchange_rates:
            return f"Sorry, I don't have exchange rate data for {from_currency}."
        
        if to_currency not in exchange_rates[from_currency] and to_currency != from_currency:
            return f"Sorry, I don't have exchange rate data from {from_currency} to {to_currency}."
        
        # If same currency, return original amount
        if from_currency == to_currency:
            return f"{amount} {from_currency} = {amount} {to_currency}"
        
        # Get exchange rate and calculate conversion
        rate = exchange_rates[from_currency][to_currency]
        converted_amount = amount * rate
        
        # Format the result
        return f"💱 {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}\n\nExchange rate: 1 {from_currency} = {rate} {to_currency}\n\n(Note: Actual rates may vary. For planning purposes only.)"
    
    except Exception as e:
        return f"Error converting currency: {str(e)}"


@tool
def translate_phrase(text: str, language: str) -> str:
    """Translate common travel phrases to a local language.
    
    Args:
        text: Text to translate (e.g., "Hello", "Thank you", "Where is the bathroom?")
        language: Target language (e.g., 'Spanish', 'Japanese', 'French')
        
    Returns:
        Translated text with pronunciation guide
    """
    try:
        # Common travel phrases in various languages
        # In a production environment, you would use a real translation API
        language = language.lower().strip()
        text_lower = text.lower().strip()
        
        phrase_translations = {
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
        
        # Find the phrase key that most closely matches the input text
        matched_phrase = None
        for phrase in phrase_translations:
            if phrase in text_lower or text_lower in phrase:
                matched_phrase = phrase
                break
        
        if not matched_phrase:
            return f"I don't have a translation for '{text}'. Try common travel phrases like 'hello', 'thank you', 'excuse me', etc."
        
        # Find the language that most closely matches the input language
        matched_language = None
        for lang in phrase_translations[matched_phrase]:
            if lang in language or language in lang:
                matched_language = lang
                break
        
        if not matched_language:
            return f"I don't have translations for {language}. Try languages like Spanish, French, Italian, German, Japanese, etc."
        
        # Get the translation
        translation = phrase_translations[matched_phrase][matched_language]
        
        return f"🗣️ '{text}' in {matched_language.capitalize()}:\n\n{translation['text']}\n\nPronunciation: {translation['pronunciation']}"
    
    except Exception as e:
        return f"Error translating text: {str(e)}"


@tool
def get_visa_requirements(nationality: str, destination: str) -> str:
    """Check visa requirements for traveling to a destination.
    
    Args:
        nationality: Traveler's passport country (e.g., 'US', 'UK', 'Canada')
        destination: Country to visit (e.g., 'Japan', 'France', 'Brazil')
        
    Returns:
        Visa requirement information
    """
    try:
        # Normalize inputs
        nationality = nationality.lower().strip()
        destination = destination.lower().strip()
        
        # Map of common country names to their normalized forms
        country_mapping = {
            "us": "united states", "usa": "united states", "united states of america": "united states",
            "uk": "united kingdom", "britain": "united kingdom", "great britain": "united kingdom",
            "uae": "united arab emirates",
            # Add more mappings as needed
        }
        
        # Apply mappings if available
        nationality = country_mapping.get(nationality, nationality)
        destination = country_mapping.get(destination, destination)
        
        # Skip if same country (generally no visa needed for citizens)
        if nationality == destination:
            return f"As a citizen of {nationality.title()}, you generally don't need a visa to visit your own country."
        
        # Sample visa requirement data
        # In a production environment, this would be a comprehensive database or API call
        visa_data = {
            "united states": {
                "european union": "No visa required for stays up to 90 days",
                "united kingdom": "No visa required for stays up to 6 months",
                "japan": "No visa required for stays up to 90 days",
                "australia": "Electronic Travel Authority (ETA) required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "No visa required for stays up to 90 days",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days"
            },
            "united kingdom": {
                "european union": "No visa required for stays up to 90 days",
                "united states": "ESTA required for entry",
                "japan": "No visa required for stays up to 90 days",
                "australia": "eVisitor visa required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "No visa required for stays up to 90 days",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days"
            },
            # Add more countries as needed
        }
        
        # Check if we have data for this nationality
        if nationality not in visa_data:
            return f"I don't have specific visa information for citizens of {nationality.title()}. Please check with the embassy of {destination.title()} for accurate visa requirements."
        
        # Check if we have data for this destination
        if destination not in visa_data[nationality]:
            return f"I don't have specific visa information for {nationality.title()} citizens traveling to {destination.title()}. Please check with the embassy of {destination.title()} for accurate visa requirements."
        
        # Get the visa requirements
        requirements = visa_data[nationality][destination]
        
        return f"🛂 Visa requirements for {nationality.title()} citizens traveling to {destination.title()}:\n\n{requirements}\n\n(Note: Visa requirements may change. Always verify with the official embassy or consulate before travel.)"
    
    except Exception as e:
        return f"Error retrieving visa information: {str(e)}"

# ==================== AGENT SETUP ====================

final_answer = FinalAnswerTool()

# Model initialization
model = HfApiModel(
    max_tokens=2096,
    temperature=0.7,  # Slightly higher temperature for more creative responses
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

# Load prompts
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# Add travel companion specific instructions to the prompt templates
travel_agent_prompt = """
You are TravelBuddy, an AI travel companion designed to help travelers plan and navigate their journeys.
Your goal is to provide helpful, accurate information about destinations, local customs, and practical travel advice.

You have access to these capabilities:
1. Generate visual previews of destinations
2. Check local time at travel destinations
3. Provide weather forecasts for trip planning
4. Convert currencies for travel budgeting
5. Translate common travel phrases
6. Check visa requirements

When users ask about a destination, try to provide comprehensive information by combining multiple tools.
For example, if someone asks about Tokyo, consider providing the local time, weather, and a visual preview.

Always be enthusiastic about travel while remaining practical and informative.
Suggest off-the-beaten-path experiences when appropriate, but prioritize the specific information requested.
"""

# Add the travel agent prompt to the existing templates
if "system_prompt" in prompt_templates:
    prompt_templates["system_prompt"] = travel_agent_prompt + "\n\n" + prompt_templates.get("system_prompt", "")
else:
    prompt_templates["system_prompt"] = travel_agent_prompt

# Agent setup with all travel tools
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        generate_destination_preview,  # Enhanced version of original image tool
        get_local_time,               # Enhanced version of original time tool
        get_weather_forecast,         # New travel tool
        convert_currency,             # New travel tool
        translate_phrase,             # New travel tool
        get_visa_requirements,        # New travel tool
    ],
    max_steps=8,                      # Increased to allow for more tool usage in a single query
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="TravelBuddy",
    description="Your AI travel companion",
    prompt_templates=prompt_templates
)

# Launch the UI
print("Launching TravelBuddy - Your AI Travel Companion")
GradioUI(agent).launch()