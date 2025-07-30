import json


class ResObj:
    __res = None

    def __init__(self, data=None, message='', code=200):
        self.__res = {
            "code": code,
            "msg": message,
            "data": data
        }

    def json_res(self):
        return json.dumps(self.__res, ensure_ascii=False)

    def get_res(self):
        return self.__res