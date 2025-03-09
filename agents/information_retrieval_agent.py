from smolagents import CodeAgent
from typing import Dict, List, Optional, Any
from smolagents.agent_types import AgentImage

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
        
        # Add specialized agent prompt with image generation guidance
        self.system_prompt_extension = """
        You are the Information Retrieval Agent for Journi, a multi-agent travel assistant system.
        Your expertise is in finding and extracting relevant travel information from the web and generating visual previews of destinations.
        
        When given a task from the Coordinator Agent, you should:
        1. Formulate effective search queries to find relevant information
        2. Visit webpages to extract detailed content when necessary
        3. Analyze and summarize the information found, focusing on travel relevance
        4. Provide factual, up-to-date information with proper citations
        5. Structure your response in a way that's easy for the Coordinator to integrate
        
        IMPORTANT FOR IMAGE GENERATION TASKS: 
        When asked to "Generate an image" of any destination:
        1. Use the generate_destination_preview tool with the destination name
        2. Do not process or modify the result - return the raw output directly
        3. Do not add any explanatory text or description - just return the image path
        4. Use this exact format:
           ```python
           image_path = generate_destination_preview(destination="Japan")
           return image_path
           ```
        
        For all other tasks, focus on finding high-quality, reliable information from multiple sources when possible.
        Always organize your findings clearly with appropriate sections like "Attractions",
        "Best Time to Visit", "Local Transportation", etc.
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
        else:
            if not prompt_templates:
                prompt_templates = {}
            prompt_templates["system_prompt"] = self.system_prompt_extension
            self.prompt_templates = prompt_templates