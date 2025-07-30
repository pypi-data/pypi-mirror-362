"""## [JOTFORM API DOCS](https://www.api.jotform.com)"""

# pylint: disable=C0115, C0116, C0103
from abc import ABC
from datetime import datetime
from typing import Union, Dict, Optional
from urllib.parse import quote
from time import sleep
import requests
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError


class JotForm(ABC):
    debug = False
    def __init__(self, api_key, form_id, timeout=45):
        self.update_timestamp = datetime.now().timestamp()
        self.api_key = api_key
        self.form_id = form_id
        self.url = (
            "https://api.jotform.com/form/"
            + form_id
            + "/submissions?limit=1000&apiKey="
            + api_key
        )
        self.set_url_param("offset", "0")
        self.submission_ids = set()
        self.submission_data = {}
        self.updating_process = False
        self.submission_count = 0
        self.timeout = timeout
        self.update()

    def _print(self, text):
        if self.debug:
            print(text)

    def _set_get_submission_data(self, submissions: list) -> dict:
        submissions_dict = {}
        for i in submissions:
            submissions_dict[i["id"]] = JotFormSubmission(i, self.api_key)
        return submissions_dict

    def get_submission_ids(self) -> set:
        return self.submission_ids

    def _set_submission_ids(self) -> None:
        """This function sets the submission memory. It is used for easier for loop for submissions.
        It is called in the constructor, and time to time in other functions"""
        self.submission_ids = set()
        for _, value in self.submission_data.copy().items():
            self.submission_ids.add(value.id)

    def _set_submission_count(self) -> None:
        self.submission_count = len(self.submission_ids)

    def get_submission_data(self) -> dict:
        self.update()
        return self.submission_data

    def get_submission_count(self) -> int:
        return self.submission_count

    def get_submission_answers(self, submission_id: int) -> dict:
        """## Returns the answers of the submission by given submission id

        Args:
            submission_id (int):

        Returns:
            dict: answers of the submission
        """
        self.update()
        return self.submission_data[submission_id].answers

    def get_submission_by_request(self, submission_id: Union[str, int]) -> Optional[object]:
        """ ## This function gets the submission by request

        Args:
            submission_id (_type_): _description_

        Returns:
            Optional[object]: _description_
        """
        url = (
            f"https://api.jotform.com/submission/{submission_id}?apiKey={self.api_key}"
        )
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            return response["content"]
        return None

    def get_submission(self, submission_id: Union[int, str]) -> object:
        return self.submission_data[submission_id]

    def get_submissions(self) -> dict:
        return self.get_submission_data()

    def get_submission_by_text(
        self, text: str, text_answer: str
    ) -> Optional[object]:
        """ ## This function gets the submission by text and answer's text
            {
                "key": 1,
                "name": "userName",
                "answer": "John Doe",
                "type": "control_textbox",
                "text": "What is Your User Name",
            }
        Args:
            text (str): _description_
            text_answer (str): _description_

        Returns:
            Optional[object]: submission object if successful, None if not
        """
        for _, submission_object in self.submission_data.copy().items():
            answer = submission_object.get_answer_by_text(text)
            if answer and answer.get("answer") == text_answer:
                return submission_object
        return None

    def get_submission_by_name(
        self, name: str, name_answer: str
    ) -> Optional[object]:
        """ ## This function gets the submission by name and answer's name
            {
                "key": 1,
                "name": "userName",
                "answer": "John Doe",
                "type": "control_textbox",
                "text": "What is Your User Name",
            }
        Args:
            name (str): _description_
            name_answer (str): _description_

        Returns:
            Optional[object]: submission object if successful, None if not
        """
        for _, submission_object in self.submission_data.copy().items():
            answer = submission_object.get_answer_by_name(name)
            if answer and answer.get("answer") == name_answer:
                return submission_object
        return None

    def get_submission_by_key(
        self, key: Union[str, int], key_answer: str
    ) -> Optional[object]:
        """ ## This function gets the submission by key and answer's key
            {
                "key": 1,
                "name": "userName",
                "answer": "John Doe",
                "type": "control_textbox",
                "text": "What is Your User Name",
            }
        Args:
            key (Union[str, int]): _description_
            key_answer (str): _description_

        Returns:
            Optional[object]: submission object if successful, None if not
        """
        for _, submission_object in self.submission_data.copy().items():
            answer = submission_object.get_answer_by_key(key)
            if answer and answer.get("answer") == key_answer:
                return submission_object
        return None

    def get_answer_by_text(self, submission_id: Union[int, str], text: str) -> dict:
        try:
            return self.get_submission(submission_id).get_answer_by_text(text)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_text(text)

    def get_answer_by_name(self, submission_id: Union[int, str], name: str) -> dict:
        try:
            return self.get_submission(submission_id).get_answer_by_name(name)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_name(name)

    def get_answer_by_key(self, submission_id: Union[int, str], key: str) -> dict:
        try:
            return self.get_submission(submission_id).get_answer_by_key(key)
        except KeyError:
            self.update()
            return self.get_submission(submission_id).get_answer_by_key(key)

    def get_answer_by_id(self, submission_id: Union[int, str], key: str) -> dict:
        return self.get_answer_by_key(submission_id, key)

    def get_submission_answers_by_question(self, submission_id: Union[int, str]) -> dict:
        self.update()
        submission_answers = self.get_submission_answers(submission_id)
        submission_answers_by_question = {}
        for answer in submission_answers:
            submission_answers_by_question[answer["id"]] = answer["answer"]
        return submission_answers_by_question

    def get_submission_answers_by_question_id(self, submission_id) -> dict:
        self.update()
        submission_answers = self.get_submission_answers(submission_id)
        submission_answers_by_question_id = {}
        for answer in submission_answers:
            submission_answers_by_question_id[answer["id"]] = answer["answer"]
        return submission_answers_by_question_id

    def get_list_of_questions(self):
        """## jotform endpoint of form/{id}/questions

        ### Returns:
            - `object` or 'bool': questions list if successful, false if not
        """
        url = f"https://api.jotform.com/form/{self.form_id}/questions?apiKey={self.api_key}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            return response["content"]
        return None

    def delete_submission(self, submission_id):
        url = (
            f"https://api.jotform.com/submission/{submission_id}?apiKey={self.api_key}"
        )
        response = requests.delete(url, timeout=self.timeout)
        if response.status_code == 200:
            del self.submission_data[submission_id]
            return True
        return False

    def create_submission(self, submission):
        """## This function creates a submission in Jotform
        then sets the new submission to the submission data.

        ### Args:
            - `submission (pseudo sumbission dictionary)`:
               {
                    "submission[1]": "value",
                    "submission[2]": "value",
                    ...
               }

        ### Returns:
            - `bool` or 'string': new created submission's id if successful, false if not
        """
        url = f"https://api.jotform.com/form/{self.form_id}/submissions?apiKey={self.api_key}"
        response = requests.post(url, data=submission, timeout=self.timeout)
        if response.status_code == 200:
            response = response.json()
            _id = response["content"]["submissionID"]
            submission = self.get_submission_by_request(_id)
            self.set_new_submission(submission)
            return _id
        return False

    def create_submission_using_another(self, submission_data, submission_to_copy):
        """## This function creates a submission in Jotform
        then sets the new submission to the submission data.

        ### Args:
            - `submission_data (sumbission dictionary)`:
            contains name value pairs of the submission
            e.g:
               {
                    "data": "value",
                    "data2": "value",
                    ...
               }
            - submission_to_copy (JotFormSubmission): submission object to copy

        ### Returns:
            - `bool`: true if successful, false if not
        """
        data = {}
        questions = self.get_list_of_questions()
        for q in questions:
            name = questions[q]["name"]
            if name in submission_data:
                data[f"submission[{q}]"] = submission_data[name]
            else:
                answer = submission_to_copy.get_answer_by_name(name)["answer"]
                if answer:
                    data[f"submission[{q}]"] = answer
        return self.create_submission(data)

    def update_submission_answers_batch(
        self, submission_id: Union[int, str], answers: Dict[str, Union[int, str, list]]
    ) -> bool:
        """## This function updates multiple answers of the submission in a single batch request

        ### Args:
            - `submission_id (Union[int, str])`: Submission ID
            - `answers (Dict[str, Union[int, str, list]])`: Dictionary of field_id to answer

        ### Returns:
            - `bool`: True if successful, False if not
        """
        data = {}
        for field_id, answer in answers.items():
            if isinstance(answer, list):
                data[f"submission[{field_id}][]"] = answer
            else:
                data[f"submission[{field_id}]"] = answer
        url = f"https://api.jotform.com/submission/{submission_id}"
        response = requests.post(
            url,
            params={"apiKey": self.api_key},
            data=data,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            for field_id, answer in answers.items():
                self.submission_data[submission_id].set_answer(field_id, answer)
            return True
        return False

    def update_submission_answer(
        self, submission_id: Union[int, str], field_id: str, answer: Union[int, str]
    ) -> bool:
        """## This function updates the answer of the submission

        ### Args:
            - `submission_id (Union[int, str])`: _description_
            - `field_id (str)`: _description_
            - `answer (Union[int, str])`: _description_

        ### Returns:
            - `bool`: True if successful, False if not
        """
        if isinstance(answer, list):
            data = {f"submission[{field_id}][]": answer}
            response = requests.post(
                f"https://api.jotform.com/submission/{submission_id}",
                params={"apiKey": self.api_key},
                data=data,
                timeout=self.timeout,
            )
        else:
            query = f"submission[{field_id}]={answer}"
            url = f"https://api.jotform.com/submission/{submission_id}"
            url += f"?apiKey={self.api_key}&{query}"
            response = requests.post(url, timeout=self.timeout)
        if response.status_code == 200:
            self.submission_data[submission_id].set_answer(field_id, answer)
            return True
        return False

    def set_url_param(self, key: Union[str, int], value: Union[str, int]) -> None:
        """Sets the URL parameter.

        Available keys:
            - `apiKey`: Your JotForm API key for authentication.\n
            - `limit`: Specifies the maximum number of results to return.\n
            - `offset`: Specifies the number of results to skip before starting to return results.\n
            - `orderby`: Determines the field by which to sort the results.\n
            - `filter`: Applies a filter to the results based on specified criteria.\n
            - `search`: Searches for a specific term within the results.\n
            - `sort`: Specifies the sort order of the results (e.g., ascending or descending).\n
            - `fields`: Specifies which fields to include in the response.\n
            - `id`: Filters results by a specific ID.\n
            - `created_at`: Filters results based on their creation date.\n
            - `updated_at`: Filters results based on their last updated date.

        Args:
            key (str): The key to set in the URL.
            value (str): The value to set for the specified key.
        """
        value = str(value)
        base_url, params = self.url.split("?")
        if key in params:
            params = params.split("&")
            for i, param in enumerate(params):
                if key in param:
                    params[i] = key + "=" + value
            self.url = base_url + "?" + "&".join(params)
        else:
            self.url += "&" + key + "=" + value

    def sort_submission_data_by_id(self) -> None:
        """## Sorts the submission data by id
            No need to sort since it is already sorted by the API
            unless orderby is changed in the url for descending order
        """
        sorted_tuples = sorted(
            self.submission_data.copy().items(), key=lambda x: x[1].id, reverse=True
        )
        sorted_dict = {k: v for k, v in sorted_tuples}
        self.submission_data = sorted_dict

    def get_missing_submission_id(self) -> Optional[int]:
        """ ## This function gets the missing submission id

        Returns:
            Optional[int]: return the missing submission id if there is any
        """
        all_submission_ids = set(self.get_submission_ids())
        expected_submission_ids = set(range(1, self.submission_count + 1))
        missing_ids = expected_submission_ids - all_submission_ids
        if missing_ids:
            return missing_ids.pop()

    def _fetch_new_submissions(self, count, attempt: int = 0, max_attempts: int = 5) -> bool:
        """## It is already newest to oldest so we can request one query, and it should be enough

        Args:
            count (_type_): Fresh count of the submissions
            attempt (_type_, optional): Current number of attempts. Defaults to 0.
            max_attempts (_type_, optional): Maximum number of attempts. Defaults to 5.

        Returns:
            bool: True if updates, False if not
        """
        count = count - self.submission_count
        if count <= 0:
            return False
        limit = 1000 if count > 1000 else count
        self.set_url_param("limit", limit)
        self.set_url_param("orderby", "id")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            self.submission_data.update(
                self._set_get_submission_data(data["content"])
            )
            if len(data["content"]) < limit:
                self.set_global_data()
                return True
            elif limit >= 1000:
                self.set_url_param("offset", data["resultSet"]["offset"] + limit)
                sleep(0.33)
                return self._fetch_new_submissions(count - limit, attempt)
            self.set_global_data()
            return True

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                self._print(f"Request failed: {http_err} (429 Too Many Requests). Retrying with backoff...")
                if attempt < max_attempts:
                    sleep_time = 2 ** attempt
                    sleep(sleep_time)
                    return self._fetch_new_submissions(count + self.submission_count, attempt + 1)
            self._print(f"Request failed: {http_err}")
        except (RequestException, JSONDecodeError) as e:
            self._print(f"Request failed: {e}")
            if attempt < max_attempts:
                sleep(.666)
                return self._fetch_new_submissions(count + self.submission_count, attempt + 1)

        except KeyError as e:
            self._print(f"KeyError: {e}")

        return False

    def _fetch_updated_submissions(self, attempt: int = 0, max_attempts: int = 5) -> bool:
        """## This function gets the last updated data from the Jotform API.
            Aim of this function is to get last 1000 submissions sorted by updated_at.
            So that network traffic is less and we can get the most recent data.

        Args:
            attempt (_type_, optional): Current number of attempts. Defaults to 0.
            max_attempts (_type_, optional): Maximum number of attempts. Defaults to 5.

        Returns:
            bool: True if updates, False if not
        """
        self.set_url_param("limit", "1000")
        self.set_url_param("orderby", "updated_at")
        self.set_url_param("offset", "0")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            self.submission_data.update(
                self._set_get_submission_data(data["content"])
            )
            self.set_global_data()
            return True

        except (RequestException, JSONDecodeError) as e:
            self._print(f"Request failed: {e}")
            if attempt < max_attempts:
                sleep(.666)
                return self._fetch_updated_submissions(attempt + 1)

        except KeyError as e:
            self._print(f"KeyError: {e}")

        return False

    def set_global_data(self) -> None:
        self._set_submission_ids()
        self._set_submission_count()
        self._reset_url_params()

    def request_submission_by_case_id(self, case_id) -> Optional[object]:
        """
        Requests the submission by case id
        this function is used when the submission is not in the submission data
        """
        query = quote(f"""{{"q221:matches:answer":"{case_id}"}}""")
        url = f"https://api.jotform.com/form/{self.form_id}/submissions"
        url += f"?apiKey={self.api_key}&filter={query}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code != 200:
            return None
        _json = response.json()
        return _json

    def set_new_submission(self, submission) -> None:
        self.submission_data.update(self._set_get_submission_data([submission]))
        self.set_global_data()

    def get_form(self) -> Optional[object]:
        """
        Gets form data directly from Jotform so there is no data diffirence on this function.
        It is slow since we are requesting data from Jotform.

        Returns:
            Optional[object]: object if successful, None if not
        """
        url = f"https://api.jotform.com/form/{self.form_id}?apiKey={self.api_key}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def _fetch_submissions_count(self):
        form = self.get_form()
        if form:
            return int(form["content"]["count"])
        return 1

    def update(self, force: bool = False) -> bool:
        """ ## This function updates the data from the Jotform API
            It will look for a change in the submission count,
            updates the data accordingly unless force is True

        Args:
            force (bool, optional): If True, it will update all the submissions. Defaults to False.

        Returns:
            bool: True if updates, False if not
        """
        if not self.updating_process:
            self.updating_process = True
            now = datetime.now().timestamp()
            its_been = now - self.update_timestamp
            if its_been > 300 or force:
                # been more than 5 minutes so only pull the 100 posibly recently updated submissions
                self.update_timestamp = now
                self._fetch_updated_submissions()
            else:
                count = self._fetch_submissions_count()
                if count != self.submission_count:
                    # only pull the new submissions if there is a change in the submission count
                    self._fetch_new_submissions(count)
                else:
                    self.updating_process = False
                    self._print("[INFO] No new submissions.")
                    return False
            self._reset_url_params()
            self._print(f"[INFO] Update process is completed.\
                Last update was {int(its_been/60)} minutes ago.")
            self.updating_process = False
            return True
        self._reset_url_params()
        self._print("[INFO] Update process is already running.")
        return False

    def _reset_url_params(self) -> None:
        self.set_url_param("offset", "0")
        self.set_url_param("limit", "1000")
        self.set_url_param("orderby", "id")

    def get_user_data_by_email(self, email: str) -> Optional[object]:
        """ ## This function gets the user data by email address"""
        if not email:
            return None
        email = email.lower()
        self.update()
        submissions = []
        for _, submission in self.submission_data.copy().items():
            submission_object = self.get_submission(submission.id)
            email_objects = [i.lower() for i in submission_object.emails if i]
            if email in email_objects:
                submissions.append(submission_object)
        return submissions


class JotFormSubmission(ABC):
    # TODO seperate this class into another file
    """Base class for JotFormSubmission.
    Takes a submission object and creates a submission object from it.

    Args:
        ABC (_type_): parent class
    """

    def __init__(self, submission_object, api_key):
        self.api_key = api_key
        self.id = submission_object["id"]
        self.form_id = submission_object["form_id"]
        self.ip = submission_object["ip"]
        self.created_at = submission_object["created_at"]
        self.status = submission_object["status"]
        self.new = submission_object["new"]
        self.flag = submission_object["flag"]
        self.notes = submission_object["notes"]
        self.updated_at = submission_object["updated_at"]
        self.answers = submission_object["answers"]
        self._clear_answers()
        self.answers_arr = self.set_answers(self.answers)
        self.emails = self.get_emails()

    def set_answers(self, answers) -> list:
        """ ## This function sets the answers array

        Args:
            answers (_type_): _description_

        Returns:
            list: _description_
        """
        answers_arr = []
        if answers is None:
            return answers_arr
        for key, value in answers.items():
            name = None
            if "name" in value:
                name = value["name"]
            answer = None
            if "answer" in value:
                answer = value["answer"]
            _type = None
            if "type" in value:
                _type = value["type"]
            text = None
            if "text" in value:
                text = value["text"]
            file = None
            if "file" in value:
                file = value["file"]
            answers_arr.append(
                {
                    "key": key,
                    "name": name,
                    "answer": answer,
                    "type": _type,
                    "text": text,
                    "file": file,
                }
            )
        return answers_arr

    def _clear_answers(self) -> None:
        """Process of getting rid of unnecessary keys in the answers dictionary."""
        for _, answer in self.answers.items():
            if "maxValue" in answer:
                del answer["maxValue"]
            if "order" in answer:
                del answer["order"]
            if "selectedField" in answer:
                del answer["selectedField"]
            if "cfname" in answer:
                del answer["cfname"]
            if "static" in answer:
                del answer["static"]
            if "type" in answer and answer["type"] != "control_email":
                del answer["type"]
            if "sublabels" in answer:
                del answer["sublabels"]
            if "timeFormat" in answer:
                del answer["timeFormat"]

    def set_answer(self, answer_key: str, answer_value: str) -> None:
        """## sets answer value for the given answer id

        Args:
            answer_key (str): order integer of the answer
            answer_value (str): value you want to set for the answer
        """

        for i, answer in enumerate(self.answers_arr):
            if answer["key"] == answer_key:
                self.answers_arr[i]["answer"] = answer_value
        self.answers[answer_key]["answer"] = answer_value
        self.update_submission(self.id, answer_key, answer_value, self.api_key)

    def set_answer_by_text(self, answer_text: str, answer_value: str) -> None:
        """## sets answer value for the given answer text

        Args:
            answer_text (str): answer_text of the answer
            answer_value (str): value you want to set for the answer
        """
        for i, answer in enumerate(self.answers_arr):
            if answer["text"] == answer_text:
                self.answers_arr[i]["answer"] = answer_value
        self.get_answer_by_text(answer_text)["answer"] = answer_value
        answer_key = self.get_answer_by_text(answer_text)["key"]
        self.update_submission(self.id, answer_key, answer_value, self.api_key)

    def set_answer_by_name(self, answer_name: str, answer_value: str) -> None:
        """## sets answer value for the given unique answer name

        Args:
            answer_name (str): answer_name of the answer
            answer_value (str): value you want to set for the answer
        """
        for i, answer in enumerate(self.answers_arr):
            if answer["name"] == answer_name:
                self.answers_arr[i]["answer"] = answer_value
        self.get_answer_by_name(answer_name)["answer"] = answer_value
        answer_key = self.get_answer_by_name(answer_name)["key"]
        self.update_submission(self.id, answer_key, answer_value, self.api_key)

    def set_answer_by_key(self, answer_key: str, answer_value: str) -> None:
        """## sets answer value for the given unique answer key

        Args:
            answer_key (str): answer_key of the answer
            answer_value (str): value you want to set for the answer
        """
        for i, answer in enumerate(self.answers_arr):
            if answer["key"] == answer_key:
                self.answers_arr[i]["answer"] = answer_value
        self.get_answer_by_key(answer_key)["answer"] = answer_value
        self.update_submission(self.id, answer_key, answer_value, self.api_key)

    @classmethod
    def update_submission(cls, submission_id, key, value, api_key) -> None:
        """
        Triggers an update for a specific submission in JotForm.

        This method sends a POST request to the JotForm API to update a specific field
        in a submission with a given value.

        Args:
            submission_id (str): The ID of the submission to be updated.
            key (str): The key of the field to be updated.
            value (str): The new value to be set for the specified field.
            api_key (str): The API key to authenticate the request.

        Raises:
            ConnectionError: If the request to the JotForm API fails due to a connection error.

        Example:
            self.trigger_submission_update("1234567890", "status", "active", "your_api_key")
        """
        query = f"submission[{key}]={value}"
        url = f"https://api.jotform.com/submission/{submission_id}?apiKey={api_key}&{query}"
        try:
            requests.post(url, timeout=45)
        except ConnectionError:
            print(f"cannot trigger for {submission_id}")

    def get_answers(self) -> list:
        """## This function gets the answers array

        Returns:
            list: answers array
        """
        return self.answers_arr

    def get_answer_by_text(self, text: str) -> dict:
        """## This function gets the answer by text
         Sensetive to the text, if the text is not exactly the same, it will return None

        Args:
            - `text (str)`: text element to search for

        Returns:
            - `dict`: jotform return object
            {
                "key": "key",
                "name": "name",
                "answer": "answer",
                "type": "type",
                "text": "text",
                "file": "file"
            }
        """
        for answer in self.answers_arr:
            if answer["text"] and answer["text"].upper() == text.upper():
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                if isinstance(_answer["answer"], list) and len(_answer["answer"]) == 1:
                    _answer["answer"] = _answer["answer"][0]
                return _answer
        raise ValueError(f"Answer with text '{text}' not found")

    def get_answer_by_name(self, name: str) -> dict:
        for answer in self.answers_arr:
            if answer["name"] and answer["name"] == name:
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                if isinstance(_answer["answer"], list) and len(_answer["answer"]) == 1:
                    _answer["answer"] = _answer["answer"][0]
                return _answer
        raise ValueError(f"Answer with name '{name}' not found")

    def get_answer_by_key(self, key: str) -> dict:
        for answer in self.answers_arr:
            if answer["key"] and answer["key"] == key:
                _answer = answer.copy()
                if not answer["answer"]:
                    _answer["answer"] = None
                if isinstance(_answer["answer"], list) and len(_answer["answer"]) == 1:
                    _answer["answer"] = _answer["answer"][0]
                return _answer
        raise ValueError(f"Answer with key '{key}' not found")

    def get_emails(self) -> list:
        """ ## This function gets the emails from the answers array

        Returns:
            list: _description_
        """
        emails = []
        for answer in self.answers_arr:
            if "type" not in answer:
                continue
            if answer["type"] == "control_email":
                emails.append(answer["answer"])
        return emails

    def get_day_from_date(self, date) -> int:
        """Given parameter is expected to be YYYY-MM-DD hh:mm:ss"""
        now = datetime.now()
        return (now - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).days

    def get_store_number_from_store(self, store) -> str:
        """If store is in the format of 'store | store_number', return store_number."""
        return store.split(" | ")[0]

    def to_dict(self) -> dict:
        """## This function returns the submission object as a dictionary,
        recomendation use case is to inherit this function in your own to_dict call

        Returns:
            dict: _description_
        """
        return {
            "id": self.id,
            "form_id": self.form_id,
            "ip": self.ip,
            "created_at": self.get_day_from_date(self.created_at),
            "status": self.get_answer_by_text("STATUS")["answer"],
            "new": self.new,
            "flag": self.flag,
            "notes": self.notes,
            "updated_at": self.updated_at,
            "emails": self.get_emails(),
        }

    def turn_into_american_datetime_format(
        self,
        date: Union[str, Dict[str, str], datetime],
        cur_frmt: str = "%Y-%m-%d %H:%M:%S",
        end_frmt: str = "%m/%d/%Y %I:%M %p",
    ) -> str:
        if isinstance(date, dict):
            date = date.get("answer") or date.get("datetime")

        if isinstance(date, str):
            date = datetime.strptime(date, cur_frmt)

        if isinstance(date, datetime):
            return date.strftime(end_frmt)

        raise ValueError("Invalid date format")

    def text_to_html(self, text) -> Optional[str]:
        """Converts plain text to HTML format."""
        if not text:
            return None
        text = text.replace("\r\n", "<br>")  # Convert Windows-style line breaks
        text = text.replace("\n", "<br>")  # Convert Unix-style line breaks
        text = text.replace("\r", "<br>")  # Convert Mac-style line breaks
        paragraphs = text.split("<br><br>")  # Split the text into paragraphs

        html = ""
        for paragraph in paragraphs:
            html += "<p>" + paragraph + "</p>"
        return html

    def split_domain_from_email(self, email: str):
        """if @ in email, split and return the first part of the string

        Args:
            email (str): string with @ in it

        Returns:
            _type_: first half of an email address.
            e.g: 'test' from 'test@test.com'
        """
        if not email:
            return None
        elif "@" in email:
            return email.split("@")[0]
        else:
            return email

    def get_value(self, obj: Union[str, dict]) -> Optional[str]:
        """ ## This function gets the value from the object
            When you call this it wont raise an error which makes it the safer version of ["answer"]
            Example:
            self.get_value(self.get_answer_by_text("CASE"))
            self.get_answer_by_text("CASE")["answer"]

        Args:
            obj (Union[str, dict]): _description_

        Returns:
            Optional[str]: _description_
        """
        if isinstance(obj, str):
            return obj.strip()
        elif isinstance(obj, dict):
            if "answer" in obj:
                answer = obj["answer"]
                if isinstance(answer, list):
                    return answer[0]
                return answer
            elif len(obj) > 1:
                return obj
            elif len(obj) == 1:
                return next(iter(obj.values()))
        else:
            return None

    def tide_answer_for_list(self, answer: Union[list, dict]) -> str:        
        """## This function converts the answer to a string, gives commas for each answer `,`
        ### Output is like:
            * Answer 1, Answer 2, Answer 3
        Args:
            answer (Union[list, dict]): _description_

        Returns:
            str: _description_
        """
        string = ""
        if isinstance(answer, list):
            for i, value in enumerate(answer):
                if i == 0:
                    string += f"{value.title()}"
                else:
                    string += f", {value.title()}"
        elif isinstance(answer, dict):
            for i, value in enumerate(answer.items()):
                if i == 0:
                    string += f"{value[1].title()}"
                else:
                    string += f", {value[1].title()}"
        return string

    def answer_for_html(self, answer: Union[list, dict]) -> str:
        """## This function converts the answer to HTML format, gives breaks for each answer `<br>`
        ### Output is like:
            * Answer 1
            * Answer 2
            * Answer 3

        Args:
            answer (str or dict): answer to be converted to HTML

        Returns:
            str: HTML formatted string
        """
        html = ""
        if isinstance(answer, list):
            for i, value in enumerate(answer):
                if i == 0:
                    html += f"*{value.title()}"
                else:
                    html += f"<br>*{value.title()}"
        elif isinstance(answer, dict):
            for i, value in enumerate(answer.items()):
                if i == 0:
                    html += f"*{value[1].title()}"
                else:
                    html += f"<br>*{value[1].title()}"
        elif isinstance(answer, str):
            html = f"*{answer.title()}"
        elif answer is None:
            html = "*None"
        else:
            html = f"*{answer}"
        return html