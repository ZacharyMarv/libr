# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        Convert Apk into Smali
"""
__author__ = 'Zachary Marv - 马子昂'

import subprocess
import os

def get_smali(path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    cmd = "../tool/apktool decode %s -o ../decoded/%s" % (path, os.path.basename(path))
    subprocess.call(cmd, shell=True)
    return '../decoded/%s' % os.path.basename(path)


def main_func():
    print "Main Func Starts."
    print get_smali("~/Downloads/切水果3.apk")
    print "Main Func Ends."


if __name__ == '__main__':
    main_func()