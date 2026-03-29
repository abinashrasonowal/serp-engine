from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager

class IBrowser(ABC):
    @asynccontextmanager
    @abstractmethod
    async def get_session(self, headless: bool = True) -> AsyncGenerator[Any, None]:
        """Get a browser context session."""
        pass

    @abstractmethod
    async def create_page(self, context: Any) -> Any:
        """Create a new page in the given context."""
        pass

    @abstractmethod
    async def human_delay(self, min_s: float = 1.0, max_s: float = 3.0):
        """Introduce a randomized delay."""
        pass

    @abstractmethod
    async def natural_scroll(self, page: Any, element: Any):
        """Scroll to an element naturally."""
        pass

    @abstractmethod
    async def natural_click(self, page: Any, element: Any):
        """Click an element naturally (with mouse movement)."""
        pass
