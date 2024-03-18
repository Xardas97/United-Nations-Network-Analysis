from enum import Enum

CERTIFICATE_PATH = "ca-root.pem"
SUBJECTS_FILE_PATH = "subjects.txt"
EXPECTED_RECORD_COUNTS_FILE_PATH = "expected_record_counts.txt"

DATA_FOLDER_PATH = "../data"
RECORDS_TABLE_PATH = DATA_FOLDER_PATH + "/records.csv"
RECORDS_PER_YEAR_TABLE_PATH = DATA_FOLDER_PATH + "/records-{}.csv"

BASE_URL = "https://digitallibrary.un.org"
BASE_SEARCH_URL = BASE_URL + "/search?cc=Voting Data"
RECORD_URL = BASE_URL + "/record/{}"

RECORDS_PER_PAGE = 50

RECORD_TABLE_HEADER = "ID,Body,Title,Date,Resolution,Subjects,Voting Data"
RECORD_TABLE_FORMAT = "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\""

class ParamTag(str, Enum):
   BODY = "fct__2"
   VOTE = "fct__9"
   SUBJECT = "fct__8"
   DATE = "fct__3"
   FIRST_RECORD = "jrec"
   PER_PAGE = "rg"

class ParamBody(str, Enum):
   GENERAL_ASSEMBLY = "General Assembly"
   SECURITY_COUNCIL = "Security Council"

class ParamVote(str, Enum):
   YES = "Vote"
   NO = "Without Vote"

class RecordRegex(str, Enum):
   TITLE = '^Title\\s*$'
   DATE = '^(Vote date|Date)\\s*$'
   RESOLUTION = '^Resolution\\s*$'
   NOTE = '^Note\\s*$'
   VOTING_DATA = '^Vote\\s*$'

class SearchResultRegex(str, Enum):
   SUBJECT_CHECKBOX = '^desktopcheckbox(1|2)-fct__8'
