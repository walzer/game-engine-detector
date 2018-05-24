#!/usr/bin/env python
import sys
import os
import traceback

# import common
# import detector
import WxapkgUnpacker
import WxapkgDetector

def main():
    # print("main entry!")

    workspace = os.getcwd()
    # print("workspace: " + workspace)

    # get the list of wxapkg
    path_packages = "wxapkg"  # to be fixed, should not hard code here
    list_wxapkg = os.listdir(path_packages)

    # the the full path
    for i in range(0, len(list_wxapkg)):
        list_wxapkg[i] = workspace + "/" + path_packages + "/" + list_wxapkg[i]

    # unpack all the wxapkgs
    for i in list_wxapkg:
        WxapkgUnpacker.run(i)

    # detect game.js
    list_unpacked_wxapkg = os.listdir("wxapkgs_unpacked")
    
    engine = {}
    engine['cocos'] = 0
    engine['laya'] = 0
    engine['egret'] = 0
    engine['others'] = 0

    for i in list_unpacked_wxapkg:
        ret = WxapkgDetector.run(workspace + "/wxapkgs_unpacked/" + i + "/game.js")
        if (ret != "null"):
            engine[ret] += 1

    # calculate total number of wxapkgs
    engine['total'] = engine['cocos'] + engine['laya'] + engine['egret'] + engine['others']

    # dump
    for i in engine.keys():
        print("%s = %d, percentage = %.2f%%" % (i, engine[i], 100 * float(engine[i]) / float(engine['total'])))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
