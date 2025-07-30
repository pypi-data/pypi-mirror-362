import pprint
from datetime import datetime
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.base.image_pull_policy import (
    from_image_pull_policy_api_object,
)
from h2o_engine_manager.gen.model.required_notebook_engine_image_resource import (
    RequiredNotebookEngineImageResource,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_image import V1NotebookEngineImage


class NotebookEngineImage:
    """
    NotebookEngineImage represents image that can be used in Notebook.
    """

    def __init__(
        self,
        image: str,
        name: str = "",
        display_name: str = "",
        enabled: bool = True,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: Optional[List[str]] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
    ):
        """
        NotebookEngineImage represents image that can be used in Notebook.

        Args:
            image: Docker image name.
            name: Resource name. Format "workspaces/*/NotebookEngineImages/*".
            display_name: Human-readable name of the NotebookEngineImage.
            enabled: Whether the NotebookEngineImage is enabled.
            image_pull_policy: Image pull policy applied when using this NotebookEngineImage.
                When unset, server will choose a default one.
            image_pull_secrets: List of references to k8s secrets that can be used for pulling an image
                of this NotebookEngineImage from a private container image registry or repository.
            create_time: Time when the NotebookEngineImage was created.
            update_time: Time when the NotebookEngineImage was last updated.
            creator: Name of entity that created the NotebookEngineImage.
            updater: Name of entity that last updated the NotebookEngineImage.
            creator_display_name: Human-readable name of entity that created the NotebookEngineImage.
            updater_display_name: Human-readable name of entity that last updated the NotebookEngineImage.
        """
        if image_pull_secrets is None:
            image_pull_secrets = []

        self.name = name
        self.image = image
        self.enabled = enabled
        self.display_name = display_name
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self) -> V1NotebookEngineImage:
        return V1NotebookEngineImage(
            image=self.image,
            enabled=self.enabled,
            display_name=self.display_name,
            image_pull_policy=self.image_pull_policy.to_api_object(),
            image_pull_secrets=self.image_pull_secrets,
        )

    def to_resource(self) -> RequiredNotebookEngineImageResource:
        return RequiredNotebookEngineImageResource(
            image=self.image,
            enabled=self.enabled,
            display_name=self.display_name,
            image_pull_policy=self.image_pull_policy.to_api_object(),
            image_pull_secrets=self.image_pull_secrets,
        )


def from_api_object(api_object: V1NotebookEngineImage) -> NotebookEngineImage:
    return NotebookEngineImage(
        image=api_object.image,
        name=api_object.name,
        enabled=api_object.enabled,
        display_name=api_object.display_name,
        image_pull_policy=from_image_pull_policy_api_object(api_object.image_pull_policy),
        image_pull_secrets=api_object.image_pull_secrets,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
    )


def from_api_objects(api_objects: List[V1NotebookEngineImage]) -> List[NotebookEngineImage]:
    return [from_api_object(api_object) for api_object in api_objects]
