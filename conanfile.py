from conans import ConanFile, CMake, tools
import os


class LinuxdeploypluginqtConan(ConanFile):
    name = "linuxdeploy-plugin-qt"
    version = "continuous"
    license = "MIT"
    author = "Alexis Lopez Zubieta contact@azubieta.net"
    url = "https://github.com/appimage-conan-community/linuxdeploy-plugin-qt_installer"
    description = "Qt plugin for linuxdeploy, bundling Qt resources, plugins and QML files."
    topics = ("AppImage", "Qt", "linuxdeploy")
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake", "cmake_find_package", "cmake_paths")
    build_requires = "cmake_installer/3.15.3@conan/stable"
    exports_sources = "patches/*"

    def requirements(self):
        self.requires("args/6.2.2@pavel-belikov/stable")
        self.requires("linuxdeploy/continuous@appimage-conan-community/stable")

    def source(self):
        self.run("git clone https://github.com/linuxdeploy/linuxdeploy-plugin-qt.git --depth=1")
        self.run("cd linuxdeploy-plugin-qt && git rm --cached lib/linuxdeploy")
        self.run("cd linuxdeploy-plugin-qt && git submodule update --init --recursive")
        tools.patch(base_path="linuxdeploy-plugin-qt", patch_file="patches/use_conan.patch")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_PROJECT_linuxdeploy-plugin-qt_INCLUDE"] = self.build_folder + "/conan_paths.cmake"
        cmake.definitions["USE_CONAN"] = True
        cmake.configure(source_folder="linuxdeploy-plugin-qt")
        cmake.build()

    def package(self):
        self.copy("linuxdeploy-plugin-qt", dst="bin", src="bin")

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

    def deploy(self):
        self.copy("*", dst="bin", src="bin")
