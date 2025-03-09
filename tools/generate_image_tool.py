from typing import Any
from smolagents.tools import Tool
from smolagents.agent_types import AgentImage
from smolagents import Tool as SmolTool  # Different name to avoid conflict

class GenerateImageTool(Tool):
    name = "generate_image"
    description = "Generates an image of a travel destination or scene."
    inputs = {'prompt': {'type': 'string', 'description': 'Description of the image to generate, such as a destination name.'}}
    output_type = "image"

    def __init__(self):
        super().__init__()
        # Initialize the image generator from Space
        self.image_generator = SmolTool.from_space(
            "black-forest-labs/FLUX.1-schnell",
            name="image_generator",
            description="Generate an image from a text prompt."
        )
    
    def forward(self, prompt: str) -> Any:
        # Enhance the prompt for better results
        enhanced_prompt = f"A photorealistic travel photo of {prompt}, high quality, professional photography"
        
        try:
            # Generate the image and return the path directly
            image_path = self.image_generator(enhanced_prompt)
            return AgentImage(image_path)  # Return as AgentImage directly
        except Exception as e:
            return f"Error generating image: {str(e)}"