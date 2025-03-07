from typing import Any, Optional
from smolagents.tools import Tool
from duckduckgo_search import DDGS

class SearchAccommodationsTool(Tool):
    name = "search_accommodations"
    description = "Searches for available accommodations at a travel destination with customizable filters like budget, style, and location."
    inputs = {
        'destination': {'type': 'string', 'description': 'The destination city or region (e.g., "Tokyo", "Bali", "Paris")'},
        'budget': {'type': 'string', 'description': 'Price range (e.g., "budget", "mid-range", "luxury")', 'nullable': True},
        'style': {'type': 'string', 'description': 'Type of accommodation (e.g., "hotel", "hostel", "apartment", "resort")', 'nullable': True},
        'location': {'type': 'string', 'description': 'Preferred area or neighborhood', 'nullable': True}
    }
    output_type = "string"

    def __init__(self, max_results=8):
        super().__init__()
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
            ) from e
        self.ddgs = DDGS()
        self.max_results = max_results

    def forward(self, destination: str, budget: Optional[str] = None, style: Optional[str] = None, location: Optional[str] = None) -> str:
        try:
            # Construct a search query based on the parameters
            query = f"accommodations {destination}"
            
            if budget:
                query += f" {budget} price"
            
            if style:
                query += f" {style}"
            
            if location:
                query += f" in {location}"
            
            # Execute the search
            results = self.ddgs.text(query, max_results=self.max_results)
            
            if not results:
                return f"No accommodation results found for {destination}. Try adjusting your search parameters."
            
            # Format the results
            formatted_results = f"🏨 **Accommodation Options in {destination}**\n\n"
            
            # Add search parameters if provided
            search_params = []
            if budget:
                search_params.append(f"Budget: {budget}")
            if style:
                search_params.append(f"Type: {style}")
            if location:
                search_params.append(f"Area: {location}")
            
            if search_params:
                formatted_results += "Search filters: " + ", ".join(search_params) + "\n\n"
            
            # Format each result
            for i, result in enumerate(results, 1):
                title = result.get('title', 'Unnamed Accommodation')
                url = result.get('href', '#')
                snippet = result.get('body', 'No description available')
                
                formatted_results += f"### {i}. {title}\n"
                formatted_results += f"{snippet}\n"
                formatted_results += f"[View Details]({url})\n\n"
            
            formatted_results += "Note: These are search results. For accurate pricing and availability, check the official websites or booking platforms."
            
            return formatted_results
            
        except Exception as e:
            return f"Error searching for accommodations: {str(e)}"
