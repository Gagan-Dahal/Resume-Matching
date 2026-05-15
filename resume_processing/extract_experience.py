import json
import re
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime

EARLIEST_JOB_START = datetime.now().year - 50
CURRENT_DATETIME = datetime.now()

month = r"(?:january|february|march|april|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|0?[1-9]|1[0-2])"
year = r"\d{4}"
date_separators = r"[-/.]"
start_patterns = rf"""(?:
    {month}[ \t]*{date_separators}[ \t]*{year}
    |{year}[ \t]*{date_separators}[ \t]*{month}
    |{month}[ \t]*{year}
    |{year}[ \t]*{month}
    |(?<!\d){year}(?!\d)
)"""
current_words = r"(?:now|present|today|current)"
end_patterns = rf"(?:{start_patterns}|{current_words})"


range_separators = r"(?:-|to)"
range_patterns = rf"""(?:
    {start_patterns}[ \t]+{range_separators}[ \t]+{end_patterns}
)"""
conj_pat = re.compile(range_patterns, re.IGNORECASE|re.VERBOSE)


experience_pattern = r"(\d{1,2})\+?[ \t]+(?:year|years)[ \t]*(?:of[ \t]+experience|experience)?"


def parse_date(date_str:str):
    if not isinstance(date_str, str):
        raise TypeError(f"{type(date_str)} sent instead of str")
    if re.search(current_words, date_str, re.IGNORECASE):
        return datetime.now()
    try:
        parsed_date = parser.parse(date_str, fuzzy=True)
        if parsed_date.year >= EARLIEST_JOB_START and parsed_date.year<=CURRENT_DATETIME.year:
            return parsed_date
        else:
            return None
    except:
        return None
    

def calculate_experience(range_list:list):
    if not isinstance(range_list, list):
        raise TypeError(f"{type(range_list)} sent instead of list")
    
    parsed_ranges = []

    for list_range in range_list:
        dates = re.split(re.compile(rf"[ \t]*{range_separators}[ \t]*"), list_range, maxsplit=1)
        if len(dates) == 2:
            start_date = parse_date(dates[0])
            end_date = parse_date(dates[1])
            if not start_date or not end_date:
                continue
            if start_date > end_date:
                start_date, end_date = end_date, start_date


            print(f"{start_date.year}-{start_date.month}, {end_date.year}-{end_date.month}")
            parsed_ranges.append([start_date, end_date])
            
    parsed_ranges.sort(key = lambda x: x[0])

    total_experience_months = 0
    list_index = 0
    while list_index < (len(parsed_ranges) - 1):
        cur = parsed_ranges[list_index]
        nex = parsed_ranges[list_index+1]

        if cur[1] >= nex[0]:
            cur[1] = max(cur[1], nex[1])
            parsed_ranges.pop(list_index + 1)
        else:
            list_index += 1

    for parsed_range in parsed_ranges:
        start_date, end_date = parsed_range
        delta = relativedelta(end_date, start_date)
        print(delta)
        total_experience_months += delta.years * 12 + delta.months

    return total_experience_months // 12


def extract_experience(experience_text):
    matches = re.search(experience_pattern, experience_text, re.IGNORECASE)
    if matches:
        print("String Match")
        years = 0
        matches = re.finditer(experience_pattern, experience_text, re.IGNORECASE)
        for match in matches:
            years += int(match.group(1))
        return years
    else:
        print("Trying date match")
        finds = re.findall(string = experience_text, pattern = conj_pat)
        return calculate_experience(finds)

if __name__ == "__main__":
    with open("demo.json", "r") as fp:
        sectioned_database = json.load(fp)

    demo_text = sectioned_database["experience"]
    # print(demo_text)
    print(extract_experience(demo_text))


# print(calculate_experience(finds))

# nlp = spacy.load("en_core_web_lg")
# sectioned_database = ""



# doc = nlp(experience_raw.lower())

# for ent in doc.ents:
#     print(ent.text, "->", ent.label_)