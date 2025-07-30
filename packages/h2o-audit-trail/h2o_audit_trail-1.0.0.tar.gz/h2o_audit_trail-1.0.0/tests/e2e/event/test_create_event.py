import uuid
from datetime import datetime
from datetime import timezone

from h2o_audit_trail.event.client import EventClient
from h2o_audit_trail.event.event import Event
from h2o_audit_trail.model.status import Status


def test_create_event(event_client_user4: EventClient) -> None:
    now = datetime.now(timezone.utc)
    event_id = str(uuid.uuid4())

    event = event_client_user4.create_event(
        event_id=event_id,
        event=Event(
            event_time=now,
            event_source="h2oai-enginemanager-server",
            action="actions/enginemanager/daiEngines/CREATE",
            read_only=False,
            resource="workspaces/w1/daiEngine/e1",
            request_parameters={
                "param1": "val1",
                "param2": "val2",
            },
            status=Status(
                code=3,
                message="cpu must be < 5",
            ),
            principal="users/jans",
            source_ip_address="1.1.1.1",
            user_agent="Mozilla/5.0",
            metadata={
                "key1": "v1",
                "key2": "v2",
            }
        ),
    )

    assert event.name == f"events/{event_id}"
    assert event.event_time == now
    assert now < event.receive_time
    assert event.event_source == "h2oai-enginemanager-server"
    assert event.action == "actions/enginemanager/daiEngines/CREATE"
    assert event.read_only is False
    assert event.resource == "workspaces/w1/daiEngine/e1"
    assert event.request_parameters == {
        "param1": "val1",
        "param2": "val2",
    }
    assert event.status.code == 3
    assert event.status.message == "cpu must be < 5"
    assert event.principal == "users/jans"
    assert event.source_ip_address == "1.1.1.1"
    assert event.user_agent == "Mozilla/5.0"
    assert event.metadata == {
        "key1": "v1",
        "key2": "v2",
    }
    assert event.workspace == "workspaces/w1"
