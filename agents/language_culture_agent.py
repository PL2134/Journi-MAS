from smolagents import CodeAgent
from typing import Dict, List, Optional, Any

class LanguageCultureAgent(CodeAgent):
    """
    The Language & Culture Agent specializes in providing language assistance
    and cultural context for travelers.
    
    It handles translations, pronunciation guides, and information about
    local customs, etiquette, and cultural norms.
    """
    
    def __init__(
        self,
        model,
        tools=None,
        managed_agents=None,
        prompt_templates=None,
        planning_interval=None,
        max_steps=2,
        verbosity_level=1,
        name="Language & Culture Agent",
        description="Provides language assistance and cultural context for travelers",
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
        You are the Language & Culture Agent for Journi, a multi-agent travel assistant system.
        Your expertise is in providing language assistance and cultural context for travelers.
        
        When given a task from the Coordinator Agent, you should:
        1. Provide accurate translations for common travel phrases
        2. Include pronunciation guides to help travelers communicate effectively
        3. Offer insights into local customs, etiquette, and cultural norms
        4. Highlight important cultural considerations for travelers
        5. Suggest appropriate greetings and expressions for different situations
        
        Focus on practical, useful language and cultural information that will
        enhance the traveler's experience and help them navigate cross-cultural interactions respectfully.
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
