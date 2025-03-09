# Journi - Multi-Agent Travel Assistant System
# This system coordinates multiple specialized agents to help travelers with 
# comprehensive travel planning and information gathering, with step-by-step display.

from smolagents import CodeAgent, HfApiModel, load_tool
import datetime
import yaml
import os
from Gradio_UI import GradioUI

# Tool imports - using the exact filenames available in the tools directory
from tools.final_answer_tool import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from tools.generate_image_tool import GenerateImageTool
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
        'generate_image': GenerateImageTool(),
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
    1. information_retrieval_agent - For web search and visiting webpages
    2. language_culture_agent - For translations and cultural information
    3. logistics_agent - For time, weather, visas, and currency
    4. recommendation_agent - For destination recommendations, accommodation searches, and activities
    
    You also have a direct tool:
    - generate_image - Creates a visual image of any destination or travel scene
    
    IMPORTANT: Your output should be step-by-step, showing progress at each stage. Each step should be
    self-contained and include your thought process before executing the code.
    
    When a user expresses interest in a destination, follow this step-by-step approach:
    
    STEP 1: Generate a destination image and gather key information
    - ALWAYS call the generate_image tool DIRECTLY with the exact destination name:
      ```python
      destination = "Brazil"  # Extract the exact destination from user query
      destination_image = generate_image(prompt=destination)
      print(f"Generated image of {destination}")
      ```
    
    STEP 2: Get weather information and visa requirements
    STEP 3: Get currency information and cultural information
    STEP 4: Get recommendations and create the final comprehensive answer
    
    For each step, use this format:
    ```python
    # STEP X: Brief description of what you're doing in this step
    print("Thought: Explain your reasoning and what you plan to do in this step...")
    
    # Your code for this particular step
    # Don't try to do everything at once - break it down
    
    # Print results to show progress
    print(result)
    
    # Use final_answer ONLY in the final step
    ```
    
    When creating the comprehensive answer in the final step, use clear formatting with proper spacing:
    
    ```python
    comprehensive_answer = f'''
    {str(destination_image)}
    
    ## Welcome to {destination}!
    
    Here's what you should know about visiting:
    
    {info}
    
    ### Weather Information:
    {weather}
    
    ### Visa Requirements:
    {visa_info}
    
    ### Currency:
    {currency_info}
    
    ### Cultural Information:
    {cultural_info}
    
    ### Top Destinations and Activities:
    {recommendations}
    
    {destination} is a wonderful place to visit with its vibrant culture, stunning landscapes, and warm hospitality. Enjoy your trip!
    '''
    
    final_answer(comprehensive_answer)
    ```
    
    For GENERAL queries about your capabilities, features, or non-destination topics, DO NOT generate images.
    
    IMPORTANT: To delegate a task to a managed agent, use this format:
    ```python
    result = information_retrieval_agent(task="Your detailed task description here")
    print(result)  # Always print the result to show progress
    ```
    
    REMEMBER: Show your progress step by step so the user can see what's happening at each stage.
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
    
    # Create specialized agents with correct tool assignments and increased verbosity
    information_retrieval_agent = CodeAgent(
        model=model,
        tools=[tools['web_search'], tools['visit_webpage']], 
        max_steps=3,
        verbosity_level=2,  # Increased verbosity to show thought process
        name="information_retrieval_agent",
        description="Finds and extracts relevant travel information from the web",
    )
    
    language_culture_agent = CodeAgent(
        model=model,
        tools=[tools['translate_phrase']],
        max_steps=2,
        verbosity_level=2,  # Increased verbosity to show thought process
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
        verbosity_level=2,  # Increased verbosity to show thought process
        name="logistics_agent",
        description="Manages practical travel information",
    )
    
    recommendation_agent = CodeAgent(
        model=model,
        tools=[tools['search_accommodations']],
        max_steps=3,
        verbosity_level=2,  # Increased verbosity to show thought process
        name="recommendation_agent",
        description="Creates destination descriptions and suggests activities",
    )
    
    # Create coordinator agent with custom prompt templates and managed agents
    prompt_templates = create_coordinator_prompt_templates()
    
    coordinator_agent = CodeAgent(
        model=model,
        tools=[tools['final_answer'], tools['generate_image']],
        managed_agents=[information_retrieval_agent, language_culture_agent, logistics_agent, recommendation_agent],
        max_steps=8,
        verbosity_level=2,  # Increased verbosity to show thought process
        name="Journi",
        description="Your AI Travel Companion",
        prompt_templates=prompt_templates
    )
    
    return coordinator_agent

# ==================== MAIN APPLICATION ====================

if __name__ == "__main__":
    print("✈️ Launching Journi - Multi-Agent AI Travel Companion")
    print("Ask me about any destination, local time, weather, currency conversion, or travel phrases!")
    
    # Create multi-agent system
    multi_agent_system = create_multi_agent_system()
    
    # Launch the UI
    GradioUI(multi_agent_system).launch()