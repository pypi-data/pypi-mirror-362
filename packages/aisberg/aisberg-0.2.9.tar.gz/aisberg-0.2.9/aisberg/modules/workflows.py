from typing import List, Union, Generator, AsyncGenerator, Coroutine, Any
from abc import ABC

from ..models.workflows import (
    Workflow,
    WorkflowDetails,
    WorkflowRunChunk,
    WorkflowRunResult,
)

from abc import abstractmethod
from ..abstract.modules import SyncModule, AsyncModule
from ..api import endpoints, async_endpoints


class AbstractWorkflowsModule(ABC):
    def __init__(self, parent, client):
        self._parent = parent
        self._client = client

    @abstractmethod
    def get(self) -> List[Workflow]:
        """Get a list of available workflows.

        Returns:
            List[dict]: A list of available workflows.

        Raises:
            Exception: If there is an error fetching the workflows.
        """
        ...

    @abstractmethod
    def details(self, workflow_id: str) -> WorkflowDetails:
        """Get details of a specific workflow.

        Args:
            workflow_id (str): The ID of the workflow to retrieve.

        Returns:
            WorkflowDetails: The details of the specified workflow.

        Raises:
            ValueError: If the workflow with the specified ID is not found.
            Exception: If there is an error fetching the workflow details.
        """
        ...

    @abstractmethod
    def run(self, workflow_id: str, data: dict = None, stream: bool = False):
        """
        Run a workflow with the given ID and data.
        If `stream` is True, it will yield chunks of the workflow run.
        If `stream` is False, it will return the final result of the workflow run.

        Args:
            workflow_id (str): The ID of the workflow to run.
            data (dict, optional): The input data for the workflow. Defaults to None.
            stream (bool, optional): If True, returns a generator yielding chunks of the workflow run. Defaults to False.

        Returns:
            Union[Generator[WorkflowRunChunk, None, None], WorkflowRunResult]:
                If `stream` is True, a generator yielding chunks of the workflow run.
                If `stream` is False, the final result of the workflow run.

        Raises:
            ValueError: If the workflow with the specified ID is not found.
            Exception: If there is an error running the workflow.
        """
        ...


class SyncWorkflowsModule(SyncModule, AbstractWorkflowsModule):
    def __init__(self, parent, client):
        SyncModule.__init__(self, parent, client)
        AbstractWorkflowsModule.__init__(self, parent, client)

    def get(self) -> List[Workflow]:
        return endpoints.workflows(self._client)

    def details(self, workflow_id: str) -> WorkflowDetails:
        return endpoints.workflow(self._client, workflow_id)

    def run(
        self, workflow_id: str, data: dict = None, stream: bool = False
    ) -> Union[Generator[WorkflowRunChunk, None, None], WorkflowRunResult]:
        if stream:
            return self._run_stream(workflow_id, data)
        else:
            return self._run_once(workflow_id, data)

    def _run_stream(
        self, workflow_id: str, data: dict = None
    ) -> Generator[WorkflowRunChunk, None, None]:
        for chunk in endpoints.run_workflow(self._client, workflow_id, data):
            yield WorkflowRunChunk.model_validate(chunk)

    def _run_once(self, workflow_id: str, data: dict = None) -> WorkflowRunResult:
        last_response = None
        for chunk in endpoints.run_workflow(self._client, workflow_id, data):
            last_response = chunk
        return WorkflowRunResult.model_validate(last_response)


class AsyncWorkflowsModule(AsyncModule, AbstractWorkflowsModule):
    def __init__(self, parent, client):
        AsyncModule.__init__(self, parent, client)
        AbstractWorkflowsModule.__init__(self, parent, client)

    async def get(self) -> List[Workflow]:
        return await async_endpoints.workflows(self._client)

    async def details(self, workflow_id: str) -> WorkflowDetails:
        return await async_endpoints.workflow(self._client, workflow_id)

    def run(
        self, workflow_id: str, data: dict = None, stream: bool = False
    ) -> Union[
        AsyncGenerator[WorkflowRunChunk, None], Coroutine[Any, Any, WorkflowRunResult]
    ]:
        if stream:
            return self._run_stream(workflow_id, data)
        else:
            return self._run_once(workflow_id, data)

    async def _run_stream(
        self, workflow_id: str, data: dict = None
    ) -> AsyncGenerator[WorkflowRunChunk, None]:
        async for chunk in async_endpoints.run_workflow(
            self._client, workflow_id, data
        ):
            yield WorkflowRunChunk.model_validate(chunk)

    async def _run_once(self, workflow_id: str, data: dict = None) -> WorkflowRunResult:
        last_response = None
        async for chunk in async_endpoints.run_workflow(
            self._client, workflow_id, data
        ):
            last_response = chunk
        return WorkflowRunResult.model_validate(last_response)
