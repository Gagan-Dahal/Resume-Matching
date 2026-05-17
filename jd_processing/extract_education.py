import re
import json

level_capture = r"""(?:
    b\.?[ \t]?(?:sc|tech|e|s)|
    bachelor(?:s|'s)?[ \t]?(?:degree)?|
    m\.?[ \t]?(?:sc|tech|e|s|ba)|
    master(?:s|'s)?[ \t]?(?:degree)?|
    p\.?[ \t]?h\.?[ \t]?d|
    doctorate    
)\.?"""
connector_capture = r"[ \t]*(?:of|in|,|:)[ \t]*"
degree_capture = r"""
    [a-zA-Z \t]+?(?=[,\n\d]|$)
"""

connector_regex = re.compile(connector_capture, re.IGNORECASE)

education_extraction_regex = re.compile(rf"(?:{level_capture}[ \t]*{connector_capture}?|{level_capture}[ \t]+(?:and|\&)?[ \t]+{level_capture}[ \t]*{connector_capture}?)", re.IGNORECASE|re.VERBOSE)

field_extraction_regex = re.compile(rf"(?:({level_capture})[ \t]*{connector_capture}?({degree_capture})|({level_capture}[ \t]+(?:and|\&)?[ \t]+{level_capture})[ \t]*{connector_capture}?({degree_capture}))", re.IGNORECASE|re.VERBOSE)

related_regex = re.compile(r"\bor[ \t]+[a-zA-Z ]*(?:related|similar|relevant)[ \t]+\w?(?:field[s]?|subject[s]?)?\b")

or_regex = re.compile(r'\bor\b')


def rejoin_wrapped_lines(text: str) -> str:
    lines = text.splitlines()
    joined = []
    buffer = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            if buffer:
                joined.append(buffer)
                buffer = ""
            continue
        
        if buffer:
            buffer += " " + line
        else:
            buffer = line
        
        if re.search(r"[.!?]$", buffer) or re.match(r"^[*\-•]", line) and buffer != line:
            joined.append(buffer)
            buffer = ""
    
    if buffer:
        joined.append(buffer)
    
    return "\n".join(joined)


def get_jd_education(education_text:str)->list:    
    """Takes raw text mentioning education and reutrns a list of dictionaries of format 
    {"degree_type": like bachelors/masters, 
    "allowed_fields": [list of fields of degree like Computer Science; many fields mean or], 
    "related_allowed": True/Fase this confirms if other related fields are allowed or not}"""
    education_status = []
    education_text = rejoin_wrapped_lines(education_text)
    lines = education_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        degree_match = education_extraction_regex.search(line)
        if not degree_match:
            continue
        
        degree_type = degree_match.group(0)
        degree_type = connector_regex.sub("", degree_type)
        degree_type = degree_type.strip()

        field_text = line[degree_match.end():].strip()

        allowed_fields = []

        relevant_present = related_regex.search(field_text)
        relevant_allowed = False

        if relevant_present:
            relevant_allowed = True

            field_text = field_text[:relevant_present.start()].strip()
            field_text = or_regex.sub(",", field_text)
            
            allowed_fields = [field.strip() for field in field_text.split(",") if field.strip()]
        
        elif or_regex.search(field_text):
            splits = re.split(or_regex, field_text)
            for splited in splits:
                allowed_fields.extend([x.strip() for x in splited.split(",") if x.strip()])

        else:
            match = field_extraction_regex.search(line)
            allowed_fields = [x.group(2) or x.group(4) for x in match]
            allowed_fields = [x.strip() for x in allowed_fields]
            degree_type = match.group(1) or match.group(3)
            degree_type = degree_type.strip()

        education_status.append({
            "degree_type": degree_type,
            "allowed_fields": allowed_fields,
            "related_allowed": relevant_allowed
        })
    return education_status


if __name__ == "__main__":
    with open("demo.json", "r") as fp:
        sectioned_data = json.load(fp)

    education_text = sectioned_data["education"]
    required_quals = get_jd_education(education_text)
    print(required_quals)