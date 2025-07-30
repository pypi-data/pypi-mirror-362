from deckgen.decks.generator import DeckGen
from deckgen.pipelines.qa_pipeline import QAToolKit
from deckgen.text_processor.reader import Reader
from prompteng.prompts.parser import QAParser
from dotenv import load_dotenv
from typing import List
import os

import genanki


def main():
    """
    Main function to run the DeckGen application.
    """
    # Load environment variables from .env file
    load_dotenv()
    reader = Reader("test.txt")
    content = reader.read()
    print("Content read from file:", content)
    deck_gen = DeckGen(input_text=content)
    deck = deck_gen.generate_deck(
        deck_name="Test Deck", deck_description="This is a test deck."
    )
    print("Generated Deck:", deck.name)
    deck.generate_anki_deck("azure_functions.apkg")
