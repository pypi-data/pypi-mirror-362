"""OpenWebUI models class for handling model operations."""

import logging
from typing import List, Optional

import httpx
from openai._base_client import make_request_options
from openai._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from openai.pagination import SyncPage
from openai.resources.models import Models
from openai.types.model import Model

_logger = logging.getLogger(__name__)


class OpenWebUIModel(Model):
    """Extended Model class for OpenWebUI that includes the human-readable name field."""

    name: Optional[str] = None
    """Human-readable name of the model."""


class OpenWebUIModels(Models):
    """Extended Models class for OpenWebUI API compatibility."""

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> List[OpenWebUIModel]:
        """
        Lists the currently available models from OpenWebUI.

        This method overrides the OpenAI implementation to handle the different response format
        from OpenWebUI's API.
        """
        _logger.debug("Fetching models from OpenWebUI")

        response = self._get_api_list(
            path="/models",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            page=SyncPage[OpenWebUIModel],
            model=OpenWebUIModel,
        )
        return list(response)
