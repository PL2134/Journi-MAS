# Journi - Your AI Travel Companion
# This agent helps travelers with destination information, local time, weather forecasts,
# currency conversion, language translation, and destination previews.

from smolagents import CodeAgent, HfApiModel, load_tool
import datetime
import yaml
import os

# Import all the tool classes from their respective files
from tools.final_answer import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from tools.generate_destination_preview import GenerateDestinationPreviewTool
from tools.get_local_time import GetLocalTimeTool
from tools.get_weather_forecast import GetWeatherForecastTool
from tools.convert_currency import ConvertCurrencyTool
from tools.translate_phrase import TranslatePhraseTool
from tools.get_visa_requirements import GetVisaRequirementsTool
from Gradio_UI import GradioUI

# ==================== AGENT SETUP ====================

# Initialize all tool instances
final_answer = FinalAnswerTool()
web_search = DuckDuckGoSearchTool(max_results=5)  # Limit results for better readability
visit_webpage = VisitWebpageTool()
generate_destination_preview = GenerateDestinationPreviewTool()
get_local_time = GetLocalTimeTool()
get_weather_forecast = GetWeatherForecastTool()
convert_currency = ConvertCurrencyTool()
translate_phrase = TranslatePhraseTool()
get_visa_requirements = GetVisaRequirementsTool()

# Model initialization
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,  # Balanced between creativity and accuracy
    model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud',  # Use the AWS endpoint
    custom_role_conversions=None,
)

# Load prompts
try:
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
except FileNotFoundError:
    # Create a basic template if file doesn't exist
    prompt_templates = {}
    print("Warning: prompts.yaml not found. Using default prompt templates.")

# Add travel companion specific instructions to the prompt templates
travel_agent_prompt = """
You are Journi, an AI travel companion designed to help travelers plan and navigate their journeys.
Your goal is to provide helpful, accurate information about destinations, local customs, and practical travel advice.

You have access to these capabilities:
1. Search for travel information online
2. Visit webpages to get detailed information
3. Provide vivid descriptions of travel destinations
4. Check local time at travel destinations
5. Provide weather forecasts for trip planning
6. Convert currencies for travel budgeting
7. Translate common travel phrases
8. Check visa requirements

When users ask about a destination, try to provide comprehensive information by combining multiple tools.
For example, if someone asks about Tokyo, consider providing the local time, weather, and a descriptive preview.

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
        web_search,
        visit_webpage,
        generate_destination_preview,
        get_local_time,
        get_weather_forecast,
        convert_currency,
        translate_phrase,
        get_visa_requirements,
    ],
    max_steps=8,                      # Increased to allow for more tool usage in a single query
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="Journi",
    description="Your AI travel companion",
    prompt_templates=prompt_templates
)

# Launch the UI
if __name__ == "__main__":
    print("✈️ Launching Journi - Your AI Travel Companion")
    print("Ask me about any destination, local time, weather, currency conversion, or travel phrases!")
    GradioUI(agent).launch()