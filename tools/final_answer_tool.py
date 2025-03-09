from typing import Any, Optional
from smolagents.tools import Tool
from smolagents.agent_types import AgentImage

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides the final comprehensive travel information to the user."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer to return to the user. Can be text or include images.'}}
    output_type = "any"

    def __init__(self):
        super().__init__()

    def forward(self, answer: Any) -> Any:
        # Handle image dictionary from GenerateDestinationPreviewTool
        if isinstance(answer, dict) and 'image' in answer and isinstance(answer['image'], AgentImage):
            image = answer['image']
            destination = answer.get('destination', 'destination')
            
            # Return both the image and a descriptive caption
            caption = f"✨ Visual preview of {destination} ✨"
            return f"{caption}\n\n{image.to_string()}"
        
        # Check if the answer is an image path
        elif isinstance(answer, str) and ('/tmp/gradio/' in answer or answer.endswith(('.png', '.jpg', '.jpeg', '.webp'))):
            # Return as AgentImage for proper handling
            return AgentImage(answer)
            
        # Format text answers for better readability (keep existing behavior)
        elif isinstance(answer, str):
            if "Travel summary" not in answer and "Detailed travel information" not in answer:
                # Add structure if not already present
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