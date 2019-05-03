from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    remotes = [("https://api.bintray.com/conan/appimage-conan-community/public-conan", "true", "appimage"),
               ("https://api.bintray.com/conan/bincrafters/public-conan", "true", "bincrafters")]
    builder = ConanMultiPackager(remotes=remotes, build_policy="outdated")
    builder.add_common_builds()

    builder.run()
