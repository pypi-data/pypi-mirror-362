"""Test database models
"""

from datetime import datetime
from pandas import DataFrame
from babylab import api


def test_participant_class(ppt_record):
    """Test participant class."""
    p = api.Participant(ppt_record)
    assert hasattr(p, "record_id")
    assert hasattr(p, "data")

    assert isinstance(p.record_id, str)
    assert isinstance(p.data, dict)

    assert isinstance(repr(p), str)
    assert "Participant " in repr(p)
    assert isinstance(str(p), str)
    assert "Participant " in str(p)


def test_appointment_class(apt_record):
    """Test appointment class."""
    a = api.Appointment(apt_record)
    assert hasattr(a, "appointment_id")
    assert hasattr(a, "record_id")
    assert hasattr(a, "date")
    assert hasattr(a, "status")
    assert hasattr(a, "data")

    assert isinstance(a.appointment_id, str)
    assert isinstance(a.record_id, str)
    assert isinstance(a.date, datetime)
    assert isinstance(a.status, str)
    assert isinstance(a.data, dict)

    assert isinstance(repr(a), str)
    assert "Appointment " in repr(a)
    assert isinstance(str(a), str)
    assert "Appointment " in str(a)


def test_questionnaire_class(que_record):
    """Test questionnaire class."""
    q = api.Questionnaire(que_record)
    assert hasattr(q, "questionnaire_id")
    assert hasattr(q, "isestimated")
    assert hasattr(q, "record_id")
    assert hasattr(q, "data")
    assert isinstance(repr(q), str)
    assert "questionnaire " in repr(q).lower()
    assert isinstance(str(q), str)
    assert "questionnaire " in str(q).lower()


def test_records_class(token_fixture):
    """Test participant class."""
    records = api.Records(token=token_fixture)
    assert hasattr(records, "appointments")
    assert hasattr(records, "participants")
    assert hasattr(records, "questionnaires")
    assert isinstance(records.appointments, api.RecordList)
    assert isinstance(records.participants, api.RecordList)
    assert isinstance(records.questionnaires, api.RecordList)

    assert isinstance(repr(records), str)
    assert "REDCap database" in repr(records)
    assert isinstance(str(records), str)
    assert "REDCap database" in str(records)


def test_recordlist_class_participants(token_fixture):
    """Test RecordList class with participants."""
    records = api.Records(token=token_fixture).participants
    assert isinstance(records.records, dict)
    assert isinstance(records.to_df(), DataFrame)


def test_recordlist_class_appointments(token_fixture):
    """Test RecordList class with appointments."""
    records = api.Records(token=token_fixture).appointments
    assert isinstance(records.records, dict)
    assert isinstance(records.to_df(), DataFrame)


def test_recordlist_class_questionnaires(token_fixture):
    """Test RecordList class with questionnaires."""
    records = api.Records(token=token_fixture).questionnaires
    assert isinstance(records.records, dict)
    assert isinstance(records.to_df(), DataFrame)


def test_records_class_participants(records_fixture):
    """Test records class (Participants)"""
    assert hasattr(records_fixture.participants, "records")
    assert hasattr(records_fixture.participants, "to_df")
    assert isinstance(records_fixture.participants.records, dict)
    assert all(
        isinstance(r, api.Participant)
        for r in records_fixture.participants.records.values()
    )


def test_records_class_appointments(records_fixture):
    """Test records class (Appointments)"""
    assert hasattr(records_fixture.appointments, "records")
    assert hasattr(records_fixture.appointments, "to_df")
    assert isinstance(records_fixture.appointments.records, dict)
    assert all(
        isinstance(r, api.Appointment)
        for r in records_fixture.appointments.records.values()
    )


def test_records_class_questionnaires(records_fixture):
    """Test records class (Questionnaires)"""
    assert hasattr(records_fixture.questionnaires, "records")
    assert hasattr(records_fixture.questionnaires, "to_df")
    assert isinstance(records_fixture.questionnaires.records, dict)
    assert all(
        isinstance(r, api.Questionnaire)
        for r in records_fixture.questionnaires.records.values()
    )
