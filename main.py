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

    parser = OptionParser()

    parser.add_option("-c", "--configfile",
                      action="store", type="string", dest="config_file", default=None,
                      help="The config file path")

    (opts, args) = parser.parse_args()

    if opts.config_file is None:
        opts.config_file = "config.json"

    d = detector.GameEngineDetector(workspace, opts.config_file)
    d.run()
    r = d.get_all_results()
    for e in r:
        str = "package: " + e["file_name"] + ", engine: " + e["engine"]
        if e["sub_type"]:
            str += ", subtype: " + e["sub_type"]

        if len(e["error_info"]) > 0:
            str += ", error info: " + e["error_info"]

        print(str)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
