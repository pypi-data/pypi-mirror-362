import time


def wait_for_rest(web_session, url, code, attempts=10):
    def pred(resp):
        return resp.status_code == code

    wait_for_response(web_session, url, pred, attempts)


def wait_for_response(web_session, url, resp_predicate, attempts=10):
    
    attempt=0
    attempt_limit=attempts
    response = None
    while attempt < attempt_limit:
        try:
            response = web_session.get(url, verify=False)
            print('code: {0}'.format(response.status_code))
            if resp_predicate(response):
                return
        except Exception as e:
            print(str(e))
        time.sleep(10)
        attempt = attempt + 1
    if response and response.text:
        print(response.text)
    raise Exception('exhausted')
