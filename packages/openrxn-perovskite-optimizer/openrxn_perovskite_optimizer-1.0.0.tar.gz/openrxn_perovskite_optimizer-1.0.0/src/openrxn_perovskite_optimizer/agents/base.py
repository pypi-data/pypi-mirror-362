from agents import Agent as OpenAIAgent

class Agent(OpenAIAgent):
    """Base agent for the OpenRXN platform"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handoff(self, agent_name: str, **kwargs):
        """Handoff to another agent"""
        return {
            "handoff_to": agent_name,
            "data": kwargs
        }