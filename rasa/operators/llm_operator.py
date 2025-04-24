# rasa/operators/llm_operator.py
from rasa.llm.llm_client import call_llm
class LLMOperator:
    @staticmethod
    def run(input_text, **kwargs):
        """
        Calls the current configured LLM with the given input and returns the response.
        Extra kwargs (like temperature, max_tokens) are passed through.
        """
        return call_llm(input_text, **kwargs)
