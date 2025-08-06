import os 
from agents import AsyncOpenAi, OpenAIChatCompletionsModel,RunConfig
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY enviroment variable is set")

external_client = AsyncOpenAi(
    api_key = gemini_api_key,
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    client = external_client,
)


gemini_config = RunConfig(
    model = model,
    model_provider=external_client
)

