from smolagents import CodeAgent
from typing import Dict, List, Optional, Any

class InformationRetrievalAgent(CodeAgent):
    """
    The Information Retrieval Agent is specialized in finding and extracting
    relevant travel information from the web.
    
    It uses web search and webpage visiting tools to gather factual information,
    reviews, recommendations, and other travel-related data.
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
        name="Information Retrieval Agent",
        description="Finds and extracts relevant travel information from the web",
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
        You are the Information Retrieval Agent for Journi, a multi-agent travel assistant system.
        Your expertise is in finding and extracting relevant travel information from the web.
        
        When given a task from the Coordinator Agent, you should:
        1. Formulate effective search queries to find relevant information
        2. Visit webpages to extract detailed content when necessary
        3. Analyze and summarize the information found, focusing on travel relevance
        4. Provide factual, up-to-date information with proper citations
        5. Structure your response in a way that's easy for the Coordinator to integrate
        
        Focus on finding high-quality, reliable information from multiple sources when possible.
        Always organize your findings clearly with appropriate sections like "Attractions",
        "Best Time to Visit", "Local Transportation", etc.
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
