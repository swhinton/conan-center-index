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

    # @property
    # def _min_cppstd(self):
    #     return "14"

    # @property
    # def _compilers_minimum_version(self):
    #     return {
    #         "gcc": "7",
    #         "Visual Studio": "16",
    #         "msvc": "192",
    #         "clang": "7",
    #         "apple-clang": "10",
    #     }

    def export_sources(self):
        export_conandata_patches(self)

    # def configure(self):
    #     self.settings.rm_safe("compiler.cppstd")
    #     self.settings.rm_safe("compiler.libcxx")

    # def layout(self):
    #     cmake_layout(self)

    # def validate(self):
    #     if self.settings.compiler.get_safe("cppstd"):
    #         check_min_cppstd(self, self._min_cppstd)
    #     minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
    #     if minimum_version and Version(self.settings.compiler.version) < minimum_version:
    #         raise ConanInvalidConfiguration(
    #             f"{self.ref} requires C{self._min_cppstd}, which your compiler does not support."
    #         )

    # def _cmake_new_enough(self, required_version):
    #     try:
    #         import re
    #         from io import StringIO
    #         output = StringIO()
    #         self.run("cmake --version", stdout=output)
    #         m = re.search(r"cmake version (\d+\.\d+\.\d+)", output.getvalue())
    #         return Version(m.group(1)) >= required_version
    #     except Exception as e:
    #         print(e)
    #         return False

    def build_requirements(self):
        self.requires("nlohmann_json/[>=3.0]")
        self.requires("gtest/[>=1.0]", transitive_headers=True, transitive_libs=True)
        if self.options.with_bdd:
            self.requires("gherkin-cpp/clibs")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    # def generate(self):
    #     tc = CMakeToolchain(self)
    #     tc.generate()
    #     cd = CMakeDeps(self)
    #     cd.generate()

    # def build(self):
    #     apply_conandata_patches(self)
    #     cmake = CMake(self)
    #     cmake.configure()
    #     cmake.build()

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

