import argparse
from deckgen.decks.generator import DeckGen
from deckgen.pipelines.qa_pipeline import QAToolKit
from deckgen.text_processor.reader import Reader
from prompteng.prompts.parser import QAParser
from typing import Optional
from dotenv import load_dotenv


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        prog="deckgen", description="Generate decks from text files."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: generate
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a deck from an input file."
    )
    generate_parser.add_argument(
        "--input-file",
        "-i",
        required=True,
        help="Path to the input file (e.g., .txt, .md). Defaults to input.txt",
    )
    generate_parser.add_argument(
        "--output",
        "-o",
        required=False,
        default="output.apkg",
        help='Directory to save the generated deck, by default "output.apkg"',
    )
    generate_parser.add_argument("--name", "-n", required=True, help="Name of the deck")

    
    args = parser.parse_args()

    if args.command == 'generate':
        print(f"Generating deck from {args.input_file} with name {args.name}")
        generate_deck_from_file(
            input_file=args.input_file,
            deck_name=args.name,
            dst=args.output,
            deck_description=None,  # Optional description can be added later
        )




def generate_deck_from_file(
    input_file: str,
    deck_name: str,
    dst: Optional[str] = None,
    deck_description: Optional[str] = None,
) -> None:
    """
    Generates a deck from the specified input file.

    :param input_file: Path to the input file.
    :param deck_name: Name of the deck to be generated.
    :param dst: Optional destination directory for the generated deck file. 
        If not provided, the deck will be saved in the current directory.
    :param deck_description: Optional description for the deck.
    """

    reader = Reader(input_file)
    content = reader.read()
    print("Content read from file:", content)

    deck_gen = DeckGen(input_text=content)
    deck = deck_gen.generate_deck(
        deck_name=deck_name, deck_description=deck_description
    )

    print("Generated Deck:", deck.name)
    if not dst:
        dst = "output.apkg"
    deck.generate_anki_deck(dst)

