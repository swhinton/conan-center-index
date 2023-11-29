from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0"


class gherkinc(ConanFile):
    name = "gherkin-c"
    license = "MIT"
    homepage = "https://github.com/cucumber/gherkin-c"
    url = "https://github.com/cucumber/gherkin-c"
    description = "Gherkin parser/compiler in C."
    topics = ("gherkin")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    short_paths = True

    @property
    def _min_cstd(self):
        return "99"

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "7",
            "Visual Studio": "16",
            "msvc": "192",
            "clang": "7",
            "apple-clang": "10",
        }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self,src_folder="src")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C{self._min_cstd}, which your compiler does not support."
            )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.options.shared:
            tc.variables["BUILD_SHARED_LIBS"] = True
        tc.generate()
        cd = CMakeDeps(self)
        cd.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        if self.settings.os == "Windows" and self.options.shared:
            for p in ("*.pdb", "concrt*.dll", "msvcp*.dll", "vcruntime*.dll"):
                rm(self, p, os.path.join(self.package_folder, "bin"))
        else:
            rmdir(self, os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "gherkin-c")
        self.cpp_info.set_property("pkg_config_name", "gherkin-c")
        self.cpp_info.components["gherkin-c"].libs = ["gherkin"]
        self.cpp_info.components["gherkin-c"].set_property("cmake_target_name", "gherkin-c::gherkin")
        self.cpp_info.components["gherkin-c"].set_property("cmake_target_name", "gherkin-c::gherkin")
        self.cpp_info.components["gherkin-c"].system_libs.append("m")
        if self.options.shared:
            self.cpp_info.components["gherkin-c"].system_libs.append("dl")
