#!/usr/bin/env python
import sys
import os
import traceback

import common
import detector


def main():
    print("main entry!")

    workspace = os.getcwd()
    print("workspace: " + workspace)

    from optparse import OptionParser

    parser = OptionParser(usage="./main.py -o csv_path")

    parser.add_option("-c", "--configfile",
                      action="store", type="string", dest="config_file", default=None,
                      help="The config file path")

    parser.add_option("-z", "--zip",
                      action="store", type="string", dest="seven_zip_path", default=None,
                      help="7z path")

    parser.add_option("-p", "--pkg-dir",
                      action="store", type="string", dest="pkg_dir", default=None,
                      help="Directory that contains packages")

    parser.add_option("-o", "--out-file",
                      action="store", type="string", dest="out_file", default=None,
                      help="The result file")

    (opts, args) = parser.parse_args()

    if opts.config_file is None:
        opts.config_file = "config.json"

    cfg = common.read_object_from_json_file(opts.config_file)

    cfg["7z_path"]= opts.seven_zip_path

    if opts.pkg_dir is not None:
        cfg["package_dirs"]= [opts.pkg_dir]

    d = detector.GameEngineDetector(workspace, cfg)
    d.run()
    r = d.get_all_results()

    out_file_name = os.path.join(workspace, "result.csv")

    if opts.out_file:
        out_file_name = opts.out_file

    common.result_csv_output(r, out_file_name)

    for e in r:
        str = "package: " + e["file_name"] + ", engine: " + e["engine"] + ", "
        if e["sub_types"]:
            for sub_type in e["sub_types"]:
                str += "subtype: " + sub_type + ", "

        if len(e["error_info"]) > 0:
            for err in e["error_info"]:
                str += ", error info: " + err

        str += "matched:" + e["matched_content_file_name"]

        print(str)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
