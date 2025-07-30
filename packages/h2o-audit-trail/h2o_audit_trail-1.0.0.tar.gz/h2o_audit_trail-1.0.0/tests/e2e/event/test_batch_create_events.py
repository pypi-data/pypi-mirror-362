import uuid
from datetime import datetime
from datetime import timezone

from h2o_audit_trail.event.client import EventClient
from h2o_audit_trail.event.create import CreateEventRequest
from tests.testutil.eventutil.event import default_event
from tests.testutil.eventutil.event import with_event_time
from tests.testutil.eventutil.event import with_metadata
from tests.testutil.eventutil.event import with_request_parameters
from tests.testutil.eventutil.event import with_resource
from tests.testutil.eventutil.event import with_user_agent


def test_batch_create_events(event_client_user4: EventClient) -> None:
    event_time1 = datetime.now(timezone.utc)
    event_time2 = datetime.now(timezone.utc)
    event_id1 = str(uuid.uuid4())
    event_id2 = str(uuid.uuid4())

    requests = [
        CreateEventRequest(
            event_id=event_id1,
            event=default_event(
                with_event_time(event_time1),
                with_resource("workspaces/w1/daiEngine/e1"),
                with_request_parameters({
                    "param1": "val1",
                    "param2": "val2",
                }),
                with_user_agent("Mozilla/5.0"),
                with_metadata({
                    "key1": "v1",
                    "key2": "v2",
                })
            ),
        ),
        CreateEventRequest(
            event_id=event_id2,
            event=default_event(with_event_time(event_time2)),
        ),
        CreateEventRequest(
            event_id="invalid",
            event=default_event(),
        )
    ]

    resp = event_client_user4.batch_create_events(
        requests=requests,
    )

    events = resp.events
    failed_requests = resp.failed_requests

    assert len(events) == 2
    event1 = events[0]
    assert event1.name == f"events/{event_id1}"
    assert event1.event_time == event_time1
    assert event_time1 < event1.receive_time
    assert event1.event_source == "h2oai-enginemanager-server"
    assert event1.action == "actions/enginemanager/daiEngines/CREATE"
    assert event1.read_only is False
    assert event1.resource == "workspaces/w1/daiEngine/e1"
    assert event1.request_parameters == {
        "param1": "val1",
        "param2": "val2",
    }
    assert event1.status.code == 3
    assert event1.status.message == "cpu must be < 5"
    assert event1.principal == "users/jans"
    assert event1.source_ip_address == "1.1.1.1"
    assert event1.user_agent == "Mozilla/5.0"
    assert event1.metadata == {
        "key1": "v1",
        "key2": "v2",
    }
    assert event1.workspace == "workspaces/w1"

    assert events[1].name == f"events/{event_id2}"

    assert len(failed_requests) == 1
    assert failed_requests[2].code == 3
    assert failed_requests[2].message == "event_id must be in UUIDv4 format"
