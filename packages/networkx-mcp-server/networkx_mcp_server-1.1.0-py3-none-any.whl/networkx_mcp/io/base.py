"""Base interfaces for graph I/O operations."""

import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import networkx as nx


class GraphReader(ABC):
    """Base class for graph file readers."""

    def __init__(self, format_name: str, file_extensions: list[str]):
        self.format_name = format_name
        self.file_extensions = file_extensions

    @abstractmethod
    async def read(self, filepath: str | Path, **options) -> nx.Graph:
        """Read a graph from file."""

    def validate_file(self, filepath: str | Path) -> bool:
        """Validate file can be read by this reader."""
        path = Path(filepath)
        return path.suffix.lower() in self.file_extensions


class GraphWriter(ABC):
    """Base class for graph file writers."""

    def __init__(self, format_name: str, file_extension: str):
        self.format_name = format_name
        self.file_extension = file_extension

    @abstractmethod
    async def write(self, graph: nx.Graph, filepath: str | Path, **options) -> bool:
        """Write a graph to file."""


def validate_file_path(filepath: str | Path, must_exist: bool = True) -> Path:
    """Validate and normalize file path."""
    path = Path(filepath)

    # Security: prevent directory traversal
    allowed_temp_dir = Path(tempfile.gettempdir())
    if ".." in str(path) or (path.is_absolute() and not path.is_relative_to(allowed_temp_dir)):
        msg = "Invalid file path - no directory traversal allowed"
        raise ValueError(msg)

    if must_exist and not path.exists():
        msg = f"File not found: {path}"
        raise FileNotFoundError(msg)

    if not must_exist:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

    return path


def detect_format(filepath: str | Path) -> str:
    """Detect graph format from file extension."""
    path = Path(filepath)
    extension = path.suffix.lower()

    format_map = {
        ".gml": "gml",
        ".graphml": "graphml",
        ".gexf": "gexf",
        ".edgelist": "edgelist",
        ".adjlist": "adjlist",
        ".json": "json",
        ".yaml": "yaml",
        ".csv": "csv",
    }

    return format_map.get(extension, "unknown")
