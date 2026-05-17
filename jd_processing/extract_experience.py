import re
import json

experience_pattern = r"(\d{1,2}|\d{1,2}[ \t]*(?:to|\-)[ \t]*\d{1,2})\+?[ \t]+(?:year[s]?)[ \t]*(?:of[ \t]+experience|experience)?"
experience_regex = re.compile(experience_pattern, re.IGNORECASE)

def extract_jd_experience(experience_text:str)->tuple:
    """Takes raw text containing experience and outputs a tuple (minimum, preferred)
    where minimum is the minimum experience required and preferred is the preferred minimum"""
    matches = experience_regex.finditer(experience_text)
    minimum = 0
    preferred = 0
    for match in matches:
        match = re.sub(r"\s", "", match.group(1))
        if "-" in match:
            l, u = match.split("-")
            minimum += int(l)
            preferred += int(u)
        else:
            minimum += int(match)
            preferred += int(match)
    return minimum, preferred


if __name__ == "__main__":
    with open("demo.json", "r") as fp:
        sectioned_database = json.load(fp)

    demo_text = sectioned_database["experience"]
    print(extract_jd_experience(demo_text))