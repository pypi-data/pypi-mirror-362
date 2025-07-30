import uuid
from datetime import datetime
from datetime import timezone

from h2o_audit_trail.event.client import EventClient
from h2o_audit_trail.event.create import CreateEventRequest
from h2o_audit_trail.event.search import SearchEventsRequestFilter
from tests.testutil.eventutil.event import default_event
from tests.testutil.eventutil.event import with_resource


def test_search_events(event_client_user4: EventClient) -> None:
    start = datetime.now(tz=timezone.utc)
    event_id1 = str(uuid.uuid4())
    event_id2 = str(uuid.uuid4())
    event_id3 = str(uuid.uuid4())

    batch_create_resp = event_client_user4.batch_create_events(requests=[
        CreateEventRequest(
            event_id=event_id1,
            event=default_event(with_resource("rsrc1"))
        ),
        CreateEventRequest(
            event_id=event_id2,
            event=default_event(with_resource("rsrc2"))
        ),
        CreateEventRequest(
            event_id=event_id3,
            event=default_event(with_resource("rsrc3"))
        )
    ])
    assert len(batch_create_resp.events) == 3

    resp = event_client_user4.search_events(
        filter_=SearchEventsRequestFilter(
            start_event_time=start,
        )
    )

    assert len(resp.events) == 3
    assert resp.next_page_token == ""
    assert resp.events[0].name == f"events/{event_id3}"
    assert resp.events[1].name == f"events/{event_id2}"
    assert resp.events[2].name == f"events/{event_id1}"
    assert resp.searched_until_time == start

    resp = event_client_user4.search_events(
        filter_=SearchEventsRequestFilter(
            start_event_time=start,
            resource_exact="rsrc1",
        ),
    )

    assert len(resp.events) == 1
    assert resp.next_page_token == ""
    assert resp.events[0].name == f"events/{event_id1}"
    assert resp.searched_until_time == start

    resp = event_client_user4.search_events(
        filter_=SearchEventsRequestFilter(
            start_event_time=start,
            resource_regex="(rsrc1|rsrc2)",
        ),
    )

    assert len(resp.events) == 2
    assert resp.next_page_token == ""
    assert resp.events[0].name == f"events/{event_id2}"
    assert resp.events[1].name == f"events/{event_id1}"
    assert resp.searched_until_time == start
