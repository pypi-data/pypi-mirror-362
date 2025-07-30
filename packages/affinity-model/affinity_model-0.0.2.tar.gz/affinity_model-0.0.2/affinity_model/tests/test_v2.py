import pytest

# Test that we can import the V2 model symbols
from affinity_model.v2 import (
    AuthenticationError,
    Company,
    Email,
    Person,
    Meeting,
    Attendee,
)


def test_v2_model_imports():
    # Instantiate a few representative classes with minimal required fields
    auth_error = AuthenticationError(code="authentication", message="msg")
    company = Company(id=1, name="Acme", domains=[], isGlobal=False)
    person = Person(id=1, firstName="John", emailAddresses=[], type="internal")
    attendee = Attendee(emailAddress="test@example.com")
    email = Email(
        type="email",
        id=1,
        sentAt="2023-01-01T00:00:00Z",
        to=[attendee],
        cc=[],
        **{"from": attendee},
    )
    meeting = Meeting(
        type="meeting",
        id=1,
        title="Test Meeting",
        allDay=False,
        startTime="2023-01-01T00:00:00Z",
        attendees=[],
    )

    assert auth_error.code == "authentication"
    assert company.name == "Acme"
    assert person.firstName == "John"
    assert email.id == 1
    assert meeting.title == "Test Meeting"
