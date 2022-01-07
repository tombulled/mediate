import mediate
import requests
import pprint

session = requests.Session()
middleware = mediate.Middleware()

@middleware
def add_param(call_next, request):
    request.params['foo'] = 'bar'

    return call_next(request)

session.prepare_request = middleware.bind(session.prepare_request)

resp = session.get('https://httpbin.org/get')

pprint.pprint(resp.json())
