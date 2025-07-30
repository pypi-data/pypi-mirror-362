__version__ = "1.0.0"

from .ollama_rich import OllamaRichClient
from .utils import models_table, model_info_table

__all__ = ["OllamaRichClient", "models_table", "model_info_table"]