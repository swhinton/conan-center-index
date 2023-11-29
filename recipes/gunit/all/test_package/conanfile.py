import os
from conan import ConanFile
from conan.tools.files import copy
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        pass
        # if can_run(self):
        #     bin_path = os.path.join(self.cpp.build.bindirs[0], "test_package")
        #     test_data = os.path.join(self.source_folder, "testdata", "good", "several_examples.feature")
        #     self.run(bin_path + " " + test_data, env="conanrun")