# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import os
import unittest
from dotenv import load_dotenv
from crossmark_jotform_api.jotForm import JotForm

load_dotenv()
api_key = os.getenv('JOTFORM_API_KEY')
form_id = os.getenv('JOTFORM_FORM_ID')

class TestForms(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jotform = JotForm(api_key, form_id)

    def test_get_form(self):
        response = self.jotform.get_form()
        self.assertEqual(response.get('responseCode'), 200)
