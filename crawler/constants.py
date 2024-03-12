from enum import Enum

CERTIFICATE_PATH = "ca-root.pem"
SUBJECTS_FILE_PATH = "subjects.txt"

BASE_URL = "https://digitallibrary.un.org"
BASE_SEARCH_URL = BASE_URL + "/search?ln=en&cc=Voting Data"

class ParamTag(str, Enum):
   BODY = "fct__2"
   VOTE = "fct__9"
   SUBJECT = "fct__8"
   DATE = "fct__3"

class ParamBody(str, Enum):
   GENERAL_ASSEMBLY = "General Assembly"
   SECURITY_COUNCIL = "Security Council"

class ParamVote(str, Enum):
   YES = "Vote"
   NO = "Without Vote"
