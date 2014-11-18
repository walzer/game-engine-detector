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

    if not os.path.isabs(opts.config_file):
        opts.config_file = os.path.join(workspace, opts.config_file)

    args = common.read_object_from_json_file(opts.config_file)
    # print("config:" + str(args))
    # print(common.re_test(args["files_in_apk"], "assets/xxx.png"))
    # print(common.re_test(args["files_in_apk"], "assets/xxx/yyy.png"))

    d = detector.GameEngineDetector(workspace, args)
    d.run()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
