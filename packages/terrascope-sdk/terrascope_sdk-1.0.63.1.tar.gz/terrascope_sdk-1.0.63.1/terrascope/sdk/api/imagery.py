
from google.protobuf.timestamp_pb2 import Timestamp
from terrascope_api import TerrascopeAsyncClient
from terrascope_api.models.imagery_pb2 import ImagerySearchRequest


class APIImagery:
    def __init__(self, client: TerrascopeAsyncClient, timeout):
        self.__timeout = timeout
        self.__client = client

    async def search(self,
                     geometry_wkb,
                     datetime_start,
                     datetime_end,
                     data_source_id,
                     product_spec_name,
                     search_service='SCENE',
                     ):
        """
        """

        time_range = ImagerySearchRequest.TimeRange(
            start_utc=Timestamp(seconds=int(datetime_start.timestamp())),
            finish_utc=Timestamp(seconds=int(datetime_end.timestamp()))
        )

        request = ImagerySearchRequest(
            geometry_wkb=geometry_wkb,
            time_range=time_range,
            data_source_id=data_source_id,
            product_spec_name=product_spec_name
        )
        request.data_source_filters.update({'SEARCH_SERVICE': search_service})
        response = await self.__client.api.imagery.search(request, timeout=self.__timeout)
        return response
