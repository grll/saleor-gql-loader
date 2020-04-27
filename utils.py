"""Module to define some utils non related to business logic.

Notes
-----
The function defined here must be context and implementation independant, for
easy reusability
"""
import requests
import json

GQL_DEFAULT_ENDPOINT = "http://localhost:8000/graphql/"


def graphql_request(query, variables={}, headers={},
                    endpoint=GQL_DEFAULT_ENDPOINT):
    """Execute the graphQL `query` provided on the `endpoint`.

    Parameters
    ----------
    query : str
        docstring representing a graphQL query.
    variables : dict, optional
        dictionary corresponding to the input(s) of the `query` must be
        serializable by requests into a JSON object.
    headers : dict, optional
        headers added to the request (important for authentication).
    endpoint : str, optional
        the graphQL endpoint url that will be queried, default is
        `GQL_DEFAULT_ENDPOINT`.

    Returns
    -------
    response : dict
        a dictionary corresponding to the parsed JSON graphQL response.

    Raises
    ------
    Exception
        when `response.status_code` is not 200.
    """
    response = requests.post(
        endpoint,
        headers=headers,
        json={
            'query': query,
            'variables': variables
        }
    )

    parsed_response = json.loads(response.text)
    if response.status_code != 200:
        raise Exception("{message}\n extensions: {extensions}".format(
            **parsed_response["errors"][0]))
    else:
        return parsed_response


def override_dict(a, overrides):
    """Override a dict with another one **only first non nested keys**.

    Notes
    -----
    This works only with non-nested dict. If dictionarries are nested then the
    nested dict needs to be completly overriden.
    The Operation is performed inplace.

    Parameters
    ----------
    a : dict
        a dictionary to merge.
    overrides : dict
        another dictionary to merge.
    """
    for key, val in overrides.items():
        try:
            if type(a[key]) == dict:
                print(
                    "**warning**: key '{}' contained a dict make sure to override each value in the nested dict.".format(key))
        except KeyError:
            pass
        a[key] = val


def handle_errors(errors):
    """Handle a list of errors as dict with keys message and field.

    Parameters
    ----------
    error : list
        a list of errors each error must be a dict with at least the following
        keys: `field` and `message`

    Raises
    ------
    Exception
        when the list is not empty and display {field} : {message} errors.
    """
    if len(errors) > 0:
        txt_list = [
            "{field} : {message}".format(**error) for error in errors]
        raise Exception("\n".join(txt_list))
