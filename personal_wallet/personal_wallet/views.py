import json

from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .utils_for_urls import URLS_FOR_FRONTEND


@api_view(['GET'])
def get_all_urls(request: HttpRequest) -> Response:
    """
    View that return a json object with all project urls.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    Response: JSON object with all project urls.
    """
    return Response(data=json.dumps(URLS_FOR_FRONTEND), status=HTTP_200_OK)
