import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from src.schemas import YesNoAnswer, NumberAnswer


load_dotenv()

model = init_chat_model(
    model = os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_URL_BASE"),
    model_provider="openai",
    temperature=0,
)

model_yes_no = model.with_structured_output(YesNoAnswer)
model_number = model.with_structured_output(NumberAnswer)