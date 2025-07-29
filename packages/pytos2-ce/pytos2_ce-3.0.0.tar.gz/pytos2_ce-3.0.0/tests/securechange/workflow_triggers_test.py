import pytest
import responses

from pytos2.securechange.workflow_triggers import (
    Script,
    Workflow,
    Trigger,
    WorkflowTrigger,
)


class TestWorkflowTrigger:
    @responses.activate
    def test_get_triggers(self, workflow_triggers_mock, scw):
        workflow_triggers = scw.get_triggers()

        assert workflow_triggers[0].name == "Test Integration"
        assert workflow_triggers[0].script.path == ""
        assert (
            workflow_triggers[0].script.arguments
            == "/opt/tufin/securitysuite/ps/bin/attach_test_report_to_ticket.py"
        )
        assert workflow_triggers[0].triggers[0].name == "New trigger group"
        assert workflow_triggers[0].triggers[0].workflow.name == "AR_MG"
        assert workflow_triggers[0].triggers[0].workflow.parent_workflow_id == 426
        assert workflow_triggers[0].triggers[0].events == ["CREATE", "ADVANCE"]

        assert workflow_triggers[1].name == "Test One"
        assert (
            workflow_triggers[1].script.path
            == "test-one-solutions/populate-access-request"
        )
        assert workflow_triggers[1].script.arguments == ""
        assert workflow_triggers[1].triggers[0].name == "Test One"
        assert workflow_triggers[1].triggers[0].workflow.name == "Test One"
        assert workflow_triggers[1].triggers[0].workflow.parent_workflow_id == 595
        assert workflow_triggers[1].triggers[0].events == ["REOPEN"]

    @responses.activate
    def test_get_trigger(self, workflow_triggers_mock, scw):
        workflow_trigger = scw.get_trigger(id=4)

        assert workflow_trigger.name == "Test Integration"
        assert workflow_trigger.script.path == ""
        assert (
            workflow_trigger.script.arguments
            == "/opt/tufin/securitysuite/ps/bin/attach_test_report_to_ticket.py"
        )
        assert workflow_trigger.triggers[0].name == "New trigger group"
        assert workflow_trigger.triggers[0].workflow.name == "AR_MG"
        assert workflow_trigger.triggers[0].workflow.parent_workflow_id == 426
        assert workflow_trigger.triggers[0].events == ["CREATE", "ADVANCE"]

        workflow_trigger = scw.get_trigger(name="Contoso")

        assert workflow_trigger.name == "Test One"
        assert (
            workflow_trigger.script.path == "test-one-solutions/populate-access-request"
        )
        assert workflow_trigger.script.arguments == ""
        assert workflow_trigger.triggers[0].name == "Test One"
        assert workflow_trigger.triggers[0].workflow.name == "Test One"
        assert workflow_trigger.triggers[0].workflow.parent_workflow_id == 595
        assert workflow_trigger.triggers[0].events == ["REOPEN"]

        with pytest.raises(ValueError) as e:
            scw.get_trigger()

        with pytest.raises(ValueError) as e:
            scw.get_trigger(id=4, name="Test One")

    @responses.activate
    def test_add_trigger(self, workflow_triggers_mock, scw):
        script = Script(path="test-solution/test-solution", arguments="")
        workflow = Workflow(name="test workflow", parent_workflow_id=1)
        trigger = Trigger(
            name="test trigger", workflow=workflow, events=["CREATE", "ADVANCE"]
        )
        workflow_trigger = WorkflowTrigger(
            name="test", script=script, triggers=[trigger]
        )
        scw.add_trigger(workflow_trigger)
