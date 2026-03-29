from abc import ABC, abstractmethod

class ISolver(ABC):
    @abstractmethod
    async def solve(self, site_key: str, url: str) -> str:
        """Solve the CAPTCHA and return the solution token."""
        pass
