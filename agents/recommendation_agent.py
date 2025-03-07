from smolagents import CodeAgent
from typing import Dict, List, Optional, Any

class RecommendationAgent(CodeAgent):
    """
    The Recommendation Agent specializes in creating personalized travel
    recommendations and itineraries.
    
    It generates evocative destination descriptions, searches for real accommodations,
    and suggests activities, attractions, and experiences based on traveler preferences.
    """
    
    def __init__(
        self,
        model,
        tools=None,
        managed_agents=None,
        prompt_templates=None,
        planning_interval=None,
        max_steps=3,
        verbosity_level=1,
        name="Recommendation Agent",
        description="Creates destination descriptions, searches real accommodations, and suggests activities",
        **kwargs
    ):
        super().__init__(
            model=model,
            tools=tools,
            managed_agents=managed_agents,
            prompt_templates=prompt_templates,
            planning_interval=planning_interval,
            max_steps=max_steps,
            verbosity_level=verbosity_level,
            name=name,
            description=description,
            **kwargs
        )
        
        # Add specialized agent prompt
        self.system_prompt_extension = """
        You are the Recommendation Agent for Journi, a multi-agent travel assistant system.
        Your expertise is in creating personalized travel recommendations and itineraries.
        
        When given a task from the Coordinator Agent, you should:
        1. Generate vivid, evocative descriptions of destinations
        2. Search for real accommodation options based on traveler preferences
        3. Suggest activities, attractions, and experiences based on traveler preferences
        4. Create balanced itineraries that include popular highlights and off-the-beaten-path experiences
        5. Consider seasonal factors, local events, and optimal visiting times
        6. Tailor recommendations to different travel styles (luxury, budget, family, adventure, etc.)
        
        For accommodation searches and recommendations:
        - Use the search_accommodations tool to find real accommodation options
        - Provide filters for budget (budget, mid-range, luxury), accommodation style (hotel, hostel, resort, apartment), and location
        - When presenting accommodation options, highlight key features like location and amenities
        - Include a mix of accommodation types to give travelers diverse options
        - Provide context about neighborhoods and proximity to attractions when relevant

        Focus on providing authentic, memorable experiences that match the traveler's
        interests while being practical and achievable. Balance must-see attractions with
        hidden gems to create unique, personalized recommendations.
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
