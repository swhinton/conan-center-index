from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0"


class CycloneDDSConan(ConanFile):
    name = "cyclonedds"
    license = "EPL-2.0"
    homepage = "https://cyclonedds.io/"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Eclipse Cyclone DDS - An implementation"\
                  " of the OMG Data Distribution Service (DDS) specification"
    topics = ("dds", "ipc", "ros", "middleware")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_ssl": [True, False],
        "with_shm" : [True, False],
        "enable_security" : [True, False],
        "with_type_discovery": [True, False],
        "with_topic_discovery": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_ssl": False,
        "with_shm": False,
        "enable_security": False,
        "with_type_discovery": True,
        "with_topic_discovery": True
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

    def layout(self):
        cmake_layout(self,src_folder="src")

    def requirements(self):
        if self.options.with_shm:
            self.requires("iceoryx/2.0.2")
        if self.options.with_ssl:
            self.requires("openssl/1.1.1t")

    def validate(self):
        if self.options.enable_security and not self.options.shared:
            raise ConanInvalidConfiguration(f"{self.ref} currently do not support"\
                                            "static build and security on")
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
        # We need to build the IDL library here so that the CXX package can link to it... ay ay ay
        tc.variables["BUILD_IDLC"] = True
        tc.variables["BUILD_IDLC_TESTING"] = False
        tc.variables["BUILD_DDSPERF"] = False
        tc.variables["BUILD_IDLC_TESTING"] = False
        tc.variables["ENABLE_SSL"] = self.options.with_ssl
        tc.variables["ENABLE_SHM"] = self.options.with_shm
        if self.options.with_shm:
            tc.preprocessor_definitions["DDSC_HAS_SHM"] = 1
        tc.variables["ENABLE_SECURITY"] = self.options.enable_security
        tc.variables["ENABLE_TYPE_DISCOVERY"] = self.options.with_type_discovery
        tc.variables["ENABLE_TOPIC_DISCOVERY"] = self.options.with_topic_discovery
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
        # Important: Cyclone team names their modules 'CycloneDDS', but conan requires lower-case.
        # If we don't do this, packages that depend on this one will fail to build, so unfortunately
        # dependency packages will need to patch their CMake scripts to use the lower-case name.
        self.cpp_info.set_property("cmake_file_name", "cyclonedds")
        self.cpp_info.set_property("pkg_config_name", "cyclonedds")

        self.cpp_info.components["idl"].libs = ["cycloneddsidl"]
        self.cpp_info.components["idl"].set_property("cmake_target_name", "cyclonedds::idl")

        self.cpp_info.components["ddsc"].libs = ["ddsc"]
        self.cpp_info.components["ddsc"].set_property("cmake_target_name", "cyclonedds::ddsc")
        requires = []
        if self.options.with_shm:
            self.cpp_info.components["ddsc"].defines = ["DDSC_HAS_SHM"]
            requires.append("iceoryx::iceoryx_binding_c")
        if self.options.with_ssl:
            requires.append("openssl::openssl")
        self.cpp_info.components["ddsc"].requires = requires
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["ddsc"].system_libs = ["pthread"]
            if self.options.shared:
                self.cpp_info.components["ddsc"].system_libs.append("dl")
        elif self.settings.os == "Windows":
            self.cpp_info.components["ddsc"].system_libs = [
                "ws2_32",
                "dbghelp",
                "bcrypt",
                "iphlpapi"
            ]
