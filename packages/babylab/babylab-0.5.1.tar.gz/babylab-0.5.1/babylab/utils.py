"""
Util functions for the app.
"""

import os
import shutil
from collections.abc import Iterable
from datetime import date, timedelta, datetime
from functools import singledispatch
from copy import deepcopy
from pandas import DataFrame, to_datetime
from markupsafe import Markup
from babylab import api


def fmt_ppt_id(ppt_id: str) -> str:
    """Format appointment ID.

    Args:
        ppt_id (str): Participant ID.

    Returns:
        str: Formated participant ID.
    """
    return f"<a class='ppt-id' href=/participants/{ppt_id}>{ppt_id}</a>"


def fmt_apt_id(apt_id: str) -> str:
    """Format appointment ID.

    Args:
        apt_id (str): Appointment ID.

    Returns:
        str: Formated appointment ID.
    """
    return f"<a class='ppt-id' href=/appointments/{apt_id}>{apt_id}</a>"


def fmt_que_id(que_id: str) -> str:
    """Format questionnaire ID.

    Args:
        apt_id (str): Questionnaire ID.
        ppt_id (str): Participant ID.

    Returns:
        str: Formated questionnaire ID.
    """
    return f"<a class='ppt-id' href=/questionnaires/{que_id}>{que_id}</a>"


def fmt_percentage(x: float | int) -> str:
    """Format number into percentage.

    Args:
        x (float | int): Number to format. Must be higher than or equal to zero, and lower than or equal to one.

    Raises:
        ValueError: If number is not higher than or equal to zero, and lower than or equal to one.

    Returns:
        str: Formatted percentage.
    """  # pylint: disable=line-too-long
    if x > 100 or x < 0:
        raise ValueError(
            "`x` higher than or equal to zero, and lower than or equal to one"
        )
    return str(int(float(x))) if x else ""


def fmt_taxi_isbooked(address: str, isbooked: str) -> str:
    """Format ``taxi_isbooked`` variable to HTML.

    Args:
        address (str): ``taxi_address`` value.
        isbooked (str): ``taxi_isbooked`` value.

    Raises:
        ValueError: If ``isbooked`` is not "0" or "1".

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if str(isbooked) not in ["", "0", "1"]:
        raise ValueError(
            f"`is_booked` must be one of '0' or '1', but {isbooked} was provided"
        )
    if not address:
        return ""
    if int(isbooked):
        return "<p style='color: green;'>Yes</p>"
    return "<p style='color: red;'>No</p>"


def fmt_new_button(record: str, ppt_id: str = None):
    """Add new record button.

    Args:
        record (str): Type of record.
        ppt_id (str): Participant ID.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if record not in ["Appointment", "Questionnaire"]:
        raise ValueError(
            f"`record` must be 'Appointment' or 'Questionnaire', but {record} was provided"
        )
    if record == "Appointment":
        button_str = '<button type="button" class="btn btn-table"><i class="fa-solid fa-calendar"></i></button></a>'
        return f'<a href="/appointments/appointment_new?ppt_id={ppt_id}">{button_str}'
    button_str = '<button type="button" class="btn btn-table"><i class="fa-solid fa-language"></i></button></a>'
    return f'<a href="/questionnaires/questionnaire_new?ppt_id={ppt_id}">{button_str}'


def fmt_modify_button(ppt_id: str = None, apt_id: str = None, que_id: str = None):
    """Add modify button.

    Args:
        ppt_id (str): Participant ID.
        apt_id (str, optional): Appointment ID. Defaults to None.
        que_id (str, optional): Questionnaire ID. Defaults to None.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    button_str = '<button type="button" class="btn btn-table"><i class="fa-solid fa-pen"></i></button></a>'

    if apt_id:
        return f'<a href="/appointments/{apt_id}/appointment_modify">{button_str}'

    if que_id:
        return f'<a href="/questionnaires/{que_id}/questionnaire_modify">{button_str}'

    return f'<a href="/participants/{ppt_id}/participant_modify">{button_str}'


@singledispatch
def fmt_labels(x: dict | DataFrame, prefixes: Iterable[str]):
    """Reformat dataframe.

    Args:
        x (dict | DataFrame): Dataframe to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.
        prefixes (Iterable[str]): List of prefixes to look for in variable names.

    Returns:
        DataFrame: A reformated Dataframe.
    """
    raise TypeError("`x` must be a dict or a pd.DataFrame")


@fmt_labels.register(dict)
def fmt_dict(x: dict, data_dict: dict) -> dict:
    """Reformat dictionary.

    Args:
        x (dict): dictionary to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.

    Returns:
        dict: A reformatted dictionary.
    """
    fields = ["participant_", "appointment_", "language_"]
    y = dict(x)
    for k, v in y.items():
        for f in fields:
            if f + k in data_dict and v:
                y[k] = data_dict[f + k][v]
        if "exp" in k:
            y[k] = round(float(v), None) if v else ""
        if "taxi_isbooked" in k:
            y[k] = fmt_taxi_isbooked(y["taxi_address"], y[k])
    return y


@fmt_labels.register(DataFrame)
def _(x: DataFrame, data_dict: dict, prefixes: list[str] = None) -> DataFrame:

    if prefixes is None:
        prefixes = ["participant", "appointment", "language"]
    for col, val in x.items():
        kdict = [x + "_" + col for x in prefixes]
        for k in kdict:
            if k in data_dict:
                x[col] = [data_dict[k][v] if v else "" for v in val]
        if "lang" in col:
            x[col] = ["" if v == "None" else v for v in x[col]]
        if "exp" in col:
            x[col] = [fmt_percentage(v) for v in val]
        if "taxi_isbooked" in col:
            pairs = zip(x["taxi_address"], x[col])
            x[col] = [fmt_taxi_isbooked(a, i) for a, i in pairs]
        if "isestimated" in col:
            x[col] = ["Estimated" if x == "1" else "Calculated" for x in x[col]]
    return x


def fmt_apt_status(x: str, markup: bool = True) -> str:
    """format appointment status using custom CSS class.

    Args:
        x (str): Appointment status value (label).
        markup (bool, optional): Should the string be markup-safe? defaults to True.

    Returns:
        str: HTML-CSS formatted appointment status label.
    """
    status_css = {
        "Scheduled": "scheduled",
        "Confirmed": "confirmed",
        "Successful": "successful",
        "Successful - Good": "good",
        "Cancelled - Reschedule": "reschedule",
        "Cancelled - Drop": "drop",
        "No show": "drop",
    }
    out = f"<p class='btn btn-status btn-status-{status_css[x]}'>{x}</p>"
    return Markup(out) if markup else out


def replace_labels(x: DataFrame | dict, data_dict: dict) -> DataFrame:
    """Replace field values with labels.

    Args:
        x (DataFrame): Pandas DataFrame in which to replace values with labels.
        data_dict (dict): Data dictionary as returned by ``get_data_dictionary``.

    Returns:
        DataFrame: A Pandas DataFrame with replaced labels.
    """  # pylint: disable=line-too-long
    return fmt_labels(x, data_dict)


def is_in_data_dict(
    x: Iterable[str] | None, variable: str, data_dict: dict
) -> Iterable[str]:
    """Check that a value is an element in the data dictionary.

    Args:
        x (Iterable[str] | None): Value to look up in the data dictionary.
        variable (str): Key in which to look for.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.

    Raises:
        ValueError: _description_

    Returns:
        Iterable[str]: Values in data dict.
    """
    options = list(data_dict[variable].values())
    if x is None:
        return options
    out = x
    if isinstance(x, str):
        out = [out]
    for o in out:
        if o not in options:
            raise ValueError(f"{o} is not an option in {variable}")
    return out


def get_age_timestamp(
    apt_records: dict, ppt_records: dict, dtype: str = "date"
) -> tuple[str, str]:
    """Get age at timestamp in months and days.

    Args:
        apt_records (dict): Appointment records.
        ppt_records (dict): Participant records.
        date_type (str, optional): Timestamp at which to calculate age. Defaults to "date".

    Raises:
        ValueError: If timestamp is not "date" or "date_created".

    Returns:
        tuple[str, str]: Age at timestamp in months and days.
    """
    if dtype not in ["date", "date_created"]:
        raise ValueError("timestamp must be 'date' or 'date_created'")

    months_new, days_new = [], []
    for v in apt_records.values():
        ppt_data = ppt_records[v.record_id].data
        months = ppt_data["age_now_months"]
        days = ppt_data["age_now_days"]
        age_now = api.get_age(
            age=(months, days),
            ts=ppt_data[dtype] if dtype == "date_created" else v.data["date"],
        )
        months_new.append(int(age_now[0]))
        days_new.append(int(age_now[1]))
    return months_new, days_new


def get_ppt_table(
    records: api.Records,
    data_dict: dict,
    relabel: bool = True,
    study: str = None,
) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict, optional): Data dictionary as returned by ``api.get_data_dictionary``.
        relabel (bool, optional): Should columns be relabeled? Defaults to True.
        study (str, optional): Study in which the participant in the records must have participated to be kept. Defaults to None.

    Returns:
        DataFrame: Table of partcicipants.
    """  # pylint: disable=line-too-long
    cols = [
        "record_id",
        "date_created",
        "date_updated",
        "source",
        "name",
        "age_created_months",
        "age_created_days",
        "days_since_last_appointment",
        "sex",
        "twin",
        "parent1_name",
        "parent1_surname",
        "isdroput",
        "email1",
        "phone1",
        "parent2_name",
        "parent2_surname",
        "email2",
        "phone2",
        "address",
        "city",
        "postcode",
        "birth_type",
        "gest_weeks",
        "birth_weight",
        "head_circumference",
        "apgar1",
        "apgar2",
        "apgar3",
        "hearing",
        "diagnoses",
        "comments",
    ]
    if not records.participants.records:
        return DataFrame([], columns=cols)
    ppt = records.participants
    apt = records.appointments
    if study:
        target_ids = [
            a.record_id for a in apt.records.values() if study in a.data["study"]
        ]
        ppt.records = {k: v for k, v in ppt.records.items() if k in target_ids}
    new_age_months = []
    new_age_days = []
    for v in ppt.records.values():
        age_created = (v.data["age_created_months"], v.data["age_created_days"])
        age = api.get_age(age_created, ts=v.data["date_created"])
        new_age_months.append(int(age[0]))
        new_age_days.append(int(age[1]))
    df = records.participants.to_df()
    df["age_now_months"], df["age_now_days"] = new_age_months, new_age_days
    if relabel:
        df = replace_labels(df, data_dict)
    return df


def get_apt_table(
    records: api.Records,
    data_dict: dict = None,
    study: str = None,
    relabel: bool = True,
) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.

    Returns:
        DataFrame: Table of appointments.
    """  # pylint: disable=line-too-long
    apts = deepcopy(records.appointments)
    if study:
        apts.records = {
            k: v for k, v in apts.records.items() if v.data["study"] == study
        }

    if not apts.records:
        return DataFrame(
            [],
            columns=[
                "appointment_id",
                "record_id",
                "study",
                "status",
                "date",
                "date_created",
                "date_updated",
                "taxi_address",
                "taxi_isbooked",
            ],
        )
    apt_records = apts.records
    if isinstance(records, api.Records):
        ppt_records = records.participants.records
    else:
        ppt_records = {records.record_id: api.RecordList(records).records}

    df = apts.to_df()
    df["appointment_id"] = [
        api.make_id(i, apt_id)
        for i, apt_id in zip(df.index, df["redcap_repeat_instance"])
    ]
    df["age_now_months"], df["age_now_days"] = get_age_timestamp(
        apt_records, ppt_records, "date_created"
    )
    df["age_apt_months"], df["age_apt_days"] = get_age_timestamp(
        apt_records, ppt_records, "date"
    )
    df["date"] = to_datetime(df.date)
    df["date"] = df["date"].dt.strftime("%d/%m/%y %H:%M")
    if relabel:
        df = replace_labels(df, data_dict)
    return df


def get_que_table(
    records: api.Records, data_dict: dict, relabel: bool = True
) -> DataFrame:
    """Get questionnaires table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.
        relabel (bool, optional): Should columns be relabeled? Defaults to True.

    Returns:
        DataFrame: A formated Pandas DataFrame.
    """  # pylint: disable=line-too-long
    quest = records.questionnaires

    if not quest.records:
        return DataFrame(
            [],
            columns=[
                "record_id",
                "questionnaire_id",
                "isestimated",
                "date_created",
                "date_updated",
                "lang1",
                "lang1_exp",
                "lang2",
                "lang2_exp",
                "lang3",
                "lang3_exp",
                "lang4",
                "lang4_exp",
            ],
        )
    df = quest.to_df()
    df["questionnaire_id"] = [
        api.make_id(p, q) for p, q in zip(df.index, df["redcap_repeat_instance"])
    ]
    if relabel:
        replace_labels(df, data_dict)
    return df


def count_col(
    x: DataFrame,
    col: str,
    values_sort: bool = False,
    cumulative: bool = False,
    missing_label: str = "Missing",
) -> dict:
    """Count frequencies of column in DataFrame.

    Args:
        x (DataFrame): DataFrame containing the target column.
        col (str): Name of the column.
        values_sort (str, optional): Should the resulting dict be ordered by values? Defaults to False.
        cumulative (bool, optional): Should the counts be cumulative? Defaults to False.
        missing_label (str, optional): Label to associate with missing values. Defaults to "Missing".

    Returns:
        dict: Counts of each category, sorted in descending order.
    """  # pylint: disable=line-too-long
    counts = x[col].value_counts().to_dict()
    counts = {missing_label if not k else k: v for k, v in counts.items()}
    if values_sort:
        counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    if cumulative:
        cumsum = 0
        for key in counts:
            cumsum += counts[key]
            counts[key] = cumsum
    return counts


def clean_tmp(path: str = "tmp"):
    """Clean temporal directory

    Args:
        path (str, optional): Path to the temporal directory. Defaults to "tmp".
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def get_year_weeks(year: int):
    """Get week numbers of the year"""
    date_first = date(year, 1, 1)
    date_first += timedelta(days=6 - date_first.weekday())
    while date_first.year == year:
        yield date_first
        date_first += timedelta(days=7)


def get_week_n(timestamp: date):
    """Get current week number"""
    weeks = {}
    for wn, d in enumerate(get_year_weeks(timestamp.year)):
        weeks[wn + 1] = [(d + timedelta(days=k)).isoformat() for k in range(0, 7)]
    for k, v in weeks.items():
        if datetime.strftime(timestamp, "%Y-%m-%d") in v:
            return k
    return None


def get_weekly_apts(
    records: api.Records,
    data_dict: dict,
    study: Iterable | None = None,
    status: Iterable | None = None,
) -> dict:
    """Get weekly number of appointments.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (Iterable | None, optional): Study to filter for. Defaults to None.
        status (Iterable | None, optional): Status to filter for. Defaults to None.

    Raises:
        ValueError: If `study` or `status` is not available.

    Returns:
        dict: Weekly number of appointment with for a given study and/or status.
    """  # pylint: disable=line-too-long
    study = is_in_data_dict(study, "appointment_study", data_dict)
    status = is_in_data_dict(status, "appointment_status", data_dict)
    apts = records.appointments.records.values()
    return sum(
        get_week_n(v.data["date_created"]) == get_week_n(datetime.today())
        for v in apts
        if data_dict["appointment_status"][v.data["status"]] in status
        and data_dict["appointment_study"][v.data["study"]] in study
    )
