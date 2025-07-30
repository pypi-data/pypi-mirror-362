from typing import List
from typing import Dict
from typing import Optional
from typing import List
from pathlib import Path
from deckgen.decks.anki_utils import generate_note
from deckgen.decks.anki_utils import get_anki_qa_model
from deckgen.decks.anki_utils import generate_deck
import genanki


class Deck:

    def __init__(self, name: str, description: Optional[str] = None):
        """
        Initializes a Deck with a name and an optional description.

        :param name: The name of the deck.
        :param description: An optional description of the deck.
        """
        self.name = name
        self.description = description if description is not None else ""
        self.cards: List[Card] = []

    def list_cards(self) -> List[Dict[str, str]]:
        """
        Lists all cards in the deck.

        :return: A list of dictionaries representing the cards in the deck.
                 Each dictionary contains 'front' and 'back' keys.
        """
        return [
            {"front": card.get_front(), "back": card.get_back()} for card in self.cards
        ]

    def add_card(self, card: "Card"):
        """
        Adds a card to the deck.

        :param card: The Card object to be added to the deck.
        """
        self.cards.append(card)

    def generate_anki_deck(self, filename: str) -> None:
        """
        Generates an Anki deck file from the current deck.

        :param filename: The name of the output file.
        :return: None
        """
        anki_model = get_anki_qa_model()
        notes = []
        for card in self.list_cards():
            note = generate_note(card["front"], card["back"], anki_model)
            notes.append(note)

        deck = generate_deck(notes, self.name, 2059400111)
        valid_filename = self._get_valid_filename(filename)
        genanki.Package(deck).write_to_file(valid_filename)

    def _get_valid_filename(self, filename: str) -> str:
        """
        Returns a valid filename by replacing invalid characters with underscores.

        :param filename: The original filename.
        :return: A valid filename.
        """
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return Path(filename).with_suffix(".apkg").name


class Card:
    def __init__(self, front: str, back: str, tags: Optional[List[str]] = None):
        """
        Initializes a Card with a front and back.

        :param front: The front text of the card.
        :param back: The back text of the card.
        """
        self.front = front
        self.back = back
        self.tags = tags if tags is not None else []

    def get_front(self) -> str:
        """
        Returns the front text of the card.

        :return: The front text of the card.
        """
        return self.front

    def get_back(self) -> str:
        """
        Returns the back text of the card.

        :return: The back text of the card.
        """
        return self.back

    def get_tags(self) -> List[str]:
        """
        Returns the tags associated with the card.

        :return: List of tags associated with the card.
        """
        return self.tags
