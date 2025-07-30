#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:47 p.m.
"""Dictionary creator

This file allows the user to create a custom dictionary in order to
generate reports.

This file requires the following imports: 'inspect',
'time', 'datetime', 'requests'.

This file contains the following functions:
    * new_dict - returns a custom dictionary for better readability
"""

import inspect
import time
import datetime
import requests


def new_dict(start: 'datetime.datetime',
             end: 'datetime.datetime',
             json_method: 'str',
             response: 'requests.models.Response') -> dict:
    """
    Returns a custom dictionary based on the given parameters in order to generate the report.

    Parameters
    ----------
    start : datetime.datetime
        Request's start time
    end : datetime.datetime
        Request's end time
    json_method : str
        HTTP method name
    response : requests.models.Response
        Response obtained from the API call

    Returns
    -------
    dict
        Custom dictionary with the following items:

        Start : datetime.datetime -> Request's start time
        End : datetime.datetime -> Request's end time
        MethodName : str -> Function that called new_dict function
        Method : str -> HTTP method name
        Result : int -> 0 for successful responses, 1 for the rest
        Response : str -> String containing the response obtained from the API call
        StatusCode : str -> Response's status code
        StatusMessage : str -> Response's status message
        Content : str -> Response's text message
    """
    return {'Start': start,
            'End': end,
            'MethodName': inspect.currentframe().f_back.f_code.co_name,
            'Method': json_method,
            'Result': 0 if str(response.status_code).startswith('20') else 1,
            'Response': time.strftime('%T ', time.localtime()) + str(response) + ' "' + str(
                response.reason) + '": ' + str(response.text),
            'StatusCode': str(response.status_code),
            'StatusMessage': str(response.reason),
            'Content': str(response.text)}
