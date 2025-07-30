import pprint

from h2o_engine_manager.clients.notebook_engine.engine import (
    notebook_engine_from_api_object,
)
from h2o_engine_manager.gen.model.v1_list_notebook_engines_response import (
    V1ListNotebookEnginesResponse,
)


class NotebookEnginesPage:
    """
    NotebookEnginesPage is a list of NotebookEngines together with a next_page_token for listing the next page of
    NotebookEngines.
    """

    def __init__(
        self,
        list_api_response: V1ListNotebookEnginesResponse,
    ):
        api_objects = list_api_response.notebook_engines
        self.notebook_engines = []
        for api_notebook_engine in api_objects:
            self.notebook_engines.append(notebook_engine_from_api_object(api_object=api_notebook_engine))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
