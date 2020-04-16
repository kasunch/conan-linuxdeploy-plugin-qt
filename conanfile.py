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
        #self.requires("linuxdeploy/continuous@appimage-conan-community/stable")
        self.requires("linuxdeploy/continuous@bincreators/stable")
        self.requires("gtest/1.10.0")

    def source(self):
        self.run("git clone https://github.com/linuxdeploy/linuxdeploy-plugin-qt.git --depth=1")
        self.run("cd linuxdeploy-plugin-qt && git rm --cached lib/linuxdeploy && git rm --cached lib/googletest")
        self.run("cd linuxdeploy-plugin-qt && git submodule update --init --recursive")

    def build(self):
      
        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "lib", "CMakeLists.txt"), 
                                            "add_subdirectory(linuxdeploy EXCLUDE_FROM_ALL)", "")

        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "lib", "CMakeLists.txt"), 
                                            "add_subdirectory(googletest EXCLUDE_FROM_ALL)", "")
      
        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "CMakeLists.txt"), 
                                            "add_subdirectory(lib)", 
                                            """
                                            add_subdirectory(lib)
                                            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                                            conan_basic_setup(NO_OUTPUT_DIRS)
                                            find_package(linuxdeploy REQUIRED)
                                            find_package(args REQUIRED)
                                            find_package(Boost REQUIRED modules filesystem)
                                            find_package(GTest REQUIRED)
                                            """)
        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "tests", "CMakeLists.txt"), 
        "target_link_libraries(linuxdeploy-plugin-qt-tests linuxdeploy_core args json gtest linuxdeploy-plugin-qt_util)", 
        "target_link_libraries(linuxdeploy-plugin-qt-tests linuxdeploy_core json GTest::GTest linuxdeploy-plugin-qt_util)")

        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "src", "CMakeLists.txt"), 
        "target_link_libraries(linuxdeploy-plugin-qt_util linuxdeploy_core args)", 
        "target_link_libraries(linuxdeploy-plugin-qt_util PUBLIC linuxdeploy::linuxdeploy args::args)")

        tools.replace_in_file(os.path.join(self.source_folder, "linuxdeploy-plugin-qt", "src", "CMakeLists.txt"), 
        "target_link_libraries(linuxdeploy-plugin-qt linuxdeploy_core args json linuxdeploy-plugin-qt_util)", 
        "target_link_libraries(linuxdeploy-plugin-qt json linuxdeploy-plugin-qt_util)")
      
        cmake = CMake(self)
        cmake.definitions["CMAKE_PROJECT_linuxdeploy-plugin-qt_INCLUDE"] = self.build_folder + "/conan_paths.cmake"
        cmake.configure(source_folder="linuxdeploy-plugin-qt")
        cmake.build()

    def package(self):
        self.copy("linuxdeploy-plugin-qt", dst="bin", src="bin")

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

    def deploy(self):
        self.copy("*", dst="bin", src="bin")
