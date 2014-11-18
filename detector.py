#!/usr/bin/env python
import os
import shutil
import common
import re

TAG = "GameEngineDetector: "

class GameEngineDetector:
    def __init__(self, workspace, opts):
        "Constructor"

        print(TAG + str(opts))
        self.workspace = workspace
        self.temp_dir = os.path.join(self.workspace, "temp")
        self._reset_result()

        # Remove temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        # Re-create the temporary directory, it's an empty directory now
        os.mkdir(self.temp_dir)

        self.package_dirs = opts["package_dirs"]
        self._normalize_package_dirs()

        self.engines = opts["engines"]

    def _reset_result(self):
        self.result = {
            "engine": "unknown",
            "matched_keywords": set(),
            "sub_type": "",
            "matched_sub_type_keywords": set()
        }
        return

    def _normalize_package_dirs(self):
        for i in range(0, len(self.package_dirs)):
            self.package_dirs[i] = common.to_absolute_path(self.workspace, self.package_dirs[i])
        print("package_dirs: " + str(self.package_dirs))


    def _check_chunk(self, chunk, engine):
        "@return True if we could confirm the engine type"

        for keyword in engine["file_content_keywords"]:
            if re.search(keyword, chunk):
                #print("==> FOUND (engine: %s, keyword: %s)" % (engine["name"], keyword))
                self.result["engine"] = engine["name"]
                self.result["matched_keywords"].add(keyword)

        for (k, v) in engine["sub_types"].items():
            for keyword in v:
                if re.search(keyword, chunk):
                    #print("==> FOUND sub type ( %s )" % v)
                    # FIXME: Check wether the type would be changed
                    self.result["sub_type"] = k
                    self.result["matched_sub_type_keywords"].add(keyword)


    def _check_executable_file(self, path, chunksize = 8192):
        #print("==> Checking executable file ( %s )" % path)

        found = False

        for engine in self.engines:
            #print("==> Checking whether the game is made by " + engine["name"])

            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunksize)
                    if chunk:
                        self._check_chunk(chunk, engine)
                    else:
                        break

            if self.result["engine"] != "unknown":
                found = True
                break

        if found:
            print("RESULT: " + str(self.result))
        return found


    def _scan_package(self, path, is_apk):
        # Resets result when starting a new package scanning
        self._reset_result()
        filename = os.path.split(path)[-1]
        print("==> Scanning apk file ( %s )" % filename)
        print("==> Unzip package ...")
        out_dir = os.path.join(self.temp_dir, filename)
        os.mkdir(out_dir)

        if 0 != common.unzip_package(path, out_dir):
            print("==> ERROR: unzip package ( %s ) failed!" % filename)
            return

        thiz = self
        def callback(path, is_dir):
            if is_dir:
                return False
            if path.endswith(".so"):
                if thiz._check_executable_file(path):
                    return True

            if not is_apk:
                if not path.endswith(".png") \
                    and not path.endswith(".jpg") \
                    and not path.endswith(".plist"):
                    if thiz._check_executable_file(path):
                        return True
            return False

        common.deep_iterate_dir(out_dir, callback)
        return


    def _iteration_callback(self, path, is_dir):
        # print(path + ", is_dir:" + str(is_dir))
        if path.endswith(".apk"):
            self._scan_package(path, True)
        elif path.endswith(".ipa"):
            self._scan_package(path, False)

        return False

    def run(self):

        for d in self.package_dirs:
            common.deep_iterate_dir(d, self._iteration_callback)

        self.clean()
        print("==> DONE!")
        return

    def clean(self):
        print("==> Cleaning ...")
        # Remove temporary directory
        # shutil.rmtree(self.temp_dir)

        return





