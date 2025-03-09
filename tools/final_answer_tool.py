from typing import Any, Optional
from smolagents.tools import Tool
from smolagents.agent_types import AgentImage
import re

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides the final comprehensive travel information to the user."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer to return to the user. Can be text or include images.'}}
    output_type = "any"

    def __init__(self):
        super().__init__()

    def forward(self, answer: Any) -> Any:
        # Direct handling for AgentImage objects
        if isinstance(answer, AgentImage):
            return answer
            
        # Handle image dictionary from image generation tools
        if isinstance(answer, dict) and 'image' in answer and isinstance(answer['image'], AgentImage):
            image = answer['image']
            destination = answer.get('destination', 'destination')
            
            # Return both the image and a descriptive caption
            caption = f"✨ Visual preview of {destination} ✨"
            return f"{caption}\n\n{image.to_string()}"
        
        # Check if answer contains both image path and destination information
        if isinstance(answer, str):
            # Look for image paths in the text
            image_path_match = re.search(r'(/tmp/gradio/[^\s\]]+\.(?:png|jpg|jpeg|webp))', answer)
            
            if image_path_match:
                image_path = image_path_match.group(1)
                
                # Try to extract destination from the text
                # First look for markdown format: ![Visual preview of Destination](path)
                destination_match = re.search(r'!\[Visual preview of ([^\]]+)\]', answer)
                if destination_match:
                    destination = destination_match.group(1)
                # Then look for "Welcome to Destination!" format
                elif "Welcome to " in answer:
                    welcome_match = re.search(r'Welcome to ([^!]+)!', answer)
                    if welcome_match:
                        destination = welcome_match.group(1).strip()
                else:
                    # Default if no destination found
                    destination = "this destination"
                
                # Create image with caption
                image = AgentImage(image_path)
                caption = f"✨ Visual preview of {destination} ✨"
                
                # Replace the image path/markdown with the proper image display
                modified_answer = answer.replace(image_path_match.group(0), "")
                # Also remove any markdown image syntax
                modified_answer = re.sub(r'!\[Visual preview of [^\]]+\]\([^)]+\)', "", modified_answer)
                
                # Remove multiple newlines
                modified_answer = re.sub(r'\n{3,}', '\n\n', modified_answer)
                
                return f"{caption}\n\n{image.to_string()}\n\n{modified_answer.strip()}"
            
            # Handle direct image paths
            elif answer.startswith('/tmp/gradio/') or answer.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Just create a generic caption for direct image paths
                image = AgentImage(answer)
                return image
            
            # Format text answers for better readability (keep existing behavior)
            elif "Travel summary" not in answer and "Detailed travel information" not in answer:
                # Your existing text formatting code
                sections = answer.split("\n\n")
                formatted_answer = "### Travel summary (short version):\n"
                
                if len(sections) > 0:
                    formatted_answer += sections[0] + "\n\n"
                
                formatted_answer += "### Detailed travel information:\n"
                if len(sections) > 1:
                    formatted_answer += "\n".join(sections[1:]) + "\n\n"
                
                formatted_answer += "### Practical tips and recommendations:\n"
                # Look for tips keywords in the answer
                tip_keywords = ["tip", "recommend", "bring", "pack", "don't forget", "suggestion"]
                tip_lines = []
                
                for line in answer.split("\n"):
                    if any(keyword in line.lower() for keyword in tip_keywords):
                        tip_lines.append(line)
                
                if tip_lines:
                    formatted_answer += "\n".join(tip_lines)
                else:
                    formatted_answer += "Safe travels! Remember to check local regulations and customs before your trip."
                
                return formatted_answer
        
        # Return the original answer for other types
        return answer