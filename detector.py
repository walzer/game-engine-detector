#!/usr/bin/env python
import os
import shutil
import common
import re

TAG = "GameEngineDetector: "


class PackageScanner:
    def __init__(self, workspace, engines, file_name):
        self.result = None
        self.workspace = workspace
        self.engines = engines
        self.file_name = file_name
        self.prev_engine_name = None
        self._reset_result()
        return

    def unzip_package(self, pkg_path, out_dir, seven_zip_path):

        ret = common.unzip_package(pkg_path, out_dir, seven_zip_path)
        if 0 != ret:
            print("==> ERROR: unzip package ( %s ) failed!" % self.file_name)
            self.result["error_info"].append("Unzip package failed")
        return ret

    def _set_engine_name(self, name):
        self.result["engine"] = name
        if self.prev_engine_name and self.prev_engine_name != name:
            self.result["error_info"].append("Previous check result is (%s), but now is (%s), please check config.json")

    def _remove_prefix(self, path):
        pos = path.find(self.workspace)
        if pos != -1:
            return path[len(self.workspace):]
        return path

    def _check_chunk(self, path, chunk, engine):
        "@return True if we could confirm the engine type"
        ret = False
        chunk = chunk.lower()

        for keyword in engine["file_content_keywords"]:
            keyword = keyword.lower()
            if re.search(keyword, chunk):
                #print("==> FOUND (engine: %s, keyword: %s)" % (engine["name"], keyword))
                self._set_engine_name(engine["name"])
                self.result["matched_content_file_name"] = self._remove_prefix(path)
                self.result["matched_content_keywords"].add(keyword)
                ret = True

        for (k, v) in engine["sub_types"].items():
            for keyword in v:
                keyword = keyword.lower()
                if re.search(keyword, chunk):

                    #print("==> FOUND sub type ( %s )" % v)
                    self._set_engine_name(engine["name"])
                    self.result["matched_content_file_name"] = self._remove_prefix(path)
                    self.result["sub_types"].add(k)
                    self.result["matched_sub_type_keywords"].add(keyword)
                    ret = True

        return ret


    def check_file_name(self, path):
        found = False

        for engine in self.engines:
            #print("==> Checking whether the game is made by " + engine["name"])

            for keyword in engine["file_name_keywords"]:
                if re.search(keyword, path):
                    self._set_engine_name(engine["name"])
                    self.result["matched_file_name_keywords"].add(keyword)

            if self.result["engine"] != "unknown":
                found = True
                break

        return found

    def check_file_content(self, path, chunk_size=81920):
        #print("==> Checking executable file ( %s )" % path)

        found = False

        for engine in self.engines:
            #print("==> Checking whether the game is made by " + engine["name"])

            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:
                        ret = self._check_chunk(path, chunk, engine)
                        if not found and ret:
                            found = True
                    else:
                        break

            if found:
                print("RESULT: " + str(self.result))
                break

        return found


    def _reset_result(self):
        self.result = {
            "file_name": self.file_name,
            "engine": "unknown",
            "matched_file_name_keywords": set(),
            "matched_content_file_name": "",
            "matched_content_keywords": set(),
            "sub_types": set(),
            "matched_sub_type_keywords": set(),
            "error_info": []
        }
        return


class GameEngineDetector:
    def __init__(self, workspace, opts):
        "Constructor"

        self.workspace = workspace
        self.opts = opts
        self.all_results = []

        print(TAG + str(opts))

        self.temp_dir = os.path.join(self.workspace, "temp")

        self.engines = opts["engines"]
        self.package_dirs = opts["package_dirs"]
        self.package_suffixes = opts["package_suffixes"]
        self._normalize_package_dirs()
        self.check_file_content_keywords = opts["check_file_content_keywords"]
        self.no_need_to_check_file_content = opts["no_need_to_check_file_content"]


    def _normalize_package_dirs(self):
        for i in range(0, len(self.package_dirs)):
            self.package_dirs[i] = common.to_absolute_path(self.workspace, self.package_dirs[i])
        print("package_dirs: " + str(self.package_dirs))


    def _need_to_check_file_content(self, path):
        "Check whether the file is an executable file"

        for k in self.no_need_to_check_file_content:
            m = re.search(k, path)
            if m:
                #print("==> Not need to check content: (%s)" % m.group(0))
                return False

        for keyword in self.check_file_content_keywords:
            m = re.search(keyword, path)
            if m:
                #print("==> Found file to check content: (%s)" % m.group(0))
                return True
        return False

    def _scan_package(self, pkg_path):

        file_name = os.path.split(pkg_path)[-1]
        print("==> Scanning package ( %s )" % file_name)
        print("==> Unzip package ...")
        out_dir = os.path.join(self.temp_dir, file_name)
        os.mkdir(out_dir)

        scanner = PackageScanner(self.workspace, self.engines, file_name)

        if 0 == scanner.unzip_package(pkg_path, out_dir, self.opts["7z_path"]):
            def callback(path, is_dir):
                if is_dir:
                    return False

                scanner.check_file_name(path)

                if self._need_to_check_file_content(path):
                    if scanner.check_file_content(path):
                        return True

                return False

            common.deep_iterate_dir(out_dir, callback)

        self.all_results.append(scanner.result)

        return


    def _iteration_callback(self, path, is_dir):
        for suffix in self.package_suffixes:
            if path.endswith(suffix):
                self._scan_package(path)

        return False

    def run(self):
        self.clean()
        # Re-create the temporary directory, it's an empty directory now
        os.mkdir(self.temp_dir)

        for d in self.package_dirs:
            common.deep_iterate_dir(d, self._iteration_callback, False)

        self.clean()
        print("==> DONE!")
        return

    def clean(self):
        print("==> Cleaning ...")
        # Remove temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        return

    def get_all_results(self):
        return self.all_results





