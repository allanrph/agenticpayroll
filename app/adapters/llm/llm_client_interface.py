from abc import ABC, abstractmethod
from typing import Dict, Any


class ILLMClient(ABC):
    """Interface for LLM client implementations."""

    @abstractmethod
    async def run_crew_agent(
        self, role: str, instructions: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a single step of the payroll crew by calling the LLM with a specialized role.
        The LLM receives the full current state (data) and returns the modified state.
        """
        pass
