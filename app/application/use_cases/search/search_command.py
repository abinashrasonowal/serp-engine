from dataclasses import dataclass


@dataclass
class SearchCommand:
    """Command object for search use case."""
    query: str
    max_results: int = 10

    def __post_init__(self):
        if not self.query or not self.query.strip():
            raise ValueError("Query cannot be empty")
        if self.max_results < 1:
            raise ValueError("max_results must be at least 1")
