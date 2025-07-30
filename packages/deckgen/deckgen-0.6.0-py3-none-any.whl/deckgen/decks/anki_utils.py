import genanki
from typing import List


def generate_note(question: str, answer: str, model: genanki.Model) -> genanki.Note:
    """
    Generates a genanki Note object from a question and answer.

    :param question: The question text.
    :param answer: The answer text.
    :param model: The genanki Model to use for the note.
    :return: A genanki.Note object.
    """
    return genanki.Note(model=model, fields=[question, answer])


def get_anki_qa_model() -> genanki.Model:
    """
    Gets a genanki Model for question-answer pairs.
    This model can be used to create Anki notes with questions and answers.
    """
    model_id = 1607392311
    model = genanki.Model(
        model_id,
        "Simple QA",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )
    return model


def generate_deck(
    notes: List[genanki.Note], deck_name: str, deck_id: int
) -> genanki.Deck:
    """
    Generates a genanki Deck from a list of notes.

    :param notes: A list of genanki.Note objects.
    :param deck_name: The name of the deck.
    :param deck_id: The unique identifier for the deck.
    :return: A genanki.Deck object containing the notes.
    """
    deck = genanki.Deck(deck_id, deck_name)
    for note in notes:
        deck.add_note(note)
    return deck
