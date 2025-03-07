# Journi - Multi-Agent Travel Assistant System
# This system coordinates multiple specialized agents to help travelers with 
# comprehensive travel planning and information gathering.
#
# The system consists of these specialized agents:
# 1. Coordinator Agent - Orchestrates workflow and delegates tasks
# 2. Information Retrieval Agent - Handles web search and webpage visits
# 3. Language & Culture Agent - Provides translations and cultural information
# 4. Logistics Agent - Manages time, weather, visas, and currency conversion
# 5. Recommendation Agent - Creates destination descriptions, accommodation recommendations, and activity suggestions

from smolagents import CodeAgent, HfApiModel, load_tool
import datetime
import yaml
import os
from Gradio_UI import GradioUI

# Tool imports
from tools.final_answer_tool import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from tools.generate_destination_preview import GenerateDestinationPreviewTool
from tools.get_local_time import GetLocalTimeTool
from tools.get_weather_forecast import GetWeatherForecastTool
from tools.convert_currency import ConvertCurrencyTool
from tools.translate_phrase import TranslatePhraseTool
from tools.get_visa_requirements import GetVisaRequirementsTool
from tools.search_accommodations import SearchAccommodationsTool

# ==================== SHARED MODEL SETUP ====================

def create_model():
    """Creates and returns a configured HfApiModel instance."""
    return HfApiModel(
        max_tokens=2096,
        temperature=0.5,  # Balanced between creativity and accuracy
        model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud',
        custom_role_conversions=None,
    )

# ==================== TOOL INITIALIZATION ====================

def initialize_tools():
    """Initialize all tools used by the agents."""
    return {
        'final_answer': FinalAnswerTool(),
        'web_search': DuckDuckGoSearchTool(max_results=5),
        'visit_webpage': VisitWebpageTool(),
        'generate_destination_preview': GenerateDestinationPreviewTool(),
        'get_local_time': GetLocalTimeTool(),
        'get_weather_forecast': GetWeatherForecastTool(),
        'convert_currency': ConvertCurrencyTool(),
        'translate_phrase': TranslatePhraseTool(),
        'get_visa_requirements': GetVisaRequirementsTool(),
        'search_accommodations': SearchAccommodationsTool(max_results=8),
    }

# ==================== PROMPT TEMPLATES ====================

def load_prompt_templates():
    """Load prompt templates from YAML file."""
    try:
        with open("prompts.yaml", 'r') as stream:
            prompt_templates = yaml.safe_load(stream)
    except FileNotFoundError:
        prompt_templates = {}
        print("Warning: prompts.yaml not found. Using default prompt templates.")
    
    # Add travel companion specific instructions to the prompt templates
    travel_agent_prompt = """
    You are part of Journi, a multi-agent AI travel companion system designed to help travelers plan and navigate their journeys.
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
    9. Search for real accommodation options with filters for budget, style, and location

    When users ask about a destination, try to provide comprehensive information by combining multiple tools.
    For example, if someone asks about Tokyo, consider providing the local time, weather, real accommodation search results, and a descriptive preview.

    Always be enthusiastic about travel while remaining practical and informative.
    Suggest off-the-beaten-path experiences when appropriate, but prioritize the specific information requested.
    """

    # Add the travel agent prompt to the existing templates
    if "system_prompt" in prompt_templates:
        prompt_templates["system_prompt"] = travel_agent_prompt + "\n\n" + prompt_templates.get("system_prompt", "")
    else:
        prompt_templates["system_prompt"] = travel_agent_prompt
    
    return prompt_templates

# ==================== MULTI-AGENT SYSTEM SETUP ====================

def create_multi_agent_system():
    """
    Create and configure the multi-agent system with specialized agents
    that work together to provide comprehensive travel assistance.
    """
    model = create_model()
    tools = initialize_tools()
    prompt_templates = load_prompt_templates()
    
    # Create specialized agents - following the documentation example
    web_agent = CodeAgent(
        model=model,
        tools=[tools['web_search'], tools['visit_webpage']],
        max_steps=3,
        name="Information Retrieval Agent",
        description="Finds and extracts relevant travel information from the web",
    )
    
    language_agent = CodeAgent(
        model=model,
        tools=[tools['translate_phrase']],
        max_steps=2,
        name="Language & Culture Agent",
        description="Provides language assistance and cultural context for travelers",
    )
    
    logistics_agent = CodeAgent(
        model=model,
        tools=[
            tools['get_local_time'], 
            tools['get_weather_forecast'],
            tools['get_visa_requirements'],
            tools['convert_currency']
        ],
        max_steps=4,
        name="Logistics Agent",
        description="Manages practical travel information",
    )
    
    recommendation_agent = CodeAgent(
        model=model,
        tools=[tools['generate_destination_preview'], tools['search_accommodations']],
        max_steps=3,
        name="Recommendation Agent",
        description="Creates destination descriptions, searches real accommodations, and suggests activities",
    )
    
    # Create coordinator agent with access to specialized agents as a list
    coordinator_agent = CodeAgent(
        model=model,
        tools=[tools['final_answer']],
        managed_agents=[web_agent, language_agent, logistics_agent, recommendation_agent],
        max_steps=5,
        name="Journi Coordinator",
        description="Your AI Travel Companion",
        prompt_templates=prompt_templates,
    )
    
    return coordinator_agent

# ==================== MAIN APPLICATION ====================

if __name__ == "__main__":
    print("✈️ Launching Journi - Multi-Agent AI Travel Companion")
    print("Ask me about any destination, real accommodation searches, local time, weather, currency conversion, or travel phrases!")
    
    # Create multi-agent system
    multi_agent_system = create_multi_agent_system()
    
    # Launch the UI
    GradioUI(multi_agent_system).launch()
