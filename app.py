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
from smolagents import Tool as SmolTool  # Adding this for image generation
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

def create_coordinator_prompt_templates():
    """Create prompt templates with coordinator-specific instructions."""
    system_prompt = """
    You are the Coordinator Agent for Journi, a multi-agent AI travel companion system.
    Your role is to understand the user's travel request, break it down into sub-tasks,
    and delegate these tasks to the appropriate specialized agents.
    
    You have access to these specialized agents:
    1. information_retrieval_agent - For web search, visiting webpages, and generating travel images
    2. language_culture_agent - For translations and cultural information
    3. logistics_agent - For time, weather, visas, and currency
    4. recommendation_agent - For destination previews, accommodation searches, and activities
    
    IMPORTANT: To delegate a task to a managed agent, use this format:
    ```python
    result = information_retrieval_agent(task="Your detailed task description here")
    print(result)
    ```
    
    IMPORTANT: For image generation of destinations, use the information_retrieval_agent with a specific instruction:
    ```python
    image_result = information_retrieval_agent(task="Generate an image of [destination]")
    print(image_result)
    ```
    
    Your overall task is to:
    1. Analyze the user's request to determine what information they need
    2. Delegate appropriate tasks to the specialized agents using the correct format
    3. Combine the responses into a well-structured, comprehensive answer
    4. Use the final_answer tool to return the complete response to the user
    
    CRITICAL: When providing the final answer, you MUST use the final_answer tool inside a code block with the correct format:
    ```python
    comprehensive_answer = "Your detailed travel information here"
    final_answer(comprehensive_answer)
    ```<end_code>
    
    ALWAYS end your code blocks with ```<end_code> - this is essential to properly execute your code.
    NEVER try to provide a direct text response without using the final_answer tool in code.
    
    Remember to provide a thorough, enthusiastic response that covers all aspects of the user's travel query.
    """
    
    return {"system_prompt": system_prompt}

# ==================== MULTI-AGENT SYSTEM SETUP ====================

def create_multi_agent_system():
    """
    Create and configure the multi-agent system with specialized agents
    that work together to provide comprehensive travel assistance.
    """
    model = create_model()
    tools = initialize_tools()
    
    # Create specialized agents with corrected names matching what will be used in calls
    information_retrieval_agent = CodeAgent(
        model=model,
        tools=[tools['web_search'], tools['visit_webpage'], tools['generate_destination_preview']],  # Add this tool
        max_steps=3,
        name="information_retrieval_agent",
        description="Finds and extracts relevant travel information from the web and generates images",
    )
    
    language_culture_agent = CodeAgent(
        model=model,
        tools=[tools['translate_phrase']],
        max_steps=2,
        name="language_culture_agent",
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
        name="logistics_agent",
        description="Manages practical travel information",
    )
    
    recommendation_agent = CodeAgent(
        model=model,
        tools=[tools['generate_destination_preview'], tools['search_accommodations']],
        max_steps=3,
        name="recommendation_agent",
        description="Creates destination descriptions, searches real accommodations, and suggests activities",
    )
    
    # Create coordinator agent with custom prompt templates and managed agents
    prompt_templates = create_coordinator_prompt_templates()
    
    coordinator_agent = CodeAgent(
        model=model,
        tools=[tools['final_answer']],
        managed_agents=[information_retrieval_agent, language_culture_agent, logistics_agent, recommendation_agent],
        max_steps=8,
        name="Journi",
        description="Your AI Travel Companion",
        prompt_templates=prompt_templates
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
