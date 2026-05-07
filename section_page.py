import re
import json

SECTION_HEADERS = {
    "summary": ["summary", "professional summary", "profile", "objective", "introduction", "additional information"],
    "skills": ["skills", "technical skills", "core competencies"],
    "education": ["education", "educational qualification", "qualification", "academic background"],
    "certifications": ["certifications", "certificates", "licenses", "training"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "projects": ["projects", "academic projects", "side projects"],
}
headers = [val for sublist in SECTION_HEADERS.values() for val in sublist]

section_regex = re.compile(r"^\s*(" + "|".join(headers) + r")\s*:?\s*$", re.IGNORECASE|re.MULTILINE)

# test_text = "Hello this is Gagan Dahal\nWork Experience\nlasjdfla\nIntroduction\n- Worked as abcde\n- ABCDE\nSKILLS\nPython, Anaconda, King Cobra\nQualification: \nBachelors in Computer Engineering\nTrubhuwan University, Nepal\nMasters in Data Science\nHarvard University, USA"

test_text = ""

with open("test.txt", "r") as fp:
    test_text = fp.read()

sectioned_text = {}

matches = list(re.finditer(section_regex, test_text))
# print(matches)
for index, match in enumerate(matches):
    # print(match.start(), match.end(), match.groups(), match.group(0), match.group(1))
    text_start = match.end()
    text_end = matches[index+1].start() if index < len(matches) - 1 else len(test_text)

    sectioned_text[match.group(1).lower()] = test_text[text_start: text_end]

# print(sectioned_text)

# with open("demo.json", "w") as fp:

#     json.dump(sectioned_text, fp, indent=4)