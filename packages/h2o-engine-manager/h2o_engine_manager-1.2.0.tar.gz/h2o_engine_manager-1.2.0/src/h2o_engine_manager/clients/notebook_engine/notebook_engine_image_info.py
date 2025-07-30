from datetime import datetime
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.base.image_pull_policy import (
    from_image_pull_policy_api_object,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_image_info import (
    V1NotebookEngineImageInfo,
)


class NotebookEngineImageInfo:
    """
    Contains original data from the NotebookEngineImage used in NotebookEngine.
    """

    def __init__(
        self,
        name: str = "",
        display_name: str = "",
        image: str = "",
        enabled: bool = False,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: Optional[List[str]] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
    ):
        if image_pull_secrets is None:
            image_pull_secrets = []

        self.name = name
        self.display_name = display_name
        self.image = image
        self.enabled = enabled
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name


def notebook_engine_image_info_from_api_object(
    api_object: Optional[V1NotebookEngineImageInfo]
) -> Optional[NotebookEngineImageInfo]:
    if api_object is None:
        return None

    return NotebookEngineImageInfo(
        name=api_object.name,
        display_name=api_object.display_name,
        image=api_object.image,
        enabled=api_object.enabled,
        image_pull_policy=from_image_pull_policy_api_object(api_object.image_pull_policy),
        image_pull_secrets=api_object.image_pull_secrets,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
    )
