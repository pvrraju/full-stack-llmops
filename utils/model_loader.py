"""
utils/model_loader.py
=====================
Centralised helper that instantiates a chat-based Large Language Model (LLM)
object used across the repo.  Abstracting the *provider* behind this class
avoids scattering API-specific code throughout the project and makes swapping
models as easy as changing one line of YAML.

Supported providers (out of the box):
• **OpenAI** – default; controlled via `OPENAI_API_KEY`.  
• **Groq** – experimental high-throughput chat completion endpoint; controlled
  via `GROQ_API_KEY`.

How provider selection works
---------------------------
1. When you create `ModelLoader(model_provider="openai")` (or omit the argument)
   the class trivially passes.
2. Internally we read `config/config.yaml` to fetch the model name for that
   provider so you can keep hard-coded strings out of your code.

Adding a new provider
---------------------
Subclassing `ModelLoader` isn’t necessary; just extend the `load_llm` method
with an `elif` block and—optionally—update the YAML schema to include model
parameters for the new provider.
"""
import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["openai"] = "openai"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model=model_name, api_key=openai_api_key)
        
        return llm
    