import requests
def check_status_code(request):
    if request.status_code != 200:
        raise Exception(request.json()['message'])
