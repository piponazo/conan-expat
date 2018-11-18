from conans import ConanFile, CMake, tools

class ExpatConan(ConanFile):
    name = "Expat"
    version = "2.2.6"
    description = "Recipe for Expat library"
    license = "MIT/X Consortium license. Check file COPYING of the library"
    url = "https://github.com/Pix4D/conan-expat"
    source_url = "https://github.com/libexpat/libexpat"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = ['FindExpat.cmake']

    def source(self):
        self.run("git clone --depth 1 --branch R_2_2_6 %s" % self.source_url)

    def build(self):
        tools.replace_in_file("libexpat/expat/CMakeLists.txt", "cmake_minimum_required(VERSION 2.8.10)",
            """cmake_minimum_required(VERSION 2.8.10)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()
""")

        cmake = CMake(self)

        cmake_args = { "BUILD_doc" : "OFF",
                       "BUILD_examples" : "OFF",
                       "BUILD_shared" : self.options.shared,
                       "BUILD_tests" : "OFF",
                       "BUILD_tools" : "OFF",
                       "CMAKE_POSITION_INDEPENDENT_CODE": "ON",
                     }

        cmake.configure(source_dir="../libexpat/expat", build_dir="build", defs=cmake_args)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindExpat.cmake", ".", ".")

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["expatd"]
        else:
            self.cpp_info.libs = ["expat"]
        if not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

    def configure(self):
        del self.settings.compiler.libcxx
