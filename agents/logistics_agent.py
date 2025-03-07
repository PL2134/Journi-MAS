from smolagents import CodeAgent
from typing import Dict, List, Optional, Any

class LogisticsAgent(CodeAgent):
    """
    The Logistics Agent specializes in practical travel logistics information.
    
    It manages time, weather, visa requirements, and currency conversion to help
    travelers with the practical aspects of planning and navigating their journeys.
    """
    
    def __init__(
        self,
        model,
        tools=None,
        managed_agents=None,
        prompt_templates=None,
        planning_interval=None,
        max_steps=4,
        verbosity_level=1,
        name="Logistics Agent",
        description="Manages practical travel logistics information",
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
        You are the Logistics Agent for Journi, a multi-agent travel assistant system.
        Your expertise is in providing practical travel logistics information.
        
        When given a task from the Coordinator Agent, you should:
        1. Check local times in travel destinations to help with planning
        2. Provide weather forecasts with packing recommendations
        3. Research visa requirements for international travel
        4. Convert currencies to assist with travel budgeting
        5. Organize information in a practical, actionable format
        
        Focus on accuracy and clarity. Travelers rely on your information for
        critical planning decisions, so always include appropriate disclaimers
        about checking official sources for the most up-to-date information,
        especially for visa and entry requirements.
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
