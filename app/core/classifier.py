import logging
import os

from transformers import pipeline

logger = logging.getLogger(__name__)

# Same zero-shot setup as the baseline youarebot-classifier: ask the model whether
# a message reads as written by a "bot" or a "human" and take the "bot" score.
MODEL_NAME = os.getenv("MODEL_NAME", "typeform/distilbert-base-uncased-mnli")
CANDIDATE_LABELS = ["bot", "human"]
HYPOTHESIS_TEMPLATE = "This message was written by a {}."

_classifier = None


def load_model():
    """Load the text-classification model once and reuse it on later calls."""
    global _classifier
    if _classifier is None:
        logger.info("Loading text-classification model '%s'...", MODEL_NAME)
        _classifier = pipeline(
            "zero-shot-classification",
            model=MODEL_NAME,
            device=-1,
        )
    return _classifier


def classify_message(text: str) -> float:
    """Probability in [0, 1] that `text` was written by a bot."""
    classifier = load_model()
    result = classifier(
        text,
        candidate_labels=CANDIDATE_LABELS,
        hypothesis_template=HYPOTHESIS_TEMPLATE,
    )
    scores = dict(zip(result["labels"], result["scores"]))
    return max(0.0, min(1.0, float(scores["bot"])))
