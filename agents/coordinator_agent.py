from smolagents import CodeAgent
from smolagents.agents import AgentText
from typing import Dict, List, Optional, Any

class CoordinatorAgent(CodeAgent):
    """
    The Coordinator Agent is the main orchestrator of the multi-agent system.
    It's responsible for:
    1. Understanding the user's request
    2. Breaking it down into sub-tasks
    3. Delegating tasks to appropriate specialized agents
    4. Synthesizing responses into a coherent final answer
    """
    
    def __init__(
        self,
        model,
        tools=None,
        managed_agents=None,
        prompt_templates=None,
        planning_interval=None,
        max_steps=8,
        verbosity_level=1,
        name="Coordinator Agent",
        description="Orchestrates the travel planning process across specialized agents",
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
        
        # Add coordinator-specific initialization if needed
        self.system_prompt_extension = """
        You are the Coordinator Agent for Journi, a multi-agent travel assistant system.
        Your role is to understand the user's travel request, break it down into sub-tasks,
        and delegate these tasks to the appropriate specialized agents:
        
        1. Information Retrieval Agent - For web search and visiting webpages
        2. Language & Culture Agent - For translations and cultural information
        3. Logistics Agent - For time, weather, visas, and currency
        4. Recommendation Agent - For destination previews, accommodation options, and activity suggestions
        
        After receiving responses from these agents, synthesize them into a comprehensive,
        cohesive final answer that addresses all aspects of the user's request.
        
        Remember to:
        - Always start by analyzing what the user is asking for
        - Identify which specialized agents can help with different parts of the request
        - Delegate clear, specific tasks to each agent
        - Combine the responses into a well-structured, unified answer
        - Format the final response with appropriate sections and headings
        """
        
        if prompt_templates and "system_prompt" in prompt_templates:
            prompt_templates["system_prompt"] += self.system_prompt_extension
