from typing import Optional
from typing import List
from typing import Dict

from deckgen.decks.base import Deck
from deckgen.decks.base import Card
from deckgen.pipelines.qa_pipeline import QAToolKit
from deckgen.decks.anki_utils import generate_note
from deckgen.decks.anki_utils import get_anki_qa_model


class DeckGen:
    def __init__(self, input_text: Optional[str] = None):
        """
        Initializes the DeckGen class with the input text.

        :param input_text: The text input to generate a deck from.
        """
        self.input_text = input_text

    def generate_deck(
        self, deck_name: Optional[str], deck_description: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generates a deck based on the input text.
        :return: List of generated cards. Each card is a dictionary with 'front' and 'back' keys.
        """
        # Placeholder for deck generation logic
        qa_toolkit = QAToolKit(input_text=self.input_text)
        qa_list = qa_toolkit.generate_qa()
        deck = Deck(name=deck_name, description=deck_description)
        for qa in qa_list:
            card = Card(front=qa["question"], back=qa["answer"])
            deck.add_card(card)

        return deck
