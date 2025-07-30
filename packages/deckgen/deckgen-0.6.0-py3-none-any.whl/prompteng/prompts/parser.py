from typing import Optional
from typing import Dict
from typing import List
import re


class QAParser:

    def __init__(self, text: Optional[str]) -> None:
        """
        Initializes the QAParser with the provided text.

        :param text: The text to be parsed for questions and answers.
        """
        self.text = text

    def parse(self, text: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Parses the provided text to extract questions and answers.

        :param text: Optional text to parse. If not provided, uses the text initialized in the constructor.
        :return: A list of dictionaries containing questions and their corresponding answers.
        :raises ValueError: If no text is provided for parsing.
        :raises ValueError: If no valid question-answer pairs are found in the text.
        """
        if text is not None:
            self.text = text

        if not self.text:
            raise ValueError("No text provided for parsing.")

        # Regex pattern to match question-answer pairs (question ends with '?', answer follows)
        pattern = r"(?P<question>.*?\?)\s+(?P<answer>.*?)(?=\n\d+\.|\Z)"

        matches = re.finditer(pattern, self.text, re.DOTALL)
        qa_list = [
            {
                "question": m.group("question").strip(),
                "answer": m.group("answer").strip(),
            }
            for m in matches
        ]

        # Remove leading index (e.g., "1. ", "2. ") from each question in qa_list
        for qa in qa_list:
            qa["question"] = (
                qa["question"].lstrip().split(" ", 1)[-1]
                if qa["question"].lstrip()[0].isdigit() and "." in qa["question"]
                else qa["question"]
            )
            qa["answer"] = qa["answer"].strip()
        # Ensure that each question and answer is stripped of leading/trailing whitespace
        qa_list = [
            {"question": qa["question"].strip(), "answer": qa["answer"].strip()}
            for qa in qa_list
        ]
        # Ensure that the list is not empty
        if not qa_list:
            raise ValueError("No valid question-answer pairs found in the text.")
        return qa_list
