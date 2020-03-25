# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 18:29
# @Author  : Octan3
# @Email   : Octan3@stu.ouc.edu.cn
# @File    : Pic2py.py
# @Software: PyCharm

import base64


def pic2py(picture_names, py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        print(picture_name)
        filename = picture_name.replace('.', '_')
        open_pic = open("%s" % picture_name, 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    with open('%s.py' % py_name, 'w+') as f:
        for data in write_data:
            f.write(data)


if __name__ == '__main__':
    pics = ["trans.ico", 'about.ico', 'check.ico', 'clock.ico', 'ocr.ico', 'pick.ico', 'exit.ico']
    pic2py(pics, 'pic')
    print("ok")
