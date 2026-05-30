import requests
import warnings

def _generateBareUrl(integrationType, integrationID):
    return r'https://api.easybase.io/' + integrationType + r"/" + integrationID

def get(integrationID: str, offset: int=None, limit: int=None, authentication: int=None, customQuery: dict={}):
    """
    :param integrationID: EasyBase integration ID. Can be found by expanding the integration menu. This id is automatically generated.
    :param offset: Edit starting index from which records will be retrieved from. Useful for paging.
    :param limit: Limit the amount of records to be retrieved. Can be used in combination with offset.
    :param authentication: Custom authentication string. Can be set in integration menu. If it is set, it is required to access integration. This acts as an extra layer of security and extensibility.
    :param customQuery: This object can be set to overwrite the query values as set in the integration menu. If your query is setup to find records where 'age' >= 0, passing in { age: 50 } will query where 'age' >= 50.
    :return: Array of records.
    :rtype: list
    """
    body = {}
    body.update(customQuery)
    if offset != None: body['offset'] = offset
    if limit != None: body['limit'] = limit
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('get', integrationID), json=body)
        if 'ErrorCode' in r.json():
            warnings.warn(r.json()['message'])
            return [ r.json()['message'] ]
        else:
            return r.json()
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def post(integrationID: str, newRecord: dict, authentication: str=None, insertAtEnd: bool=None):
    """
    :param integrationID: EasyBase integration ID. Can be found by expanding the integration menu. This id is automatically generated.
    :param newRecord: Values to post to EasyBase collection. Format is { "column name": value }
    :param authentication: Custom authentication string. Can be set in integration menu. If it is set, it is required to access integration. This acts as an extra layer of security and extensibility.
    :param insertAtEnd: If true, record will be inserted at the end of the collection rather than the front.
    :return: Post status.
    :rtype: str
    """
    body = {}
    body.update(newRecord)
    if authentication != None: body['authentication'] = authentication
    if insertAtEnd != None: body['insertAtEnd'] = insertAtEnd

    try:
        r = requests.post(_generateBareUrl('post', integrationID), json=body)
        if 'ErrorCode' in r.json():
            warnings.warn(r.json()['message'])
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def update(integrationID: str, updateValues: dict, authentication: int=None, customQuery: dict={}):
    """
    :param integrationID: EasyBase integration ID. Can be found by expanding the integration menu. This id is automatically generated.
    :param updateValues: Values to update records with. Format is { "column_name": new value }
    :param authentication: Custom authentication string. Can be set in integration menu. If it is set, it is required to access integration. This acts as an extra layer of security and extensibility.
    :param customQuery: This object can be set to overwrite the query values as set in the integration menu. If your query is setup to find records where 'age' >= 0, passing in { age: 50 } will query where 'age' >= 50.
    :return: Update status.
    :rtype: str
    """
    body = { "updateValues": updateValues }
    body.update(customQuery)
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('update', integrationID), json=body)
        if 'ErrorCode' in r.json():
            warnings.warn(r.json()['message'])
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e


def delete(integrationID: str, authentication: int=None, customQuery: dict={}):
    """
    :param integrationID: EasyBase integration ID. Can be found by expanding the integration menu. This id is automatically generated.
    :param authentication: Custom authentication string. Can be set in integration menu. If it is set, it is required to access integration. This acts as an extra layer of security and extensibility.
    :param customQuery: This object can be set to overwrite the query values as set in the integration menu. If your query is setup to find records where 'age' >= 0, passing in { age: 50 } will query where 'age' >= 50.
    :return: Delete status.
    :rtype: str
    """
    body = {}
    body.update(customQuery)
    if authentication != None: body['authentication'] = authentication

    try:
        r = requests.post(_generateBareUrl('delete', integrationID), json=body)
        if 'ErrorCode' in r.json():
            warnings.warn(r.json()['message']) 
        return r.json()['message']
    except Exception as e:
        print("EasyBase exception: {}".format(e))
        return e