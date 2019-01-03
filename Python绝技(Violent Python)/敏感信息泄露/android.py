# -*- coding=utf-8 -*-

import os
import time
from optparse import OptionParser
from PIL import Image

def option():
     # 获取脚本所在当前目录
     current_dir = os.path.dirname(__file__)
     # 根据截图时间生成默认文件名：20170722142831.png
     file_name = "%s.png" % time.strftime("%Y%m%d%H%M%S", time.localtime())

     usage = "screencap.py [-d <directory> -f <filename>]"
     description = "Automatic screenshots for android, After in PC display ."

     p = OptionParser(usage=usage, description=description)

     p.add_option("-d", "--dir",
                  dest="directory", default=current_dir,
                  help="directory of save the address")
     p.add_option("-f", "--filename",
                  dest="filename", default=file_name,
                  help="filename of screen shots file name")
     return p.parse_args()

def screen(options):
     # 截图
     print(os.popen("adb shell screencap /sdcard/{filename}".format(filename=options.filename)).read())
     # 截图导出
     print(os.popen(r"adb pull /sdcard/{filename} {dir}".format(filename=options.filename, dir=options.directory)).read())
     # 打开截图
     img = Image.open('{filename}'.format(filename=options.filename))
     img.show()
     # print(os.popen(r"start {filename}".format(filename=options.filename)).read())
     # 删除截图
     print(os.popen("adb shell rm /sdcard/{filename}".format(filename=options.filename)))
if __name__ == '__main__':
    while(True):
        options, args = option()
        screen(options)
        time.sleep(6)
        # print(options)
        # print(args)
