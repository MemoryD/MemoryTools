import time
import threading
import pyperclip as p
import easygui as g
from aip import AipOcr
from PIL import Image, ImageGrab
from io import BytesIO
from setting import *
from utils import *

# APP_ID = '18054283'
# API_KEY = 'UnwUzcDzzMcR6smt5xm9vIwi'
# SECRET_KEY = '755vO7iZGV0DDIlzH7DHpkWjGDOBZzav'

class OCR(object):
    def __init__(self, root):
        self.root = root
        self.is_pause = False
        config = read_config()
        ocr = config['ocr']
        self.client = AipOcr(ocr['APP_ID'], ocr['API_KEY'], ocr['SECRET_KEY'])

    def result_ok(self, dic_result):
        return 'words_result' in dic_result

    def pause_ocr(self, sysTrayIcon):
        self.is_pause = not self.is_pause
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def pause_text(self):
        return "开启OCR" if self.is_pause else "暂停OCR"

    def setting(self, sysTrayIcon):
        msg = "需要设置百度AI平台(https://ai.baidu.com/)的API才能进行OCR识别"
        title = "设置百度API"
        fieldNames = ["*APP_ID","*API_KEY","*SECRET_KEY"]
        fieldValues = []
        fieldValues = g.multenterbox(msg, title, fieldNames)
        #print(fieldValues)
        while True:
            if fieldValues == None:
                break
            errmsg = ""
            for i in range(len(fieldNames)):
                option = fieldNames[i].strip()
                if fieldValues[i].strip() == "" and option[0] == "*":
                    errmsg += ("【%s】为必填项   " %fieldNames[i])
            if errmsg == "":
                break
            fieldValues = g.multenterbox(errmsg, title, fieldNames, fieldValues)
        
        if fieldValues:
            config = read_config()
            ocr = config['ocr']
            ocr['APP_ID'] = fieldValues[0]
            ocr['API_KEY'] = fieldValues[1]
            ocr['SECRET_KEY'] = fieldValues[2]
            config['ocr'] = ocr
            write_config(config)
            self.client = AipOcr(ocr['APP_ID'], ocr['API_KEY'], ocr['SECRET_KEY'])

    def image2text(self, image):
        '''
        先使用精确版API，如果次数到了，再使用普通版。
        '''
        dic_result = self.client.basicAccurate(image)
        if self.result_ok(dic_result):
            res = dic_result['words_result']
        else:
            dic_result = self.client.basicGeneral(image)
            if self.result_ok(dic_result):
                res = dic_result['words_result']
            else:
                result = str(dic_result)
                return result

        result = ''
        for m in res:
            result = result + str(m['words']) + '\n'

        return result

    def start(self):
        while True:
            time.sleep(0.2)
            if self.is_pause:
                continue
            im = ImageGrab.grabclipboard()          # 获取剪切板

            if isinstance(im, Image.Image):         # 判断是否是图片
                bf = BytesIO()
                im.save(bf, 'png')
                try:
                    text = self.image2text(bf.getvalue())
                except Exception as e:
                    text = str(e)

                p.copy('')
                button = g.textbox(msg='OCR 识别结果, 可以直接编辑修改。', title="OCR 识别结果", text=text)
                if button:
                    p.copy(text)

    def run(self):
        thread = threading.Thread(target=self.start)
        thread.setDaemon(True)
        thread.start()

if __name__ == '__main__':
    OCR().start()
