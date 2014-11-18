#!/usr/bin/env python
import json
import re
import os
import subprocess


def unzip_package(file_path, out_dir):
    with open(file_path, 'rb') as f:
        ret = subprocess.call(['/usr/local/bin/7z', 'x', file_path, "-o" + out_dir], stdout=open(os.devnull, 'w'))
    return ret

def to_absolute_path(basePath, relativePath):
    if relativePath and not os.path.isabs(relativePath):
        relativePath = os.path.join(basePath, relativePath)
    return relativePath


def read_object_from_json_file(jsonFilePath):
    ret = None
    with open(jsonFilePath, 'r') as json_file:
        ret = json.load(json_file)
    return ret


# Returns True of callback indicates no need to iterate
def deep_iterate_dir(rootDir, callback):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            if not callback(path, True):
                if deep_iterate_dir(path, callback):
                    return True
            else:
                return True
        elif os.path.isfile(path):
            if callback(path, False):
                return True
    return False

def re_test(args, path_in_apk):
    if args:
        for f in args:
            f = '^' + f + '$'
            if re.search(f, path_in_apk):
                return True
    return False
