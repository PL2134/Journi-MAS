from typing import Any, Optional
from smolagents.tools import Tool
import datetime
import pytz

class GetLocalTimeTool(Tool):
    name = "get_local_time"
    description = "Gets the current local time at a travel destination."
    inputs = {'destination': {'type': 'string', 'description': 'A city or location name (e.g., "Paris", "Tokyo", "New York").'}}
    output_type = "string"

    def __init__(self):
        super().__init__()
        try:
            import pytz
        except ImportError as e:
            raise ImportError(
                "You must install package `pytz` to run this tool: for instance run `pip install pytz`."
            ) from e
        
        # Map of common tourist destinations to their timezones
        self.destination_timezones = {
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

    def forward(self, destination: str) -> str:
        try:
            # Normalize the destination name
            normalized_dest = destination.lower().strip()
            
            # Find the closest matching timezone
            timezone = None
            for city, tz in self.destination_timezones.items():
                if city in normalized_dest or normalized_dest in city:
                    timezone = tz
                    break
            
            if not timezone:
                # If we don't have a direct match, try to find it through pytz
                try:
                    # Try web search for timezone if available
                    import importlib
                    if importlib.util.find_spec("duckduckgo_search"):
                        from duckduckgo_search import DDGS
                        ddgs = DDGS()
                        results = ddgs.text(f"{destination} timezone")
                        if results:
                            # Simple heuristic to extract timezone from search results
                            for result in results:
                                body = result.get('body', '').lower()
                                if 'utc' in body or 'gmt' in body:
                                    timezone_pos = body.find('utc') if 'utc' in body else body.find('gmt')
                                    timezone_info = body[timezone_pos:timezone_pos+8]
                                    return f"Based on web search, the timezone in {destination} appears to be around {timezone_info.upper()}. Current time information is not available."
                except:
                    pass
                
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
