from typing import Any, Optional
from smolagents.tools import Tool

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides the final comprehensive travel information to the user."
    inputs = {'answer': {'type': 'string', 'description': 'The final answer to return to the user.'}}
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, answer: str) -> str:
        # Format the answer for better readability
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
        
        return answer  # Return as is if already formatted
