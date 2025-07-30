from typing import Optional

from vijil.api import BASE_URL, make_api_request


class VijilClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key

    def get_latest_objects_version(self):
        """
        Get the current objects version
        """
        try:
            response = make_api_request(
                base_url=self.base_url,
                endpoint="harness-configs/versions",
                token=self.api_key,
            )
            return response.get("results", [None])[0]
        except Exception as e:
            raise ValueError(
                f"An error occured while trying to get the latest version number : {e}"
            )
