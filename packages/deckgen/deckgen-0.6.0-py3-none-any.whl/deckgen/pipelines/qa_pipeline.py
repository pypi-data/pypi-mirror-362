from deckgen.client.openai_client import OpenAIClient
from prompteng.prompts.parser import QAParser
from prompteng.prompts.templates import TOPIC_FINDER
from prompteng.prompts.templates import QUESTION_ASKING
from typing import Optional
from typing import List
from typing import Dict
import json


class QAToolKit:
    def __init__(
        self, input_text: Optional[str] = None, openai_api_key: Optional[str] = None
    ):
        self.input_text = input_text
        self.openai_client = OpenAIClient(api_key=openai_api_key)

    def _get_topics(self, text: Optional[str] = None) -> str:
        """
        Extracts topics from the input text.
        This is a placeholder for topic extraction logic.
        """
        if text is not None:
            self.input_text = text

        if not self.input_text:
            raise ValueError("No text provided for topic extraction.")

        topic_response = self.openai_client.request(
            method="POST",
            endpoint="responses",
            data=json.dumps(
                {
                    "model": "gpt-3.5-turbo",
                    "input": TOPIC_FINDER.replace("{{", "{")
                    .replace("}}", "}")
                    .format(text=self.input_text),
                }
            ),
        )

        if topic_response.status_code != 200:
            raise ValueError(f"Failed to extract topics: {topic_response.text}")

        topics = topic_response.json()["output"][0]["content"][0]["text"]
        return topics

    def _generage_qa_string(self, topics: str) -> str:
        """
        Generates a question-answer string based on the input text and identified topics.
        :param topics: A string containing the identified topics.
        """
        qa_response = self.openai_client.request(
            method="POST",
            endpoint="responses",
            data=json.dumps(
                {
                    "model": "gpt-4o-mini",
                    "input": QUESTION_ASKING.replace("{{", "{")
                    .replace("}}", "}")
                    .format(expertise=topics, text=self.input_text),
                }
            ),
        )

        qa_string = qa_response.json()["output"][0]["content"][0]["text"]
        return qa_string

    def generate_qa(self) -> List[Dict[str, str]]:
        """
        Generates a list of questions and answers based on the input text.
        :return: A list of dictionaries containing questions and their corresponding answers.
        """
        if not self.input_text:
            raise ValueError("No input text provided for question generation.")

        topics = self._get_topics(self.input_text)
        qa_string = self._generage_qa_string(topics)

        parser = QAParser(qa_string)
        qa_list = parser.parse()
        return qa_list
