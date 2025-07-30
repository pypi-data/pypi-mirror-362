#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 03/10/2022
#  Time: 03:19 p. m.
"""Simple REST

This file allows the user to send simple REST requests using "requests"
module.

This file requires the following imports: 'requests'.

This file contains the following functions:
    * post_request - returns a POST request response
    * get_request - returns a GET request response
"""

import requests


def post_request(url: 'str', payload: 'list', headers: 'dict'):
    """
    Makes a simple POST request.

    Parameters
    ----------
    url : str
        Host URL
    payload : list
        JSON payload
    headers : dict
        Request's additional headers

    Returns
    -------
    requests.models.Response
        POST request response
    """

    # POST request
    response = requests.post(url=url, data=payload, headers=headers)

    return response


def get_request(url: 'str', headers: 'dict'):
    """
    Makes a simple GET request.

    Parameters
    ----------
     url : str
        Host URL
    headers : dict
        Request's additional headers

    Returns
    -------
    requests.models.Response
        GET request response
    """

    # GET request
    response = requests.get(url=url, headers=headers)

    return response
