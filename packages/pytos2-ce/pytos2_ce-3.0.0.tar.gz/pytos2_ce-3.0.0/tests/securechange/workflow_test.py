import pytest
import json
import responses

from pytos2.securechange.workflow import (
    BasicWorkflowInfo,
    WorkflowType,
    FullWorkflow,
    FullARWorkflow,
)


class TestWorkflows:
    @responses.activate
    def test_get_workflows(self, workflows_mock, scw):
        workflows = scw.get_workflows()
        assert workflows[0].id == 588
        assert workflows[0].name == "Contoso"
        assert workflows[0].description == ""
        assert workflows[0].type == WorkflowType.ACCESS_REQUEST
        unique_types = sorted(set([w.type.value for w in workflows]))
        assert unique_types == [
            WorkflowType.ACCESS_REQUEST.value,
            WorkflowType.GENERIC.value,
        ]

        workflows = scw.get_workflows(workflow_type=WorkflowType.ACCESS_REQUEST)
        assert workflows[0].id == 588
        assert workflows[0].name == "Contoso"
        assert workflows[0].description == ""
        assert workflows[0].type == WorkflowType.ACCESS_REQUEST
        unique_types = sorted(set([w.type.value for w in workflows]))
        assert unique_types == [WorkflowType.ACCESS_REQUEST.value]

    @responses.activate
    def test_get_workflow(self, workflows_mock, scw):
        workflow = scw.get_workflow(586)
        assert isinstance(workflow, FullWorkflow)
        assert isinstance(workflow, FullARWorkflow)
        assert workflow.id == 586
        assert workflow.name == "Fully automated Firewall change request"

        workflow = scw.get_workflow(
            workflow_name="Fully automated Firewall change request"
        )
        assert isinstance(workflow, FullWorkflow)
        assert workflow.id == 586
        assert workflow.name == "Fully automated Firewall change request"

        workflow = scw.get_workflow(600)
        assert isinstance(workflow, FullWorkflow)
        assert type(workflow) is not FullARWorkflow
        assert workflow.id == 600
        assert workflow.name == "Generic Workflow"

        workflow = scw.get_workflow(workflow_name="Generic Workflow")
        assert isinstance(workflow, FullWorkflow)
        assert type(workflow) is not FullARWorkflow
        assert workflow.id == 600
        assert workflow.name == "Generic Workflow"
