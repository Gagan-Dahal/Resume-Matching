import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import json

nlp = spacy.load("en_core_web_lg")

skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


def get_skills_and_type(skills_text:str)->list:
    annotations = skill_extractor.annotate(skills_text)
    skills = {}

    for match in annotations["results"]["full_matches"]:
        skills[match["doc_node_value"]] = SKILL_DB[match["skill_id"]]["skill_type"]

    for match in annotations["results"]["ngram_scored"]:
        skill_difficulty = SKILL_DB[match["skill_id"]]["skill_type"]
        threshold = 0.8 if skill_difficulty == "Hard Skill" else 0.5
        if match["score"] > threshold:
            skills[match["doc_node_value"]] = SKILL_DB[match["skill_id"]]["skill_type"]
    
    return skills

with open("demo.json", "r") as fp:
    sectioned_database = json.load(fp)

demo_text = sectioned_database["skills"]

skills = get_skills_and_type(demo_text)
print(skills)