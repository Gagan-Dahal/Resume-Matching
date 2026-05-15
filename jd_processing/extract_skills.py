from resume_processing.extract_skills import get_skills_and_type
import json
import re

sectioned_data = {}
with open("demo.json", "r") as fp:
    sectioned_data = json.load(fp)


all_skills = sectioned_data["skills"]
lines = all_skills.strip().split("\n")


or_regex = re.compile(r"\bor\b")
required_skills = []
for line in lines:
    or_present = or_regex.search(line)
    line_skills = get_skills_and_type(line)
    if or_present:
        required_skills.append(list(line_skills.keys()))
    else:
        required_skills.extend(list(line_skills.keys()))    
print(required_skills)