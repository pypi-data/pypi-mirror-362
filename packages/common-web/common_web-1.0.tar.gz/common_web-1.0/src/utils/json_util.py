import json


def __json_2_dict(request):
    """
    将请求参数json转换为dict,用于解析请求参数
    """
    return json.loads(request.body.decode())
