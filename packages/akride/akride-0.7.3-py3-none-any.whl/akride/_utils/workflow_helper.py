from datetime import datetime
from typing import Tuple
from uuid import uuid4


class WorkflowHelper:
    @staticmethod
    def get_session_and_workflow_id(
        workflow_id_prefix: str, dataset_id: str
    ) -> Tuple[str, str]:
        session_id = (
            datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            + "-"
            + str(dataset_id)
        )
        workflow_id = f"{workflow_id_prefix}_{uuid4().hex}"

        return session_id, workflow_id
