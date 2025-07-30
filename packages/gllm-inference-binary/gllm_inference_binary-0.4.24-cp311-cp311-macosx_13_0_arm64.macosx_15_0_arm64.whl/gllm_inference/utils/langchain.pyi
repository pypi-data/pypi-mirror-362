from langchain_core.embeddings import Embeddings as Embeddings
from langchain_core.language_models import BaseChatModel as BaseChatModel
from typing import Any

def load_langchain_model(model_class_path: str, model_name: str, model_kwargs: dict[str, Any]) -> BaseChatModel | Embeddings:
    '''Loads the LangChain\'s model instance.

    Args:
        model_class_path (str): The path to the LangChain\'s Embeddings class, e.g. "langchain_openai.ChatOpenAI".
        model_name (str): The model name.
        model_kwargs (dict[str, Any]): The additional keyword arguments.

    Returns:
        BaseChatModel | Embeddings: The LangChain\'s model instance.
    '''
