import PyV8

def create_vl5x(param):
    ctxt = PyV8.JSContext()
    ctxt.enter()
    js_file = open('E:\lga\dataanalysis\wenshu\wenshu\spiders\getKey.js', 'r')
    js_data = js_file.read()
    js_file.close()
    ctxt.eval(js_data.decode('GBK', 'ignore'))
    create_key = ctxt.locals.getKey
    key1 = create_key(param)
    return key1


def create_number(guid):
    import requests
    param = {'guid': str(guid)}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    r1 = requests.post('http://wenshu.court.gov.cn/ValiCode/GetCode', data=param, headers=headers)
    return r1.text
