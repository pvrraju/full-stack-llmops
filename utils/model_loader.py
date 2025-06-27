
import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config_loader import load_config
from langchain_openai import ChatOpenai
from langchain_groq import ChatGroq



class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
    
    def __getitem__ (self, key):
        return self.config[key]

    def load_config(self):

        print(f"Loading configuration from {self.config_path}")
        return {"config" : "data"}
    

class ModelLoader(BaseModel):
    model_provider: Literal["openai"] = "openai"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):

        """
        Load and return the LLM model
        """
        print("LLM loading")
        print(f"Loading model from provider: {self.model_provider}")

        if self.model_provider == "openai":
            print("Loading LLM from openai......")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenai( model = "o4-mini" , api_key = openai_api_key )
        
        elif self.model_provider == "groq":
            print("Loading LLM from groq......")
            openai_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq( model = model_name , api_key = groq_api_key )

        return llm