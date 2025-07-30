# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import os
import unittest
from dotenv import load_dotenv
from crossmark_jotform_api.jotForm import JotForm, JotFormSubmission

load_dotenv()
api_key = os.getenv("JOTFORM_API_KEY")
form_id = os.getenv("JOTFORM_FORM_ID")


class TestSubmissions(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jotform = JotForm(api_key, form_id)
        # we need a testing environment with at least one submission
        first_submission = self.jotform.get_submissions()[0]
        self.submission = JotFormSubmission(first_submission, api_key)

    def test_set_answer_by_text(self):
        self.submission.set_answer_by_text("Full Name", "John Doe")
        self.assertEqual(self.submission.get_answer_by_text("Full Name"), "John Doe")
