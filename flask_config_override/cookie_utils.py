import json
import urllib


def cookie_to_json(encoded_cookie):
    if not encoded_cookie:
        return {}
    decoded_cookie = urllib.unquote(encoded_cookie)
    return json.loads(decoded_cookie)


def json_to_cookie(data):
    json_data = json.dumps(data)

    # excludes safe chars, they will be quoted in the various cookies
    # that we set (for example: the 'stats' cookie that contains urls like
    # http://deliveryherosite.world/ will become:
    #
    # 'http:%2F%2Fdeliveryherosite.world%2F'
    return urllib.quote(json_data, safe='')
