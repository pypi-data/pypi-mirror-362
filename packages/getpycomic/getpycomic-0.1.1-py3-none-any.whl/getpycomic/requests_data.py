# -*- coding: utf-8 -*-
"""
"""

import requests

import io

from typing import Union


class RequestsData:

    def request_data(
        header: dict,
        link: str,
    ) -> Union[io.BytesIO, None]:
        """
        """
        # disable warning verify False
        requests.packages.urllib3.disable_warnings()

        req = requests.get(link, headers=header, verify=False)
        if req.status_code == 200:
            if 'image' in req.headers.get("Content-Type", ""):
                return io.BytesIO(req.content)
        else:
            return None
