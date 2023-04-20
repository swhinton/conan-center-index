from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=1.53.0"


class CycloneDDSCXXConan(ConanFile):
    name = "cyclonedds-cxx"
    license = "EPL-2.0"
    homepage = "https://cyclonedds.io/"
    url = "https://github.com/eclipse-cyclonedds/cyclonedds-cxx"
    description = "Eclipse Cyclone DDS CXX - Cyclone DDS C++ language binding"
    topics = ("dds", "ipc", "ros", "middleware")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_shm": [True, False],
        "with_type_discovery": [True, False],
        "with_topic_discovery": [True, False],
        "with_legacy_support": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_shm": False,
        "with_type_discovery": True,
        "with_topic_discovery": True,
        "with_legacy_support": False
    }

    short_paths = True

    @property
    def _min_cppstd(self):
        return "14"

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
        # The C++ binding options are coupled to the C implementation.
        # The cyclone team uses CMake to generate their dep files and
        # uses CMake properties to check for correct coupling. Conan
        # doesn't know about that, so we patch the CMakeLists.txt and
        # implement a more permissive analogue here.
        if self.options.with_shm:
            self.options["cyclonedds"].with_shm = True
        if self.options.with_type_discovery:
            self.options["cyclonedds"].with_type_discovery = True
        if self.options.with_topic_discovery:
            # Prerequisite for topic discovery.
            self.options["cyclonedds"].with_type_discovery = True
            self.options.with_type_discovery = True

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("cyclonedds/0.10.3")
        if self.options.with_shm:
            self.requires("iceoryx/2.0.2")
        if self.options.with_legacy_support:
            self.requires("boost/1.81.0")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
            )

    def _cmake_new_enough(self, required_version):
        try:
            import re
            from io import StringIO
            output = StringIO()
            self.run("cmake --version", output=output)
            m = re.search(r"cmake version (\d+\.\d+\.\d+)", output.getvalue())
            return Version(m.group(1)) >= required_version
        except:
            return False

    def build_requirements(self):
        if not self._cmake_new_enough("3.16"):
            self.tool_requires("cmake/3.25.2")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        # The IDL generator from CycloneDDS isn't part of this package, but we need to produce the library for it.
        tc.variables["BUILD_IDLLIB"] = True
        tc.variables["ENABLE_LEGACY"] = self.options.with_legacy_support
        tc.variables["ENABLE_SHM"] = self.options.with_shm
        tc.variables["ENABLE_TYPE_DISCOVERY"] = self.options.with_type_discovery
        tc.variables["ENABLE_TOPIC_DISCOVERY"] = self.options.with_topic_discovery
        if self.options.with_shm:
            tc.preprocessor_definitions["DDSCXX_HAS_SHM"] = 1
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
            # idlcxx is a library loaded by idlc, so we don't have any bins.
            rmdir(self, os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "cyclonedds-cxx")
        self.cpp_info.set_property("pkg_config_name", "cyclonedds-cxx")

        # C++ IDL extension for the IDLC tool.
        self.cpp_info.components["idlcxx"].libs = ["cycloneddsidlcxx"]
        self.cpp_info.components["idlcxx"].set_property("cmake_target_name", "cyclonedds-cxx::idlcxx")

        self.cpp_info.components["ddscxx"].libs = ["ddscxx"]
        self.cpp_info.components["ddscxx"].set_property("cmake_target_name", "cyclonedds-cxx::ddscxx")
        self.cpp_info.components["ddscxx"].requires = ["cyclonedds::ddsc"]
        self.cpp_info.components["ddscxx"].includedirs = ["include/ddscxx"]
        if self.options.with_shm:
            self.cpp_info.components["ddscxx"].requires.append("iceoryx::iceoryx_binding_c")
            self.cpp_info.components["ddscxx"].defines.append("DDSCXX_HAS_SHM")
        if self.options.with_legacy_support:
            self.cpp_info.components["ddscxx"].requires.append("boost::headers")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["ddscxx"].system_libs = ["pthread"]
            if self.options.shared:
                self.cpp_info.components["ddscxx"].system_libs.append("dl")
        elif self.settings.os == "Windows":
            self.cpp_info.components["ddscxx"].system_libs = [
                "ws2_32",
                "dbghelp",
                "bcrypt",
                "iphlpapi"
            ]
