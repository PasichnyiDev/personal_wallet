from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .routes_util import routes_util


@api_view(['GET'])
def get_all_urls(request) -> Response:
    """
    View provides getting a json object with all project urls.

    :param: request: HttpRequest;

    :return: Response: JSON object with all project urls.
    """
    return Response(data=routes_util.get_all_project_urls(), status=HTTP_200_OK)
