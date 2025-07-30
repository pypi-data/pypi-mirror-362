from typing import List
from typing import Dict
from typing import Optional
import pandas as pd
import mlflow


class QAEvaluation:
    """
    Base class for question-answering evaluation.
    This class is intended to be extended by specific evaluation implementations.
    It provides a structure for evaluating question-answer pairs.
    """

    def __init__(
        self, input_text: str, qa_pairs: Optional[List[Dict[str, str]]] = None
    ) -> None:
        """
        Initializes the QAEvaluation with the provided input text.

        :param input_text: The text to be used for evaluation.
        """
        self.input_text = input_text
        self.qa_pairs = qa_pairs if qa_pairs is not None else []

    def basic_evaluation(self) -> List[Dict[str, str]]:
        """
        Performs a basic evaluation of the question-answer pairs.
        This method can be overridden by subclasses to provide specific evaluation logic.

        :return: A list of dictionaries containing the question and its corresponding answer.
        """
        with mlflow.start_run(run_name="Basic Evaluation"):
            mlflow.log_param("input_text", self.input_text)
            mlflow.log_param("qa_pairs", self.qa_pairs)

            # Basic evaluation logic can be implemented here
            evaluated_pairs = []
            for qa in self.qa_pairs:
                question = qa.get("question", "")
                answer = qa.get("answer", "")
                evaluated_pairs.append({"question": question, "answer": answer})

            mlflow.log_metric("evaluated_pairs_count", len(evaluated_pairs))
            return evaluated_pairs

    def evaluate(self) -> None:
        """
        Evaluates the question-answer pairs based on the input text.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def _build_static_dataset(self) -> List[Dict[str, str]]:
        """
        Builds a static dataset from the question-answer pairs.
        The keys for the dataset are "generated_question", "generated_answer", and "input_text".

        :return: A list of dictionaries containing the question and its corresponding answer.

        """
        static_dataset = pd.DataFrame(
            {
                "inputs": [qa.get("question", "") for qa in self.qa_pairs],
                "ground_truth": [qa.get("answer", "") for qa in self.qa_pairs],
            }
        )
        return self.qa_pairs if self.qa_pairs else [{"question": "", "answer": ""}]
