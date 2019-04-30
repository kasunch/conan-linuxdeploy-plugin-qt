import os

from conans import ConanFile, CMake, tools


class LinuxdeploypluginqtTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("echo \"plugin-type: `linuxdeploy-plugin-qt --plugin-type`\"", run_environment=True)
            self.run("echo \"plugin-api-version: `linuxdeploy-plugin-qt --plugin-api-version`\"", run_environment=True)
