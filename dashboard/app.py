from src.pos_tagging.pipeline_nltk import pipeline_nltk
from src.pos_tagging.pipeline_spacy import pipeline_spacy

nltk_pipeline = pipeline_spacy()

nltk_pipeline.ejecutar()