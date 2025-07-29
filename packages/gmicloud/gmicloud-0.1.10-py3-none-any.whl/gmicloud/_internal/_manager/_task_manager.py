import os

from .._client._iam_client import IAMClient
from .._client._task_client import TaskClient
from .._models import *

import time
import logging

logger = logging.getLogger(__name__)

class TaskManager:
    """
    TaskManager handles operations related to tasks, including creation, scheduling, and stopping tasks.
    """

    def __init__(self, iam_client: IAMClient):
        """
        Initialize the TaskManager instance and the associated TaskClient.

        :param iam_client: The IAMClient instance used for authentication
        """
        self.iam_client = iam_client
        self.task_client = TaskClient(iam_client)

    def get_task(self, task_id: str) -> Task:
        """
        Retrieve a task by its ID.

        :param task_id: The ID of the task to retrieve.
        :return: A `Task` object containing the details of the task.
        :raises ValueError: If `task_id` is invalid (None or empty string).
        """
        self._validate_not_empty(task_id, "Task ID")

        return self.task_client.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve a list of all tasks available in the system.

        :return: A list of `Task` objects.
        """
        resp = self.task_client.get_all_tasks()
        if not resp or not resp.tasks:
            return []

        return resp.tasks

    def create_task(self, task: Task) -> Task:
        """
        Create a new task.

        :param task: A `Task` object containing the details of the task to be created.
        :return: A `Task` object containing the details of the created task.
        :rtype: Task
        :raises ValueError: If `task` is None.
        """
        self._validate_task(task)
        if not task.owner:
            task.owner = TaskOwner(user_id=self.iam_client.get_user_id())
        resp = self.task_client.create_task(task)
        if not resp or not resp.task:
            raise ValueError("Failed to create task.")

        logger.info(f"Task created: {resp.task.task_id}")
        return resp.task
    
    def create_task_from_artifact_id(self, artifact_id: str, replica_resource: ReplicaResource, task_scheduling: TaskScheduling) -> Task:
        """
        Create a new task using the configuration data from a file.
        """
        # Create Task based on Artifact
        new_task = Task(
            config=TaskConfig(
                ray_task_config=RayTaskConfig(
                    artifact_id=artifact_id,
                    file_path="serve",
                    deployment_name="app",
                    replica_resource=replica_resource,
                ),
                task_scheduling = task_scheduling,
            ),
        )
        return self.create_task(new_task).task_id

    def create_task_from_file(self, artifact_id: str, config_file_path: str, trigger_timestamp: int = None) -> Task:
        """
        Create a new task using the configuration data from a file.

        :param artifact_id: The ID of the artifact to be used in the task.
        :param config_file_path: The path to the file containing the task configuration data.
        :param trigger_timestamp: Optional, for one-off scheduling.
        :return: A `Task` object containing the details of the created task.
        :rtype: Task
        :raises ValueError: If the `file_path` is invalid or the file cannot be read.
        """
        self._validate_not_empty(artifact_id, "Artifact ID")
        self._validate_file_path(config_file_path)

        task = self._read_file_and_parse_task(config_file_path)
        task.config.ray_task_config.artifact_id = artifact_id

        if trigger_timestamp:
            task.config.task_scheduling.scheduling_oneoff.trigger_timestamp = trigger_timestamp

        return self.create_task(task)

    def update_task_schedule(self, task: Task) -> bool:
        """
        Update the schedule of an existing task.

        :param task: A `Task` object containing the updated schedule details.
        :return: None
        :raises ValueError: If `task` is None.
        """
        self._validate_task(task)
        self._validate_not_empty(task.task_id, "Task ID")

        return self.task_client.update_task_schedule(task)

    def update_task_schedule_from_file(self, artifact_id: str, task_id: str, config_file_path: str,
                                       trigger_timestamp: int = None) -> bool:
        """
        Update the schedule of an existing task using data from a file. The file should contain a valid task definition.

        :param artifact_id: The ID of the artifact to be used in the task.
        :param task_id: The ID of the task to update.
        :param config_file_path: The path to the file containing the task configuration data.
        :param trigger_timestamp: Optional, for one-off scheduling.
        :return: None
        :raises ValueError: If the `file_path` is invalid or the file cannot be read.
        """
        self._validate_not_empty(artifact_id, "Artifact ID")
        self._validate_not_empty(task_id, "Task ID")
        self._validate_file_path(config_file_path)

        task = self._read_file_and_parse_task(config_file_path)
        task.task_id = task_id
        task.config.ray_task_config.artifact_id = artifact_id

        if trigger_timestamp:
            task.config.task_scheduling.scheduling_oneoff.trigger_timestamp = trigger_timestamp

        return self.update_task_schedule(task)

    def start_task(self, task_id: str) -> bool:
        """
        Start a task by its ID.

        :param task_id: The ID of the task to be started.
        :return: None
        :raises ValueError: If `task_id` is invalid (None or empty string).
        """
        self._validate_not_empty(task_id, "Task ID")

        return self.task_client.start_task(task_id)
    

    def wait_for_task(self, task_id: str, timeout_s: int = 900) -> Task:
        """
        Wait for a task to reach the RUNNING state or raise an exception if it fails.

        :param task_id: The ID of the task to wait for.
        :param timeout_s: The timeout in seconds.
        :return: The task object.
        :rtype: Task
        """
        start_time = time.time()
        while True:
            try:
                task = self.get_task(task_id)
                if task.task_status == TaskStatus.RUNNING:
                    if task.endpoint_info is not None and task.endpoint_info.endpoint_status == TaskEndpointStatus.RUNNING:
                        return task
                    else:
                        if task.cluster_endpoints:
                            for ce in task.cluster_endpoints:
                                if ce.endpoint_status == TaskEndpointStatus.RUNNING:
                                    return task
                if task.task_status in [TaskStatus.NEEDSTOP, TaskStatus.ARCHIVED]:
                    raise Exception(f"Unexpected task status after starting: {task.task_status}")
                else:
                    logger.info(f"Pending task starting. Task status: {task.task_status}")
            except Exception as e:
                logger.error(f"Failed to get task, Error: {e}")
            if time.time() - start_time > timeout_s:
                raise Exception(f"Task creation takes more than {timeout_s // 60} minutes. Testing aborted.")
            time.sleep(10)

    def start_task_and_wait(self, task_id: str, timeout_s: int = 3600) -> Task:
        """
        Start a task and wait for it to be ready.

        :param task_id: The ID of the task to start.
        :param timeout_s: The timeout in seconds.
        :return: The task object.
        :rtype: Task
        """
        try:
            self.start_task(task_id)
            logger.info(f"Started task ID: {task_id}")
        except Exception as e:
            logger.error(f"Failed to start task, Error: {e}")
            raise e

        return self.wait_for_task(task_id, timeout_s)

    def stop_task(self, task_id: str) -> bool:
        """
        Stop a task by its ID.

        :param task_id: The ID of the task to be stopped.
        :return: None
        :raises ValueError: If `task_id` is invalid (None or empty string).
        """
        self._validate_not_empty(task_id, "Task ID")
        return self.task_client.stop_task(task_id)

        
    def stop_task_and_wait(self, task_id: str, timeout_s: int = 3600):
        try:
            self.stop_task(task_id)
            logger.info(f"Stopping task ID: {task_id}")
        except Exception as e:
            logger.error(f"Failed to stop task, Error: {e}")
        start_time = time.time()
        while True:
            try:
                task = self.get_task(task_id)
                if task.task_status == TaskStatus.IDLE:
                    break
            except Exception as e:
                logger.error(f"Failed to get task, Error: {e}")
            if time.time() - start_time > timeout_s:
                raise Exception(f"Task stopping takes more than {timeout_s // 60} minutes. Testing aborted.")
            time.sleep(10)

    def get_task_endpoint_url(self, task_id: str) -> str:
        task = self.get_task(task_id)
        if task.endpoint_info is not None and task.endpoint_info.endpoint_status == TaskEndpointStatus.RUNNING:
            return task.endpoint_info.endpoint_url
        else:
            if task.cluster_endpoints:
                for ce in task.cluster_endpoints:
                    if ce.endpoint_status == TaskEndpointStatus.RUNNING:
                        return ce.endpoint_url
            return ""


    def get_usage_data(self, start_timestamp: str, end_timestamp: str) -> GetUsageDataResponse:
        """
        Retrieve the usage data of a task within a given time range.

        :param start_timestamp: The start timestamp of the usage data.
        :param end_timestamp: The end timestamp of the usage data.
        :return: A `GetUsageDataResponse` object containing the usage data.
        """
        self._validate_not_empty(start_timestamp, "Start timestamp")
        self._validate_not_empty(end_timestamp, "End timestamp")

        return self.task_client.get_usage_data(start_timestamp, end_timestamp)

    def archive_task(self, task_id: str) -> bool:
        """
        Archive a task by its ID.

        :param task_id: The ID of the task to be archived.
        :return: None
        :raises ValueError: If `task_id` is invalid (None or empty string).
        """
        self._validate_not_empty(task_id, "Task ID")

        return self.task_client.archive_task(task_id)

    @staticmethod
    def _validate_not_empty(value: str, name: str):
        """
        Validate a string is neither None nor empty.

        :param value: The string to validate.
        :param name: The name of the value for error reporting.
        """
        if not value or not value.strip():
            raise ValueError(f"{name} is required and cannot be empty.")

    @staticmethod
    def _validate_task(task: Task) -> None:
        """
        Validate a Task object.

        :param task: The Task object to validate.
        :raises ValueError: If `task` is None.
        """
        if task is None:
            raise ValueError("Task object is required and cannot be None.")

    @staticmethod
    def _validate_file_path(file_path: str) -> None:
        """
        Validate the file path.

        :param file_path: The file path to validate.
        :raises ValueError: If `file_path` is None, empty, or does not exist.
        """
        if not file_path or not file_path.strip():
            raise ValueError("File path is required and cannot be empty.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    def _read_file_and_parse_task(self, file_path: str) -> Task:
        """
        Read a file and parse it into a Task object.

        :param file_path: The path to the file to be read.
        :return: A `Task` object parsed from the file content.
        :raises ValueError: If the file is invalid or cannot be parsed.
        """
        self._validate_file_path(file_path)

        with open(file_path, "rb") as file:
            file_data = file.read()

        try:
            task = Task.model_validate_json(file_data)  # Ensure Task has a static method for model validation.
        except Exception as e:
            raise ValueError(f"Failed to parse Task from file: {file_path}. Error: {str(e)}")

        return task
