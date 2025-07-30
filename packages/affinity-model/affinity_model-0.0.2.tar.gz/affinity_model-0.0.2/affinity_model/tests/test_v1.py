import json
from pydantic import BaseModel
import pytest
from datetime import datetime
from freezegun import freeze_time
from ..v1 import Note, NoteType, InteractionType


from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def assert_model(m: BaseModel, snapshot):
    json = m.model_dump_json(by_alias=True, exclude_unset=True, round_trip=True)
    assert json == snapshot


@freeze_time("2020-01-01 12:34:56")
def test_note(snapshot_json):
    n = Note(
        id=1,
        creator_id=1,
        person_ids=[1],
        associated_person_ids=[1],
        interaction_person_ids=[1],
        interaction_id=1,
        interaction_type=InteractionType.EMAIL,
        is_meeting=True,
        mentioned_person_ids=[1],
        organization_ids=[1],
        opportunity_ids=[1],
        type=NoteType.PLAIN_TEXT,
        parent_id=None,
        content="Hello, World!",
        created_at=datetime.now(),
        updated_at=None,
    )

    assert_model(n, snapshot_json)
