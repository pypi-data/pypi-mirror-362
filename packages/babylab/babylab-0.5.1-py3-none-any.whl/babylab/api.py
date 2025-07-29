#!/usr/bin/env python

"""
Functions to interact with the REDCap API.
"""

from os import mkdir, walk
from os.path import join, exists
from collections import OrderedDict
from collections.abc import Iterable
import json
import zipfile
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import requests
from pandas import DataFrame


class MissingEnvException(Exception):
    """If .env file is not found in user folder"""

    def __init__(self, envpath):
        msg = f".env file not found. Please, make sure to save your credentials in {envpath}"  # pylint: disable=line-too-long
        super().__init__(msg)


class MissingEnvToken(Exception):
    """If token is not provided under 'API_TEST_TOKEN' key."""

    def __init__(self):
        msg = "No token was found under the 'API_TEST_TOKEN' key in your .env file."  # pylint: disable=line-too-long
        super().__init__(msg)


class RecordList:
    """List of records"""

    def __init__(self, records: dict):
        self.records: dict = records

    def __len__(self) -> int:
        return len(self.records)

    def __repr__(self) -> str:
        return f"RecordList with {len(self)} records"

    def to_df(self) -> DataFrame:
        """Transforms a a RecordList to a Pandas DataFrame.

        Returns:
            DataFrame: Tabular dataset.
        """
        df = DataFrame([p.data for p in self.records.values()])
        df.set_index("record_id", inplace=True)
        return df


def filter_fields(data: dict, prefix: str, fields: Iterable[str]) -> dict:
    """Filter a data dictionary based on a prefix and field names.

    Args:
        records (dict): Record data dictionary.
        prefix (str): Prefix to look for.
        fields (Iterable[str]): Field names to look for.

    Returns:
        dict: Filtered records.
    """
    return {
        k.replace(prefix, ""): v
        for k, v in data.items()
        if k.startswith(prefix) or k in fields
    }


class Participant:
    """Participant in database"""

    def __init__(self, data, apt: RecordList = None, que: RecordList = None):
        data = filter_fields(data, "participant_", ["record_id"])
        age_created = (data["age_created_months"], data["age_created_days"])
        data["age_now_months"], data["age_now_days"] = get_age(
            age_created, data["date_created"]
        )
        self.record_id = data["record_id"]
        self.data = data
        self.appointments = apt
        self.questionnaires = que

    def __repr__(self) -> str:
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        n_apt = 0 if self.appointments is None else len(self.appointments)
        n_que = 0 if self.questionnaires is None else len(self.questionnaires)
        return f"Participant {self.record_id}: {str(n_apt)} appointments, {str(n_que)} questionnaires"  # pylint: disable=line-too-long

    def __str__(self) -> str:
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        n_apt = 0 if self.appointments is None else len(self.appointments)
        n_que = 0 if self.questionnaires is None else len(self.questionnaires)
        return f"Participant {self.record_id}: {str(n_apt)} appointments, {str(n_que)} questionnaires"  # pylint: disable=line-too-long


class Appointment:
    """Appointment in database"""

    def __init__(self, data: dict):
        data = filter_fields(
            data, "appointment_", ["record_id", "redcap_repeat_instance"]
        )
        self.record_id = data["record_id"]
        self.data = data
        self.appointment_id = make_id(data["record_id"], data["redcap_repeat_instance"])
        self.status = data["status"]
        self.date = data["date"]

    def __repr__(self) -> str:
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long

    def __str__(self) -> str:
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long


class Questionnaire:
    """Language questionnaire in database"""

    def __init__(self, data: dict):
        data = filter_fields(data, "language_", ["record_id", "redcap_repeat_instance"])
        self.record_id = data["record_id"]
        self.questionnaire_id = make_id(self.record_id, data["redcap_repeat_instance"])
        self.isestimated = data["isestimated"]
        self.data = data
        for i in range(1, 5):
            lang = f"lang{i}_exp"
            self.data[lang] = int(self.data[lang]) if self.data[lang] else 0

    def __repr__(self) -> str:
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return f"Questionnaire {self.questionnaire_id}, participant {self.record_id}"

    def __str__(self) -> str:
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return f" Questionnaire {self.questionnaire_id}, participant {self.record_id}"


class BadTokenException(Exception):
    """If token is ill-formed."""


def post_request(fields: dict, token: str, timeout: Iterable[int] = (5, 10)) -> dict:
    """Make a POST request to the REDCap database.

    Args:
        fields (dict): Fields to retrieve.
        token (str): API token.
        timeout (Iterable[int], optional): Timeout of HTTP request in seconds. Defaults to 10.

    Raises:
        requests.exceptions.HTTPError: If HTTP request fails.
        BadTokenException: If API token contains non-alphanumeric characters.

    Returns:
        dict: HTTP request response in JSON format.
    """
    fields = OrderedDict(fields)
    fields["token"] = token
    fields.move_to_end("token", last=False)

    try:
        if not token.isalnum():
            raise BadTokenException("Token contains non-alphanumeric characters")
        r = requests.post(
            "https://apps.sjdhospitalbarcelona.org/redcap/api/",
            data=fields,
            timeout=timeout,
        )
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print(str(e) + ":\n" + r.text.replace("'<.*?>'", ""))
    except BadTokenException:
        print("Token contains non-alphanumeric characters")
    return None


def get_redcap_version(**kwargs: any) -> str:
    """Get REDCap version.
    Args:
        **kwargs (any, optional): Arguments passed to ``post_request``.
    Returns:
        str: REDCAp version number.
    """
    fields = {"content": "version"}
    r = post_request(fields=fields, **kwargs)
    return r.content.decode("utf-8") if r else None


def get_data_dict(**kwargs: any) -> any:
    """Get data dictionaries for categorical variables

    Args:
        **kwargs (any, optional): Additional arguments passed tp ``post_request``.

    Returns:
        dict: Data dictionary.
    """
    items = [
        "participant_sex",
        "participant_birth_type",
        "participant_hearing",
        "participant_source",
        "appointment_study",
        "appointment_status",
        "language_lang1",
        "language_lang2",
        "language_lang3",
        "language_lang4",
    ]
    fields = {"content": "metadata", "format": "json", "returnFormat": "json"}
    for idx, i in enumerate(items):
        fields[f"fields[{idx}]"] = i
    r = json.loads(post_request(fields=fields, **kwargs).text)
    items_ordered = [i["field_name"] for i in r]
    dicts = {}
    for k, v in zip(items_ordered, r):
        options = v["select_choices_or_calculations"].split("|")
        options = [tuple(o.strip().split(", ")) for o in options]
        if k.startswith("language_"):
            options = sorted(options, key=lambda x: x[1])
        dicts[k] = dict(options)
    return dicts


def str_to_dt(data: dict) -> dict:
    """Parse strings in a dictionary as formatted datetimes.

    It first tries to format the date as "Y-m-d H:M:S". If error, it assumes the "Y-m-d H:M" is due and tries to format it accordingly.

    Args:
        data (dict): Dictionary that may contain string formatted datetimes.

    Returns:
        dict: Dictionary with strings parsed as datetimes.
    """  # pylint: disable=line-too-long
    for k, v in data.items():
        if v and "date" in k:
            try:
                data[k] = datetime.strptime(data[k], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                data[k] = datetime.strptime(data[k], "%Y-%m-%d %H:%M")
    return data


def dt_to_str(data: dict) -> dict:
    """Format datatimes in a dictionary as strings following the ISO 8061 date format.

    Args:
        data (dict): Dictionary that may contain datetimes.

    Returns:
        dict: Dictionary with datetimes formatted as strings.
    """  # pylint: disable=line-too-long
    for k, v in data.items():
        if isinstance(v, datetime):
            data[k] = data[k].isoformat()
    return data


def get_next_id(**kwargs: any) -> str:
    """Get next record_id in REDCap database.

    Args:
        **kwargs (any, optional): Additional arguments passed to ``post_request``.

    Returns:
        str: record_id of next record.
    """
    fields = {"content": "generateNextRecordName"}
    return str(post_request(fields=fields, **kwargs).json())


def get_records(record_id: str | list = None, **kwargs: any) -> dict:
    """Return records as JSON.

    Args:
        kwargs  (any, optional): Additional arguments passed to ``post_request``.

    Returns:
        dict: REDCap records in JSON format.
    """
    fields = {"content": "record", "format": "json", "type": "flat"}
    if record_id and isinstance(record_id, list):
        fields["records[0]"] = record_id
        for r in record_id:
            fields[f"records[{record_id}]"] = r
    records = post_request(fields=fields, **kwargs).json()
    return [str_to_dt(r) for r in records]


def make_id(ppt_id: str, repeat_id: str = None) -> str:
    """Make a record ID.

    Args:
        ppt_id (str): Participant ID.
        repeat_id (str, optional): Appointment or Questionnaire ID, or ``redcap_repeated_id``. Defaults to None.

    Returns:
        str: Record ID.
    """  # pylint: disable=line-too-long
    ppt_id = str(ppt_id)
    if not ppt_id.isdigit():
        raise ValueError(f"`ppt_id`` must be a digit, but '{ppt_id}' was provided")
    if not repeat_id:
        return ppt_id
    repeat_id = str(repeat_id)
    if not repeat_id.isdigit():
        raise ValueError(
            f"`repeat_id`` must be a digit, but '{repeat_id}' was provided"
        )
    return ppt_id + ":" + repeat_id


class RecordNotFound(Exception):
    """If record is not found."""

    def __init__(self, record_id):
        super().__init__(f"Record '{record_id}' not found")


def get_participant(ppt_id: str, **kwargs: any) -> Participant:
    """Get participant record.

    Args:
        ppt_id: ID of participant (record_id).
        **kwargs (any, optional): Additional arguments passed to ``post_request``

    Returns:
        Participant: Participant object.
    """
    fields = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "records[0]": ppt_id,
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json",
    }
    for i, f in enumerate(["participants", "appointments", "language"]):
        fields[f"forms[{i}]"] = f
    recs = [str_to_dt(r) for r in post_request(fields, **kwargs).json()]
    apt, que = {}, {}
    for r in recs:
        repeat_id = make_id(r["record_id"], r["redcap_repeat_instance"])
        if r["redcap_repeat_instrument"] == "appointments":
            apt[repeat_id] = Appointment(r)
        if r["redcap_repeat_instrument"] == "language":
            que[repeat_id] = Questionnaire(r)
    try:
        return Participant(recs[0], apt=RecordList(apt), que=RecordList(que))
    except IndexError as exc:
        raise RecordNotFound(record_id=ppt_id) from exc


def get_appointment(apt_id: str, **kwargs: any) -> Appointment:
    """Get appointment record.

    Args:
        apt_id (str): ID of appointment (``redcap_repeated_id``).
        **kwargs (any, optional): Additional arguments passed to ``post_request``

    Returns:
        Appointment: Appointment object.
    """
    ppt_id, _ = apt_id.split(":")
    ppt = get_participant(ppt_id, **kwargs)
    try:
        return ppt.appointments.records[apt_id]
    except KeyError as exc:
        raise RecordNotFound(record_id=apt_id) from exc


def get_questionnaire(que_id: str, **kwargs: any) -> Questionnaire:
    """Get questionnaire record.

    Args:
        que_id (str): ID of appointment (``redcap_repeated_id``).
        **kwargs (any, optional): Additional arguments passed to ``post_request``

    Returns:
        Questionnaire: Appointment object.
    """
    ppt_id, _ = que_id.split(":")
    ppt = get_participant(ppt_id, **kwargs)
    try:
        return ppt.questionnaires.records[que_id]
    except KeyError as exc:
        raise RecordNotFound(record_id=que_id) from exc


def add_participant(data: dict, modifying: bool = False, **kwargs: any):
    """Add new participant to REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "normal" if modifying else "overwrite",
        "forceAutoNumber": "false" if modifying else "true",
        "data": f"[{json.dumps(dt_to_str(data))}]",
    }
    return post_request(fields=fields, **kwargs)


def delete_participant(data: dict, **kwargs: any):
    """Delete participant from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "",
        "records[0]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def add_appointment(data: dict, **kwargs: any):
    """Add new appointment to REDCap database.

    Args:
        record_id (dict): ID of participant.
        data (dict): Appointment data.
        **kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "overwrite",
        "forceAutoNumber": "false",
        "data": f"[{json.dumps(dt_to_str(data))}]",
    }
    return post_request(fields=fields, **kwargs)


def delete_appointment(data: dict, **kwargs: any):
    """Delete appointment from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        **kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "appointments",
        "repeat_instance": int(data["redcap_repeat_instance"]),
        f"records[{data['record_id']}]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def add_questionnaire(data: dict, **kwargs: any):
    """Add new questionnaire to REDCap database.

    Args:
        data (dict): Questionnaire data.
        **kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "overwrite",
        "forceAutoNumber": "false",
        "data": f"[{json.dumps(dt_to_str(data))}]",
    }

    return post_request(fields=fields, **kwargs)


def delete_questionnaire(data: dict, **kwargs: any):
    """Delete questionnaire from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        **kwargs (any, optional): Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "language",
        "repeat_instance": int(data["redcap_repeat_instance"]),
        f"records[{data['record_id']}]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def redcap_backup(path: str = "tmp", **kwargs: any) -> dict:
    """Download a backup of the REDCap database

    Args:
        path (str, optional): Output directory. Defaults to "tmp".
        **kwargs (any, optional): Additional arguments passed to ``post_request``.

    Returns:
        dict: A dictionary with the key data and metadata of the project.
    """
    if not exists(path):
        mkdir(path)
    pl = {}
    for k in ["project", "metadata", "instrument"]:
        pl[k] = {"format": "json", "returnFormat": "json", "content": k}
    d = {k: json.loads(post_request(v, **kwargs).text) for k, v in pl.items()}
    with open(join(path, "records.csv"), "w+", encoding="utf-8") as f:
        fields = {
            "content": "record",
            "action": "export",
            "format": "csv",
            "csvDelimiter": ",",
            "returnFormat": "json",
        }
        records = post_request(fields, **kwargs).content.decode().split("\n")
        records = [r + "\n" for r in records]
        f.writelines(records)

    b = {
        "project": d["project"],
        "instruments": d["instrument"],
        "fields": d["metadata"],
    }
    for k, v in b.items():
        with open(join(path, k + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f)
    timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M")
    file = join(path, "backup_" + timestamp + ".zip")
    for root, _, files in walk(path, topdown=False):
        with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(join(root, f))
    return file


class Records:
    """REDCap records"""

    def __init__(self, record_id: str | list = None, **kwargs: any):
        records = get_records(record_id, **kwargs)
        ppt, apt, que = {}, {}, {}
        for r in records:
            ppt_id = r["record_id"]
            repeat_id = r["redcap_repeat_instance"]
            if repeat_id and r["appointment_status"]:
                r["appointment_id"] = make_id(ppt_id, repeat_id)
                apt[r["appointment_id"]] = Appointment(r)
            if repeat_id and r["language_lang1"]:
                r["questionnaire_id"] = make_id(ppt_id, repeat_id)
                que[r["questionnaire_id"]] = Questionnaire(r)
            if not r["redcap_repeat_instrument"]:
                ppt[ppt_id] = Participant(r)

        # add appointments and questionnaires to each participant
        for p, v in ppt.items():
            apts = {k: v for k, v in apt.items() if v.record_id == p}
            v.appointments = RecordList(apts)
            ques = {k: v for k, v in que.items() if v.record_id == p}
            v.questionnaires = RecordList(ques)

        self.participants = RecordList(ppt)
        self.appointments = RecordList(apt)
        self.questionnaires = RecordList(que)

    def __repr__(self) -> str:
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return (
            "REDCap database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} questionnaires"
        )

    def __str__(self) -> str:
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return (
            "REDCap database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} questionnaires"
        )


class BadAgeFormat(Exception):
    """If age des not follow the right format."""

    def __init__(self, age: tuple[int, int]):
        super().__init__(f"`age` must follow the `(months, age)` format': { age }")


def parse_age(age: tuple) -> tuple[int, int]:
    """Validate age string or tuple.

    Args:
        age (tuple): Age of the participant as a tuple in the ``(months, days)`` format.

    Raises:
        ValueError: If age is not str or tuple.
        BadAgeFormat: If age is ill-formatted.

    Returns:
        tuple[int, int]: Age of the participant in the ``(months, days)`` format.
    """  # pylint: disable=line-too-long
    try:
        assert isinstance(age, tuple)
        assert len(age) == 2
        return int(age[0]), int(age[1])
    except AssertionError as e:
        raise BadAgeFormat(age) from e


def get_age(age: str | tuple, ts: datetime, ts_new: datetime = None):
    """Calculate the age of a person in months and days at a new timestamp.

    Args:
        age (tuple): Age in months and days as a tuple of type (months, days).
        ts (datetime): Birth date as ``datetime.datetime`` type.
        ts_new (datetime.datetime, optional): Time for which the age is calculated. Defaults to current date (``datetime.datetime.now()``).

    Returns:
        tuple: Age in at ``new_timestamp``.
    """  # pylint: disable=line-too-long
    if ts_new is None:
        ts_new = datetime.now(pytz.UTC)
    if ts.tzinfo is None or ts.tzinfo.utcoffset(ts) is None:
        ts = pytz.UTC.localize(ts, True)
    if ts_new.tzinfo is None or ts_new.tzinfo.utcoffset(ts_new) is None:
        ts_new = pytz.UTC.localize(ts_new, True)
    tdiff = relativedelta(ts_new, ts)
    age = parse_age(age)
    new_age_months = age[0] + tdiff.years * 12 + tdiff.months
    new_age_days = age[1] + tdiff.days
    if new_age_days >= 30:
        additional_months = new_age_days // 30
        new_age_months += additional_months
        new_age_days %= 30
    return new_age_months, new_age_days
