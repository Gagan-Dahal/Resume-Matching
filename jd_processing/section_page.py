import re
import json

SECTION_HEADERS = {
    "summary": ["summary", "about the role", "about this role", "role overview", "job overview", "position overview", "about the position", "overview", "job summary"],

    "responsibilities": ["responsibilities", "duties", "what you will do", "what you'll do", "your responsibilities", "role responsibilities", "job duties"],

    "skills": ["skills", "technical skills", "competencies", "tools and technologies", "tech stack"],

    "optional_skills": ["optional skills", "nice to have", "good to have"],

    "education": ["education", "educational qualification", "educational qualifications", "academic background", "educational", "qualifications"],

    "experience": ["experience", "work experience", "professional experience"],

    "benefits": [ "benefits", "what we offer", "perks", "compensation", "salary", "what you get", "our benefits"],

    "about_company": ["about us", "about the company", "who we are", "company overview"]
}

headers = [val for sublist in SECTION_HEADERS.values() for val in sublist]
pre_suff = ["required", "preferred", "requirement", "requirements", "basic", "core", "minimum", "key"]

headers = [h.replace(" ", r"\ ") for h in headers]

section_regex = rf"""
    ^\s*
    (?:(?:{"|".join(pre_suff)})[ \t]*)?
    ({"|".join(headers)})
    [ \t]*
    (?:(?:{"|".join(pre_suff)})[ \t]*)?
    (?:\&[ \t]*\w+[ \t]*)?
    (?:[:-]|\s*$)
"""

compiled_section_regex = re.compile(section_regex, re.IGNORECASE|re.VERBOSE|re.MULTILINE)

# test_text = "About the company: Our company is highly reputed. \nRequired Experience: 5+ years as developer\nPreferred Skills\nDjango, FastAPI\nHTML, CSS, JavaScript, React\nSome more skills\nEducational Qualifications\nBachelors in Computer Science, Information Technology or related fields\nSalary: 100,000"


test_text = ""

with open("test.txt", "r") as fp:
    test_text = fp.read()


sectioned_text = {}

matches = list(re.finditer(compiled_section_regex, test_text))

for index, match in enumerate(matches):
    text_start = match.end()
    text_end = matches[index+1].start() if index < len(matches) - 1 else len(test_text)
    extracted_topic = match.group(1).lower()
    normalized_topic = extracted_topic if extracted_topic in SECTION_HEADERS.keys() else None
    if normalized_topic is None:
        for key, value in SECTION_HEADERS.items():
            if extracted_topic in value:
                normalized_topic = key
    sectioned_text[normalized_topic] = test_text[text_start: text_end]

# print(sectioned_text)

with open("demo.json", "w") as fp:
    json.dump(sectioned_text, fp, indent=4)