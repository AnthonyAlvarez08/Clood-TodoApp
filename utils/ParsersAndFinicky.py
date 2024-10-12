import json

def parse_request_data(request):
    """
    
    gets data from either a form or a json data
    
    """


    data = dict()
    if request.is_json:
        data = request.get_json()
        data = json.loads(data)
    else:
        data = request.values

    return data