import requests


class BaseTrans(object):
    """docstring for BaseTrans"""
    def __init__(self, url, mode='post'):
        self.url = url
        self.mode = mode

    @classmethod
    def joinParams(self, params: dict) -> str:
        '''
        用于拼接参数。因为直接传递字典会返回图片模糊的结果，待解决。
        '''
        palist = []
        for k, v in params.items():
            palist.append('%s=%s' % (k, v))
        payload = '&'.join(palist)
        return payload

    def getData(self, params: dict, headers=None):
        payload = self.joinParams(params)
        print(payload)

        res = requests.post(self.url, params=payload, headers=headers)

        return res.json()

    def translate(self, sentence: str, src: str, dest: str) -> str:
        pass
