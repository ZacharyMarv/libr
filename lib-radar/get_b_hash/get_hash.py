# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        Convert Apk into Smali
"""
__author__ = 'Zachary Marv - 马子昂'

import os
import json
import glob
import re
import subprocess
import sys
import time


class TimeRecord:
    """
    Made for Time Recording.
    用来计时。
    """
    def __init__(self, Tag = ""):
        self.init_time = time.time()
        self.if_start = False
        self.start_time = 0
        self.tag = Tag

    def start(self):
        self.start_time = time.time()
        self.if_start = True
        print('*' * 60)
        print('Task: '+self.tag+' Starts.')

    def end(self):
        end_time = time.time()
        if self.if_start:
            task_interval = end_time - self.start_time
            print('Task: '+sys.argv[0]+' Ends.')
            m = int(task_interval) / 60
            s = task_interval - m
            if m <= 1:
                mi = 'minute'
            else:
                mi = 'minutes'
            if s <= 1:
                se = 'second'
            else:
                se = 'seconds'
            print(self.tag + ' Consuming '+str(m)+' '+mi+' and '+str(s)+' '+se+'.')
            print('*' * 60)
        self.if_start = False

time_decode = TimeRecord('Decoding')
time_compare = TimeRecord('Searching')

reload(sys)
sys.setdefaultencoding( "utf-8" )

DEBUG = True

api_dict = {}
packages_feature = []
libs_feature = []
project_path = os.path.dirname(sys.argv[0])

def get_smali(path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    time_decode.start()
    cmd = project_path + "/" + "../tool/apktool decode %s -o " % path + project_path + "/" + "../decoded/%s" % os.path.basename(path)
    #print "CMD \n\n"
    #print cmd
    #print "\n"
    subprocess.call(cmd, shell=True)
    # print os.getcwd()
    time_decode.end()
    return project_path + '/../decoded/%s' % os.path.basename(path)


def get_hash(apk_path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    # - Loading Data

    time_compare.start()
    dep_addr = project_path + "/" + "../data/tagged_dep2.dat"
    dict_addr = project_path + "/" + "../data/dict.dat"
    dep_file = open(dep_addr, 'r')
    dict_file = open(dict_addr, 'r')

    # -- Loading API Dict
    for line in dict_file:
        # print line
        u = json.loads(line)
        api_dict[u['key']] = u['value']

    # -- Loading Hashed Libs

    for line in dep_file:
        # print line
        u = json.loads(line)
        # s_path = '/'.join(u['path_parts'])
        libs_feature.append((u['b_hash'],  u['b_total_num'], u['b_total_call'], u['s_path'], u['lib']))

    # - All Over
    # print apk_path+'/smali'
    if os.path.exists(apk_path+'/smali'):
        os.chdir(apk_path+'/smali')
        all_over(apk_path, apk_path+'/smali')
        os.chdir(apk_path)

    # Print Res
    # print packages_feature
    '''
    if DEBUG:
        for p in packages_feature:
            print p
    '''
    cur_app_libs = []
    cur_app_routes = []
    for p in packages_feature:
        for l in libs_feature:
            if l[2] < 5:
                continue
            if p[0] == l[0] and p[1] == l[1] and p[2] == l[2]:
                # print(str(l) + "   " + str(p))
                tmp = ""
                if l[4] != "":
                    tmp = l[4]
                    if tmp not in cur_app_libs:
                        cur_app_libs.append(tmp)
                else :
                    tmp = l[3]
                    if tmp not in cur_app_routes:
                        cur_app_routes.append(tmp)
    print "--Spliter--"
    for i in cur_app_libs:
        print i + ','
    print "--Spliter--"
    for i in cur_app_routes:
        print i + ','
    print "--Spliter--"
    time_compare.end()
    return "Get Function Ends."

def get_number(string):
    """
    Get API ID From API Dictionary.
    获得API的编号
    :param string: API Name
    :return: API ID
    """
    if string not in api_dict:
        return -1
    return str(api_dict[string])

def all_over(apk_path, path):
    """
    Recursive body of package for getting the features
    :param apk_path: APK Path
    :param path: Packages Path
    :return: API Dict of this package, Directory Number in this Package, File Number, Total API Call.
    """

    find_file = re.compile(r'.smali$')
    p = re.compile(r'Landroid/.*?;?\-?>*?\(|Ljava/.*?;?\-?>*?\(|Ljavax/.*?;?\-?>*?\(|Lunit/runner/.*?;?\-?>*?\('
                   r'|Lunit/framework/.*?;?\-?>*?\('
                   r'|Lorg/apache/commons/logging/.*?;?\-?>*?\(|Lorg/apache/http/.*?;?\-?>*?\(|Lorg/json/.*?;'
                   r'?\-?>*?\(|Lorg/w3c/.*?;?\-?>*?\(|Lorg/xml/.*?;?\-?>*?\(|Lorg/xmlpull/.*?;?\-?>*?\(|'
                   r'Lcom/android/internal/util.*?;?\-?>*?\(')
    all_thing = glob.glob('*')
    this_call_num = 0
    this_dir_num = 0
    this_file_num = 0
    direct_dir_num = 0
    direct_file_num = 0
    this_dict = {}
    for thing in all_thing:
        # If the thing is a directory.
        if os.path.isdir(thing):
            os.chdir(path+'/'+thing)
            # Merge Dictionary
            # 合并字典
            child = all_over(apk_path, path+'/'+thing)
            if child is not None:
                this_dict.update(child[0])
                this_dir_num += child[1] + 1
                direct_dir_num += 1
                this_file_num += child[2]
                this_call_num += child[3]
            os.chdir(path)
        # If the thing is a file
        else:
            try:
                # Is this file a smali file?
                if not find_file.search(thing):
                    continue
                f = open(thing, 'r')
                for u in f:
                    # For every line in this file.
                    match = p.findall(u)
                    for system_call in match:
                        if '"' in system_call:
                            continue
                        this_call_num += 1
                        if "\"" in system_call or "'" in system_call or "“" in system_call or "‘" in system_call:
                            continue
                        if ";->" not in system_call:
                            continue
                        call_num = get_number(system_call)
                        if call_num == -1:
                            continue
                        if call_num in this_dict:
                            this_dict[call_num] += 1
                        else:
                            this_dict[call_num] = 1
                f.close()
                this_file_num += 1
                direct_file_num += 1
            except Exception as ex:
                print('Can not Open ' + thing + ' Wrong with:' + str(ex))
    # Remove all the Log API
    # 去除所有的关于Log的API，来去除插桩或者其他因素造成的影响
    logs = ['Landroid/util/Log;->v(', 'Landroid/util/Log;->e(', 'Landroid/util/Log;->w(',
            'Landroid/util/Log;->i(', 'Landroid/util/Log;->d(']
    for log in logs:
        if get_number(log) in this_dict:
            del this_dict[get_number(log)]
    # If there is no API call in this package, just ignore it.
    if len(this_dict) == 0:
        return
    parts = path[len(apk_path)+7:].split("/")
    if parts[0] == '':
        depth = 0
    else:
        depth = len(parts)
    package = {'apk': apk_path,                         # Ahe APK file storing path
               'path': path,                            # The Packages' path
               'path_parts': parts,                     # Parts of Path
               'depth': depth,                     # Directory Depth
               'total_num': len(this_dict),             # Total API Types
               'total_call': this_call_num,             # Total API Calls
               'dir_num': this_dir_num,                 # The number of all the directories in this package
               'file_num': this_file_num,               # The number of all the code files in this package
               'direct_dir_num': direct_dir_num,        # The number of directories directly in this package
               'direct_file_num': direct_file_num,      # The number of code files directly in this package
               'api_dict': this_dict,                   # API Dict
               'status': 0
               # status (0:not_scanned, 1:is_lib_root, 2:is_not_lib, 3:is_lib_child, 4:smali_root)
               }
    b_hash = 0
    for a in this_dict:
        b_hash = (b_hash + int(a) * this_dict[a]) % 999983
    packages_feature.append((b_hash, len(this_dict), this_call_num, '/'.join(parts)))
    return this_dict, this_dir_num, this_file_num, this_call_num



def main_func(path):
    # print "Main Func Starts."
    decoded_path = get_smali(path)
    get_hash(decoded_path)
    # print "Main Func Ends."


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "No Apk File Name."
        if DEBUG:
            main_func("~/Downloads/365rili.apk")
    else:
        print os.path.basename(sys.argv[1])
        main_func(sys.argv[1])