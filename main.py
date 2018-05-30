#!/usr/bin/env python
import sys
import os
import os.path
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

    # get the path to wxapkgs, use "{workspace}/wxapkg" as default
    if len(sys.argv) < 2:
        path_to_wxapkgs_dir = "wxapkg"
    else:
        path_to_wxapkgs_dir = sys.argv[1]

    workspace = os.getcwd()

    # get the list of wxapkgs
    list_of_wxapkgs = os.listdir(path_to_wxapkgs_dir)

    # read and detect all the wxapkgs
    for i in list_of_wxapkgs:
                
        # skip any other files whos extension is not ".wxapkg"
        ext = os.path.splitext(i)[1]
        if ( ".wxapkg" == ext ):
            # set the full path
            full_path_wxapkg = workspace + "/" + path_to_wxapkgs_dir + "/" + i
        else:
            print("%s isn't a wxapkg." % i)
            continue

        # read the .wxapkg file content
        f = open(full_path_wxapkg, 'rb')
        content_size = os.path.getsize(full_path_wxapkg)
        content = f.read(content_size)

        # continue if this wxapkg doesn't has a "game.js" as a main entry file
        if (False == re.search("game.js", content)):
            print("%s doesn't have game.js" % i)
            f.close()
            continue

        # start game engine detection        
        index += 1

        # use re.findall instead of re.search to avoid words like "playable, playanimation, regret"
        count_cocos = len( re.findall("cocos", content) ) - len( re.findall("[a-zA-Z]cocos", content )) - len( re.findall("cocos[a-zA-Z]", content ))
        count_laya  = len( re.findall("laya",  content) ) - len( re.findall("[a-zA-Z]laya", content )) - len( re.findall("laya[a-zA-Z]", content ))
        count_egret = len( re.findall("egret", content) ) - len( re.findall("[a-zA-Z]egret", content)) - len( re.findall("egret[a-zA-Z]", content ))
        
        # some pkgs has "playable" but doesn't use laya, or has "regret" but doesn't use egret
        count_cocos = max (0, count_cocos)
        count_laya = max (0, count_laya)
        count_egret = max (0, count_egret)
        
        # who wins?
        count_max   = max( count_cocos, count_egret, count_laya )

        if ( count_max != ( count_cocos + count_egret + count_laya ) ):
            print("WARNING: PLEASE DETECT %s MANUALLY. cocos %d, egret %d, laya %d" % (i, count_cocos, count_egret, count_laya))

        if ( 0 == count_max ):
            result = "others"
        elif (count_max == count_egret):
            result = "egret"
        elif (count_max == count_laya):
            result = "laya"
        elif (count_max == count_cocos):
            result = "cocos"
        else:
            result = "WTF??"

        engines[result] += 1
        print("[%d] %s: \t%s\t [cocos:%4d, egret %4d, laya %4d]" % (index, i, result, count_cocos, count_egret, count_laya))

        f.close()
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
