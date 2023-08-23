#!/usr/bin/env python
#coding=utf-8
import json
import re
import os
import subprocess
import platform

def to_unix_path(path):
    return path.replace('\\', '/')

def normalize_utf8_path(path, index):
    dir = os.path.split(path)[0]
    ext = os.path.splitext(path)[1]
    new_path = os.path.join(dir, str(index) + ext)
    return new_path

def unzip_package(file_path, out_dir, seven_zip_path=None):
    if not seven_zip_path:
        os_name = platform.system().lower()
        if os_name == "darwin":
            seven_zip_path = './lib/7z-mac/7zz'
        elif os_name == "windows":
            seven_zip_path = '.\\lib\\7z-win\\7z.exe'
        else:
            seven_zip_path = '7z'

    ret = subprocess.call([seven_zip_path, 'x', file_path, "-o" + out_dir], stdout=open(os.devnull, 'w'))
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


# Returns True of callback indicates to stop iteration
def deep_iterate_dir(rootDir, callback, to_iter=True):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            if not to_iter:
                print("*** Skip sub directory: " + path)
                continue
            if callback(path, True):
                return True
            else:
                if deep_iterate_dir(path, callback, to_iter):
                    return True
        elif os.path.isfile(path):
            if callback(path, False):
                return True
    return False

def result_csv_output(result, output_path):
    import csv

    with open(output_path, "wb") as f:
        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["File",
                             "Engine",
                             "EngineVersion",
                             "Subtypes",
                             "matched_content_file_name",
                             "matched_content_keywords"])
        for e in result:
            if len(e["error_info"]) > 0:
                engine = ", ".join(e["error_info"])
                engine_version = "UNKNOWN"
            else:
                engine = e["engine"]
                engine_version = e["engine_version"]

            sub_types = ", ".join(e["sub_types"])
            matched_content_keywords = ",".join(e["matched_content_keywords"])

            csv_writer.writerow([e["file_name"].encode("utf-8"),
                                 engine.encode("utf-8"),
                                 engine_version.encode("utf-8"),
                                 sub_types.encode("utf-8"),
                                 e["matched_content_file_name"].encode("utf-8"),
                                 matched_content_keywords.encode("utf-8")])
            f.flush()
