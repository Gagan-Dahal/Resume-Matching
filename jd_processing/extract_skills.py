from resume_processing.extract_skills import get_skills_and_type
import json
import re

or_regex = re.compile(r"\bor\b")

sectioned_data = {}
skills_text = ""

def get_jd_skills(skills_text:str)->list:
    """This takes raw text mentioning skills and returns a list of lists. If a number of skills are enclosed in a list then, they are or separated and having one is enough. E.g. [[python, java, c++], sql] here, this is interpreted as either python or java or c++ but sql is compulsary"""
    lines = skills_text.strip().split("\n")
    required_skills = []
    for line in lines:
        or_present = or_regex.search(line)
        line_skills = get_skills_and_type(line)
        if or_present:
            required_skills.append(list(line_skills.keys()))
        else:
            required_skills.extend(list(line_skills.keys()))    
    return required_skills
    # print(required_skills)

if __name__ == "__main__":
    with open("demo.json", "r") as fp:
        sectioned_data = json.load(fp)

    skills_text = sectioned_data["skills"]
    required_skills = get_jd_skills(skills_text)
    print(required_skills)
