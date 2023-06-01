from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0"


class gunit(ConanFile):
    name = "gunit"
    license = "BSL-1.0"
    homepage = "https://github.com/c-libs/GUnit"
    url = "https://github.com/c-libs/GUnit"
    description = "Google.Test/Google.Mock/Cucumber on steroids"
    topics = ("test", "gherkin", "cucumber")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
		"shared": [True, False],
		"fPIC": [True, False],
        "with_bdd": [True, False]
    }
    default_options = {
		"shared": False,
		"fPIC": False,
        "with_bdd": True
    }

    short_paths = True

    def export_sources(self):
        export_conandata_patches(self)

    def build_requirements(self):
        self.requires("nlohmann_json/[>=3.0]", transitive_headers=True, transitive_libs=True)
        self.requires("gtest/[>=1.0]", transitive_headers=True, transitive_libs=True)
        if self.options.with_bdd:
            self.requires("gherkin-cpp/clibs", transitive_headers=True, transitive_libs=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def package(self):
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "gunit")
        self.cpp_info.set_property("pkg_config_name", "gunit")
        self.cpp_info.set_property("cmake_target_name", "gunit::gunit")
        self.cpp_info.set_property("cmake_target_name", "gunit::gunit")
        self.cpp_info.requires = ["gtest::libgtest", "gtest::gmock", "gtest::gmock_main", "nlohmann_json::nlohmann_json"]
        if self.options.with_bdd:
            self.cpp_info.requires.append("gherkin-cpp::gherkin-cpp")

