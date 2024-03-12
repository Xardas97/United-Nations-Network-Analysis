import requests
from bs4 import BeautifulSoup

BASE_URL = "https://digitallibrary.un.org/search?ln=en&cc=Voting Data"

PAR_BODY = "fct__2"
PAR_VOTE = "fct__9"
PAR_SUBJECT = "fct__8"
PAR_DATE = "fct__3"

PAR_BODY_GA = "General Assembly"
PAR_BODY_SC = "Security Council"

PAR_VOTE_YES = "Vote"
PAR_VOTE_NO = "Without Vote"

PAR_SUBJECT_DECOLONIZATION = "DECOLONIZATION"
PAR_SUBJECT_HUMAN_RIGHT = "HUMAN RIGHTS ADVANCEMENT"
PAR_SUBJECT_DISARMAMENT = "DISARMAMENT--GENERAL AND COMPLETE"
PAR_SUBJECT_MIDDLE_EAST = "MIDDLE EAST SITUATION"

def crawl(body, vote, subject, date):
    url = build_url(body, vote, subject, date)

    source_code = requests.get(url)
    source_code_text = source_code.text

    soup_object = BeautifulSoup(source_code_text, 'html.parser')
    for line in soup_object.find_all('a', {'class': 'moreinfo'}, True, "Detailed record"):
        print(line)

def build_url(body, vote, subject, date):
    url = BASE_URL

    if body:
       url = add_param(url, PAR_BODY, body)

    if vote:
       url = add_param(url, PAR_VOTE, vote)

    if subject:
       url = add_param(url, PAR_SUBJECT, subject)

    if date:
       url = add_param(url, PAR_DATE, str(date))

    return url

def add_param(url, param_tag, param_value):
    return url + "&" + param_tag + "=" + param_value

crawl(PAR_BODY_GA, PAR_VOTE_YES, PAR_SUBJECT_MIDDLE_EAST, 2015)
