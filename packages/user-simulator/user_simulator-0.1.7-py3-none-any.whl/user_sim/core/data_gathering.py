import ast
import pandas as pd
from src.user_sim.utils.token_cost_calculator import calculate_cost, max_output_tokens_allowed, max_input_tokens_allowed
import re
from src.user_sim.utils.exceptions import *
from src.user_sim.utils.utilities import init_model
from src.user_sim.utils import config
from langchain_core.prompts import ChatPromptTemplate


model = " "
llm = None

import logging
logger = logging.getLogger('Info Logger')


def init_data_gathering_module():
    global model
    global llm
    model, llm = init_model()

def extract_dict(in_val):
    reg_ex = r'\{[^{}]*\}'
    coincidence = re.search(reg_ex, in_val, re.DOTALL)

    if coincidence:
        return coincidence.group(0)
    else:
        return None


def to_dict(in_val):
    try:
        dictionary = ast.literal_eval(extract_dict(in_val))
    except (BadDictionaryGeneration, ValueError) as e:
        logger.error(f"Bad dictionary generation: {e}. Setting empty dictionary value.")
        dictionary = {}
    return dictionary


class ChatbotAssistant:
    def __init__(self, ask_about):
        self.verification_description = "the following has been answered, confirmed or provided by the chatbot:"
        self.data_description = """"the piece of the conversation where the following has been answered 
                                or confirmed by the assistant. Don't consider the user's interactions:"""
        self.properties = self.process_ask_about(ask_about)
        self.system_message = """You are a helpful assistant that detects when a query in a conversation
                                has been answered, confirmed or provided by the chatbot."""
        self.messages = ""
        self.gathering_register = {}

    def process_ask_about(self, ask_about):
        properties = {
        }

        for ab in ask_about:
            properties[ab.replace(' ', '_')] = {
                "type": "object",
                "properties": {
                    "verification": {
                        "type": "boolean",
                        "description": f"{self.verification_description} {ab}"
                    },
                    "data": {
                        "type": ["string", "null"],
                        "description": f"{self.data_description} {ab} "
                    }
                },
                "required": ["verification", "data"],
                "additionalProperties": False
            }
        return properties

    def add_message(self, history):     # adds directly the chat history from user_simulator "self.conversation_history"
        text = ""
        for entry in history['interaction']:
            for speaker, message in entry.items():
                text += f"{speaker}: {message}\n"

        self.messages = text
        self.gathering_register = self.create_dataframe()

    def get_json(self):

        response_format = {
                "title": "data_gathering",
                "type": "object",
                "description": "The information to check.",
                "properties": self.properties,
                "required": list(self.properties.keys()),
                "additionalProperties": False
        }

        parsed_input_message = self.messages + self.verification_description + self.data_description

        if llm is None:
            logger.error("data gathering module not initialized.")
            return "Empty data"

        if max_input_tokens_allowed(parsed_input_message, model):
            logger.error(f"Token limit was surpassed")
            return None

        if config.token_count_enabled:
            llm.max_tokens = max_output_tokens_allowed(model)

        prompt = ChatPromptTemplate.from_messages([("system", self.system_message), ("human", "{input}")])
        structured_llm = llm.with_structured_output(response_format)
        prompted_structured_llm = prompt | structured_llm

        try:
            response = prompted_structured_llm.invoke({"input": self.messages})
            parsed_output_message = str(response)

        except Exception as e:
            logger.error(f"Truncated data in message: {e}")
            response = parsed_output_message = None
        if config.token_count_enabled:
            calculate_cost(parsed_input_message, parsed_output_message, model=config.model, module="data_extraction")
        return response

    def create_dataframe(self):
        data_dict = self.get_json()
        if data_dict is None:
            df = self.gathering_register
        else:
            try:
                df = pd.DataFrame.from_dict(data_dict, orient='index')
            except Exception as e:
                logger.error(f"{e}. data_dict: {data_dict}. Retrieving data frame from gathering_register")
                df = self.gathering_register
        return df

