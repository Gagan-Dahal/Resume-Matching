import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import json

nlp = spacy.load("en_core_web_lg")

skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

sections = {}
with open("demo.json", "r") as fp:
    sections = json.load(fp)

annotations = skill_extractor.annotate(sections['skills'])
def get_skills(annotations):
    skills = set()

    for match in annotations["results"]["full_matches"]:
        skills.add(match["doc_node_value"].lower())

    for match in annotations["results"]["ngram_scored"]:
        if match["score"] >= 0.8:
            skills.add(match["doc_node_value"].lower())

    return skills

skills = get_skills(annotations)
print("Skills found:", skills)