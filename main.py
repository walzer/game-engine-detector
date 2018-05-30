#!/usr/bin/env python
import sys
import os
import traceback
import re

def main():
    
    # initialization
    engines = {}
    engines['cocos']  = 0
    engines['laya']   = 0
    engines['egret']  = 0
    engines['others'] = 0
    index = 0

    # get the path to wxapkg
    if len(sys.argv) < 2:
        print 'usage: python main.py {path_to_wxapkgs}'
        exit()
    
    path_packages = sys.argv[1]
    workspace = os.getcwd()

    # get the list of wxapkg
    list_wxapkg = os.listdir(path_packages)

    # the the full path
    for i in range(0, len(list_wxapkg)):
        list_wxapkg[i] = workspace + "/" + path_packages + "/" + list_wxapkg[i]



    # unpack all the wxapkgs
    for i in list_wxapkg:

        # skip .DS_Store on mac
        if (".DS_Store" == os.path.basename(i)):
            continue

        # read the .wxapkg file content
        f = open(i, 'rb')
        content_size = os.path.getsize(i)
        content = f.read(content_size)

        # continue if this wxapkg doesn't has a "game.js" as a main entry file
        if (False == re.search("game.js", content)):
            print("%s doesn't have game.js" % i)
            f.close()
            continue
        
        index += 1
        is_cocos = ( None != re.search("cocos", content) )
        is_laya  = ( None != re.search("laya",  content) )
        is_egret = ( None != re.search("egret", content) )

        # conflicts such as "playable", "REGERT", "playAnimation" etc.
        if (is_cocos + is_egret + is_laya > 1):
            # use re.findall
            count_cocos = len( re.findall("cocos", content) )
            count_laya  = len( re.findall("laya",  content) )
            count_egret = len( re.findall("egret", content) )
            count_max   = max(count_cocos, count_egret, count_laya)

            if (count_cocos == count_egret or
                count_laya  == count_egret  or
                count_egret == count_laya ):
                print("CONFLICT: PLEASE DETECT %s MANUALLY." % i)
            elif (count_max == count_egret):
                is_cocos = 0
                is_egret = 1
                is_laya  = 0
            elif (count_max == count_laya):
                is_cocos = 0
                is_egret = 0
                is_laya  = 1
            elif (count_max == count_cocos):
                is_cocos = 1
                is_egret = 0
                is_laya  = 0

        if (is_cocos + is_laya + is_egret > 1):
            print("STILL CONFLICT: %s" % i)
        elif ( is_cocos + is_egret + is_laya == 0):
            engines['others'] += 1
            print("%s: others" % i)
        elif (is_cocos):
            engines['cocos'] += 1
            print("%s: cocos" % i)
        elif (is_laya):
            engines['laya'] += 1
            print("%s: laya" % i)
        elif (is_egret):
            engines['egret'] += 1
            print("%s: egret" % i)
        else:
            print("WTF??")
    # end of for list_wxapkg

    # calculate total number of wxapkgs
    total = engines['cocos'] + engines['laya'] + engines['egret'] + engines['others']

    # dump
    print("total = %d" % total)
    for i in engines.keys():
        print("%s = %d, percentage = %.2f%%" % (i, engines[i], 100 * float(engines[i]) / float(total)))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
