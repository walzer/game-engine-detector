
import os
import re

def run(name):

    # there are empty or stab wxapkgs, we should avoid this ones
    if ( False == os.path.exists(name) ):
        return "null"

    f = open(name, "rb")
    content_size = os.path.getsize(name)
    content = f.read(content_size)
    content.lower()

    if re.search("cocos", content):
        retVal = "cocos"
    elif re.search("egret", content):
        retVal = "egret"
    elif re.search("laya", content):
        retVal = "laya"
    else:
        retVal = "others"
    
    f.close()
    return retVal