import re
import json

level_capture = r"""(?:
    b\.?[ \t]?(?:sc|tech|e|s)|
    bachelor(?:s|'s)?|
    m\.?[ \t]?(?:sc|tech|e|s|ba)|
    master[s]?|
    p\.?[ \t]?h\.?[ \t]?d|
    doctorate    
)\.?"""

connector_capture = r"[ \t]*(?:of|in|,|:)[ \t]*"

degree_capture = r"""
    [a-zA-Z \t]+?(?=[,\n\d]|$)
"""


education_extraction_regex = re.compile(rf"(:?{level_capture}[ \t]*{connector_capture}?{degree_capture}|{level_capture}[ \t]+(?:and|\&)?[ \t]+{level_capture}[ \t]*{connector_capture}?{degree_capture})", re.IGNORECASE|re.VERBOSE)

def get_education(education_text:str)->list:
    matches = re.finditer(education_extraction_regex, education_text)
    qualifications = []
    for match in matches:
        qualifications.append(match.group(0))
    return qualifications

# test_text = "Bachelors in Computer Engineering, 2018, Masters in Data Science, 2021, PHD. in Cyberbio Engineering for Simulation of Human Neural Network\nBachelors in Business Studies, mba, b.tech in biomechanical engineering\nbachelors, data science\np.h.d., memory systems\nB.S & Masters: Computer Applications"

with open("demo.json", "r") as fp:
    sectioned_database = json.load(fp)

test_text = sectioned_database["education"]

educational_quals = get_education(test_text)
print(educational_quals)