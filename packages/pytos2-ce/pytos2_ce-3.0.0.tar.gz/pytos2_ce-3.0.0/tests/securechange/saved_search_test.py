import pytest
import responses


class TestQuest:
    @responses.activate
    def test_get_saved_searches(self, saved_search_mock, scw):
        queries = scw.get_saved_searches()
        assert queries[0].id == 14
        assert queries[0].type == "DETAILED"
        assert queries[0].name == "Clone Server/Subnet Policy tickets"
        assert (
            queries[0].last_used.isoformat(timespec="milliseconds")
            == "2024-10-22T05:54:18.451-07:00"
        )
        assert (
            queries[0].create_date.isoformat(timespec="milliseconds")
            == "2019-11-27T14:31:05.389-08:00"
        )

        assert queries[1].id == 16
        assert queries[1].type == "FREE_TEXT"
        assert queries[1].name == "Rule Recertification tickets"
        assert (
            queries[1].last_used.isoformat(timespec="milliseconds")
            == "2024-10-28T08:45:02.931-07:00"
        )
        assert (
            queries[1].create_date.isoformat(timespec="milliseconds")
            == "2019-11-27T15:24:11.654-08:00"
        )

    @responses.activate
    def test_get_saved_search(self, saved_search_mock, scw):
        query = scw.get_saved_search(14)
        assert query[0].id == 14
        assert query[0].name == "Clone Server/Subnet Policy tickets"
        assert query[0].type == "DETAILED"
        assert (
            query[0].last_used.isoformat(timespec="milliseconds")
            == "2024-10-22T05:54:18.451-07:00"
        )
        assert (
            query[0].create_date.isoformat(timespec="milliseconds")
            == "2019-11-27T14:31:05.389-08:00"
        )

        filters = query[0].filters
        assert filters.subject == "CSP*"
        assert filters.requester == ""
        assert filters.group == ""
        assert filters.assigned_to == ""
        assert filters.current_step_name == ""
        assert filters.priorities == ["Critical", "High", "Normal", "Low"]
        assert filters.sla_outcome == []
        assert filters.sla_status == []
        assert filters.ticket_statuses == ["IN_PROGRESS"]
        assert filters.task_status == []
        assert filters.domain_id == []
        assert filters.field.name == ""
        assert filters.field.value == ""

    @responses.activate
    def test_add_saved_search(self, saved_search_mock, scw):
        create_query = {
            "query": {
                "type": "DETAILED",
                "name": "DetailedQuery_test1",
                "description": "detailed query",
                "filters": {
                    "ticketId": 1,
                    "subject": "subject",
                    "requester": "requester",
                    "group": "group",
                    "assignedTo": "handler",
                    "currentStepName": "currentStepName",
                    "priorities": ["Critical", "Normal"],
                    "slaOutcomes": ["OVERDUE"],
                    "slaStatuses": ["ALERT"],
                    "ticketStatuses": ["IN_PROGRESS"],
                    "taskStatuses": ["WAITING_TO_BE_ASSIGNED", "ASSIGNED"],
                    "domainIds": [],
                    "expiration": {
                        "fromDate": "2023-11-01T00:00:00+02:00",
                        "toDate": "2023-12-31T00:00:00+02:00",
                    },
                    "field": {"name": "fieldName", "value": "fieldValue"},
                },
            }
        }
        scw.add_saved_search(create_query)

    @responses.activate
    def test_update_saved_search(self, saved_search_mock, scw):
        id = 81
        update_query = {
            "query": {
                "type": "DETAILED",
                "id": 81,
                "name": "DetailedQuery_test1",
                "description": "detailed query Update Test",
                "createDate": "2024-11-04T05:20:36.755-08:00",
                "filters": {
                    "ticketId": 1,
                    "subject": "subject",
                    "requester": "requester",
                    "group": "group",
                    "assignedTo": "handler",
                    "currentStepName": "currentStepName",
                    "priorities": ["Critical", "Normal"],
                    "slaOutcomes": ["OVERDUE"],
                    "slaStatuses": ["ALERT"],
                    "ticketStatuses": ["IN_PROGRESS"],
                    "taskStatuses": ["WAITING_TO_BE_ASSIGNED", "ASSIGNED"],
                    "domainIds": [],
                    "expiration": {
                        "fromDate": "2023-10-31T15:00:00-07:00",
                        "toDate": "2023-12-30T14:00:00-08:00",
                    },
                    "field": {"name": "fieldName", "value": "fieldValue"},
                },
            }
        }
        scw.update_saved_search(id, update_query)

    @responses.activate
    def test_delete_saved_search(self, saved_search_mock, scw):
        id = 81
        scw.delete_saved_search(id)

    @responses.activate
    def test_add_saved_search_bad_request(self, bad_saved_search_mock, scw):
        create_query = {
            "query": {
                "type": "DETAILED",
                "name": "DetailedQuery_test1",
                "description": "detailed query",
                "filters": {
                    "ticketId": 1,
                    "subject": "subject",
                    "requester": "requester",
                    "group": "group",
                    "assignedTo": "handler",
                    "currentStepName": "currentStepName",
                    "priorities": ["Critical", "Normal"],
                    "slaOutcomes": ["OVERDUE"],
                    "slaStatuses": ["ALERT"],
                    "ticketStatuses": ["IN_PROGRESS"],
                    "taskStatuses": ["WAITING_TO_BE_ASSIGNED", "ASSIGNED"],
                    "domainIds": [],
                    "expiration": {
                        "fromDate": "2023-11-01T00:00:00+02:00",
                        "toDate": "2023-12-31T00:00:00+02:00",
                    },
                    "field": {"name": "fieldName", "value": "fieldValue"},
                },
            }
        }

        with pytest.raises(ValueError) as exc_info:
            scw.add_saved_search(create_query)

        assert "400" in str(exc_info.value)
        assert "The query name already exists" in str(exc_info.value)

    @responses.activate
    def test_update_saved_search_bad_request(self, bad_saved_search_mock, scw):
        update_query = {
            "query": {
                "type": "DETAILED",
                "name": "DetailedQuery_test1",
                "description": "detailed query",
                "filters": {
                    "ticketId": 1,
                    "subject": "subject",
                    "requester": "requester",
                    "group": "group",
                    "assignedTo": "handler",
                    "currentStepName": "currentStepName",
                    "priorities": ["Critical", "Normal"],
                    "slaOutcomes": ["OVERDUE"],
                    "slaStatuses": ["ALERT"],
                    "ticketStatuses": ["IN_PROGRESS"],
                    "taskStatuses": ["WAITING_TO_BE_ASSIGNED", "ASSIGNED"],
                    "domainIds": [],
                    "expiration": {
                        "fromDate": "2023-11-01T00:00:00+02:00",
                        "toDate": "2023-12-31T00:00:00+02:00",
                    },
                    "field": {"name": "fieldName", "value": "fieldValue"},
                },
            }
        }
        id = 97
        with pytest.raises(ValueError) as exc_info:
            scw.update_saved_search(id, update_query)

        assert "400" in str(exc_info.value)
        assert (
            "The query ID does not exist, or you do not have the required permissions"
            in str(exc_info.value)
        )

    @responses.activate
    def test_delete_saved_search_bad_request(self, bad_saved_search_mock, scw):
        id = 97
        with pytest.raises(ValueError) as exc_info:
            scw.delete_saved_search(id)

        assert "400" in str(exc_info.value)
        assert (
            "The query ID does not exist, or you do not have the required permissions"
            in str(exc_info.value)
        )

    @responses.activate
    def test_saved_searches_unauthorized(self, bad_saved_search_mock, scw):

        with pytest.raises(ValueError) as exc_info:
            scw.get_saved_searches()

        assert "401" in str(exc_info.value)
        assert "Unauthorized" in str(exc_info.value)
