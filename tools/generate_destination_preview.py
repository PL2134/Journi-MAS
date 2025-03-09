from typing import Any, Optional
from smolagents.tools import Tool
from smolagents.agent_types import AgentImage
from smolagents import Tool as BaseSmolTool  # Using a different name to avoid conflict

class GenerateDestinationPreviewTool(Tool):
    name = "generate_destination_preview"
    description = "Generates a visual preview of a travel destination using AI image generation."
    inputs = {'destination': {'type': 'string', 'description': 'The travel destination to visualize (e.g., "Paris", "Tokyo", "Bali").'}}
    output_type = "image"

    def __init__(self):
        super().__init__()
        # Initialize image generation tool from the Space
        self.image_generator = BaseSmolTool.from_space(
            "black-forest-labs/FLUX.1-schnell",
            name="image_generator",
            description="Generate an image from a text prompt."
        )
    
    def forward(self, destination: str) -> Any:
        # Create a detailed prompt for the image generator
        prompt = f"A beautiful, photorealistic travel photo of {destination}, showing iconic landmarks and scenery, high resolution, professional travel photography"
        
        try:
            # Generate the image
            image_path = self.image_generator(prompt)
            
            # Return as an AgentImage with additional context
            return {
                "image": AgentImage(image_path),
                "destination": destination,
                "prompt": prompt
            }
        except Exception as e:
            # Return error message if image generation fails
            return f"Could not generate image for {destination}: {str(e)}"