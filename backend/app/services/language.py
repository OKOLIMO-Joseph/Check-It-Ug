from langdetect import detect, DetectorFactory
from app.models.claim import Lang
import random

DetectorFactory.seed = 0

def detect_language(text: str) -> Lang:
    """Detect language and map to supported languages"""
    try:
        detected = detect(text)
        if detected == 'lg' or 'luganda' in text.lower():
            return Lang.lg
        elif detected == 'nyn' or 'runyankole' in text.lower():
            return Lang.nyn
        else:
            return Lang.en
    except:
        return Lang.en

language_names = {
    Lang.en: "English",
    Lang.lg: "Luganda",
    Lang.nyn: "Runyankole"
}