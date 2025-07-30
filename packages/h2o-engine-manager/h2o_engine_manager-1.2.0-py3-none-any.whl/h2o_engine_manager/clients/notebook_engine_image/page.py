import pprint

from h2o_engine_manager.clients.notebook_engine_image.image import from_api_object
from h2o_engine_manager.gen.model.v1_list_notebook_engine_images_response import (
    V1ListNotebookEngineImagesResponse,
)


class NotebookEngineImagesPage:
    """
    Represents a list of NotebookEngineImages together with a next_page_token for listing all NotebookEngineImages.
    """

    def __init__(self, list_api_response: V1ListNotebookEngineImagesResponse) -> None:
        api_objects = list_api_response.notebook_engine_images
        self.notebook_engine_images = []
        for api_version in api_objects:
            self.notebook_engine_images.append(from_api_object(api_version))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
