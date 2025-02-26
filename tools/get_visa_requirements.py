from typing import Any, Optional
from smolagents.tools import Tool
import os
import requests

class GetVisaRequirementsTool(Tool):
    name = "get_visa_requirements"
    description = "Checks visa requirements for traveling to a destination."
    inputs = {
        'nationality': {'type': 'string', 'description': "Traveler's passport country (e.g., 'US', 'UK', 'Canada')"},
        'destination': {'type': 'string', 'description': "Country to visit (e.g., 'Japan', 'France', 'Brazil')"}
    }
    output_type = "string"

    def __init__(self, api_key=None):
        super().__init__()
        # You can set an API key for a real visa API service
        self.api_key = api_key or os.environ.get("VISA_API_KEY")
        
        # Map of common country names to their normalized forms
        self.country_mapping = {
            "us": "united states", "usa": "united states", "united states of america": "united states",
            "uk": "united kingdom", "britain": "united kingdom", "great britain": "united kingdom",
            "uae": "united arab emirates", "emirates": "united arab emirates",
            "china": "china", "prc": "china",
            "japan": "japan", 
            "korea": "south korea", "south korea": "south korea", "republic of korea": "south korea",
            "india": "india",
            "germany": "germany",
            "france": "france",
            "italy": "italy",
            "spain": "spain",
            "mexico": "mexico",
            "brazil": "brazil",
            "australia": "australia", "aus": "australia",
            "new zealand": "new zealand", "nz": "new zealand",
            "canada": "canada", "can": "canada",
            "russia": "russia", "russian federation": "russia",
            "south africa": "south africa", "sa": "south africa",
            "thailand": "thailand",
            "vietnam": "vietnam",
            "indonesia": "indonesia",
            "malaysia": "malaysia",
            "philippines": "philippines", "ph": "philippines",
            "singapore": "singapore", "sg": "singapore",
            "egypt": "egypt",
            "turkey": "turkey", "türkiye": "turkey"
        }
        
        # Sample visa requirement data for frequently traveled routes
        self.visa_data = {
            "united states": {
                "european union": "No visa required for stays up to 90 days in the Schengen Area",
                "united kingdom": "No visa required for stays up to 6 months",
                "japan": "No visa required for stays up to 90 days",
                "australia": "Electronic Travel Authority (ETA) required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "No visa required for stays up to 90 days",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days",
                "canada": "No visa required for US citizens"
            },
            "united kingdom": {
                "european union": "No visa required for stays up to 90 days in the Schengen Area",
                "united states": "ESTA required for entry",
                "japan": "No visa required for stays up to 90 days",
                "australia": "eVisitor visa required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "No visa required for stays up to 90 days",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days",
                "canada": "eTA required for British citizens"
            },
            "canada": {
                "european union": "No visa required for stays up to 90 days in the Schengen Area",
                "united states": "No visa required for Canadian citizens",
                "japan": "No visa required for stays up to 90 days",
                "australia": "eVisitor visa required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "No visa required for stays up to 90 days",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days",
                "united kingdom": "No visa required for stays up to 6 months"
            },
            "japan": {
                "european union": "No visa required for stays up to 90 days in the Schengen Area",
                "united states": "ESTA required for entry",
                "australia": "eVisitor visa required",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "Visa required for Japanese citizens",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days",
                "united kingdom": "No visa required for stays up to 6 months",
                "canada": "eTA required for Japanese citizens"
            },
            "australia": {
                "european union": "No visa required for stays up to 90 days in the Schengen Area",
                "united states": "ESTA required for entry",
                "japan": "No visa required for stays up to 90 days",
                "china": "Visa required, must apply in advance",
                "india": "e-Visa available, apply online before travel",
                "brazil": "Visa required for Australian citizens",
                "mexico": "No visa required for stays up to 180 days",
                "south africa": "No visa required for stays up to 90 days",
                "thailand": "No visa required for stays up to 30 days",
                "united kingdom": "No visa required for stays up to 6 months",
                "canada": "eTA required for Australian citizens"
            }
        }

    def forward(self, nationality: str, destination: str) -> str:
        try:
            # Normalize inputs
            nationality = nationality.lower().strip()
            destination = destination.lower().strip()
            
            # Apply mappings if available
            nationality = self.country_mapping.get(nationality, nationality)
            destination = self.country_mapping.get(destination, destination)
            
            # Try to use a real visa API if the API key is available
            if self.api_key:
                try:
                    # This would be the API call in a real implementation
                    # For now, we'll fall back to stored data
                    pass
                except:
                    # Fall back to stored data if API call fails
                    return self._check_with_stored_data(nationality, destination)
            
            # If no API key is available, use the stored data
            return self._check_with_stored_data(nationality, destination)
        
        except Exception as e:
            return f"Error retrieving visa information: {str(e)}"
    
    def _check_with_stored_data(self, nationality: str, destination: str) -> str:
        # Skip if same country (generally no visa needed for citizens)
        if nationality == destination:
            return f"As a citizen of {nationality.title()}, you generally don't need a visa to visit your own country."
        
        # Check if we have data for this nationality
        if nationality not in self.visa_data:
            # Try to search web for information if available
            try:
                import importlib
                if importlib.util.find_spec("duckduckgo_search"):
                    from duckduckgo_search import DDGS
                    ddgs = DDGS()
                    results = ddgs.text(f"visa requirements for {nationality} citizens traveling to {destination}")
                    if results:
                        return f"Based on web search, for {nationality.title()} citizens traveling to {destination.title()}: {results[0]['body']}\n\n(Note: Always verify visa requirements with the official embassy or consulate before travel.)"
            except:
                pass
                
            return f"I don't have specific visa information for citizens of {nationality.title()}. Please check with the embassy of {destination.title()} for accurate visa requirements."
        
        # Check if we have data for this destination
        if destination not in self.visa_data[nationality]:
            # Try to search web for information if available
            try:
                import importlib
                if importlib.util.find_spec("duckduckgo_search"):
                    from duckduckgo_search import DDGS
                    ddgs = DDGS()
                    results = ddgs.text(f"visa requirements for {nationality} citizens traveling to {destination}")
                    if results:
                        return f"Based on web search, for {nationality.title()} citizens traveling to {destination.title()}: {results[0]['body']}\n\n(Note: Always verify visa requirements with the official embassy or consulate before travel.)"
            except:
                pass
                
            return f"I don't have specific visa information for {nationality.title()} citizens traveling to {destination.title()}. Please check with the embassy of {destination.title()} for accurate visa requirements."
        
        # Get the visa requirements
        requirements = self.visa_data[nationality][destination]
        
        return f"🛂 Visa requirements for {nationality.title()} citizens traveling to {destination.title()}:\n\n{requirements}\n\n(Note: Visa requirements may change. Always verify with the official embassy or consulate before travel.)"
