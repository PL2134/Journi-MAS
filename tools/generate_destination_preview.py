from typing import Any, Optional
from smolagents.tools import Tool
from smolagents import load_tool
import random

class GenerateDestinationPreviewTool(Tool):
    name = "generate_destination_preview"
    description = "Generates a vibrant, artistic preview image of a travel destination."
    inputs = {'destination': {'type': 'string', 'description': 'The travel destination to visualize (e.g., "Paris", "Tokyo", "Bali").'}}
    output_type = "string"

    def __init__(self):
        super().__init__()
        
        # Try to load the image generation tool from the hub
        try:
            self.image_model = load_tool("agents-course/text-to-image", trust_remote_code=True)
            self.has_image_model = True
        except Exception:
            self.has_image_model = False
        
        # List of visual styles for variety
        self.styles = [
            "sunrise golden hour", 
            "blue hour twilight", 
            "vibrant daytime", 
            "dramatic sunset", 
            "night lights"
        ]
        
        # Common descriptions for popular destinations (fallback if image generation fails)
        self.destination_descriptions = {
            "paris": "The Eiffel Tower stands tall against a backdrop of elegant Haussmannian buildings. Charming cafés line the cobblestone streets as the Seine River winds through the heart of the city.",
            "tokyo": "Neon lights illuminate the bustling streets of Shibuya as modern skyscrapers tower over ancient temples. Cherry blossoms add splashes of pink to the urban landscape in spring.",
            "new york": "The iconic skyline of Manhattan rises majestically with the Empire State Building standing prominently. Yellow taxis navigate the grid of streets as diverse neighborhoods showcase the city's cultural melting pot.",
            "rome": "Ancient ruins of the Colosseum and Forum tell stories of a glorious past. Baroque fountains and piazzas are filled with locals and tourists alike enjoying the Mediterranean sunshine.",
            "bali": "Lush terraced rice fields cascade down hillsides to meet pristine beaches. Hindu temples with intricate stone carvings are set against dramatic volcanic backdrops.",
            "london": "The historic Tower Bridge spans the Thames River with the modern Shard rising in the background. Royal parks offer green spaces amid the bustling city streets.",
            "sydney": "The Opera House's distinctive sail-shaped roofs curve gracefully over the harbor as ferries cross the sparkling blue waters. The Harbour Bridge arches dramatically against the skyline.",
            "mount fuji": "The perfectly symmetrical snow-capped volcanic cone rises majestically above the surrounding lakes and forests. Cherry blossoms or autumn leaves frame the mountain depending on the season.",
            "santorini": "Whitewashed buildings with blue domes cling to dramatic cliffs overlooking the deep blue Aegean Sea. Narrow winding pathways lead through charming villages that catch the golden Mediterranean light.",
            "kyoto": "Ancient wooden temples and shrines are nestled among Japanese maple trees and peaceful Zen gardens. Geisha in colorful kimonos occasionally appear on traditional streets lined with machiya houses."
        }

    def forward(self, destination: str) -> str:
        # Select a random style for variety
        style = random.choice(self.styles)
        
        # Construct a detailed prompt for the AI model
        prompt = f"A beautiful travel photograph of {destination}, {style}, photorealistic, high-resolution, travel photography, highly detailed landmark view"
        
        # Try to generate an image if the model is available
        if self.has_image_model:
            try:
                image_url = self.image_model(prompt)
                
                # Find a matching description for additional context
                dest_lower = destination.lower()
                description = None
                for key, value in self.destination_descriptions.items():
                    if key in dest_lower or dest_lower in key:
                        description = value
                        break
                
                # Include a description if available
                if description:
                    return f"Here's a preview of {destination}: {image_url}\n\n{description}"
                else:
                    return f"Here's a preview of {destination}: {image_url}"
                
            except Exception as e:
                # Fall back to text description if image generation fails
                return self._generate_text_description(destination, style)
        else:
            # Fall back to text description if no image model is available
            return self._generate_text_description(destination, style)
    
    def _generate_text_description(self, destination: str, style: str) -> str:
        # Normalize destination name
        dest_lower = destination.lower()
        
        # Look for matching or partial matching descriptions
        description = None
        for key, value in self.destination_descriptions.items():
            if key in dest_lower or dest_lower in key:
                description = value
                break
        
        # Generate a generic description if no specific one is found
        if not description:
            landmark_types = ["mountains", "beaches", "historic sites", "urban centers", "natural wonders", "cultural attractions"]
            activities = ["explore", "discover", "experience", "immerse yourself in", "marvel at"]
            features = ["beautiful", "breathtaking", "stunning", "picturesque", "magnificent"]
            
            random.seed(sum(ord(c) for c in destination))  # Make it deterministic based on destination
            landmark = random.choice(landmark_types)
            activity = random.choice(activities)
            feature = random.choice(features)
            
            description = f"The {feature} {landmark} of {destination} invite you to {activity} this incredible destination. The unique atmosphere and character create an unforgettable travel experience that captivates visitors from around the world."
        
        # Format the final response
        return f"✨ Destination Preview: {destination} ✨\n\n{description}\n\nImagine {destination} during {style} - a perfect time to capture memories of this magnificent destination."
