import pytest
import os
from pprint import pprint
from rara_tools.formatters import format_keywords
from tests.test_utils import read_json_file

ROOT_DIR = os.path.join("tests", "test_data", "formatter")
INPUT_KEYWORDS_FILE_PATH = os.path.join(ROOT_DIR, "keywords.json")

INPUT_KEYWORDS = read_json_file(INPUT_KEYWORDS_FILE_PATH)

def test_formatting_keywords_for_core():
    formatted_keywords = format_keywords(INPUT_KEYWORDS)
    assert formatted_keywords
    assert isinstance(formatted_keywords, dict)
