from conan import ConanFile, tools
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
from conan.tools.scm import Version
import os


class DiConan(ConanFile):
    name = "di"
    license = "BSL-1.0"
    homepage = "https://github.com/boost-ext/di"
    url = "https://github.com/conan-io/conan-center-index"
    description = "DI: C++14 Dependency Injection Library."
    topics = ("dependency-injection", "metaprogramming", "design-patterns")
    exports_sources = ["BSL-1.0.txt"]
    settings = "compiler"
    options = {"with_extensions": [True, False], "diagnostics_level": [0, 1, 2]}
    default_options = {"with_extensions": False, "diagnostics_level": 1}
    no_copy_source = True
    package_type = "header-library"

    @property
    def _min_cppstd(self):
        return "14"

    @property
    def _minimum_compilers_version(self):
        return {
            "gcc": "5",
            "clang": "3.4",
            "apple-clang": "10",
            "Visual Studio": "15"
        }

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)
        minimum_version = self._minimum_compilers_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support.",
            )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

    def package(self):
        copy(self, "BSL-1.0.txt", src="", dst="licenses")
        copy(self, "*", src=os.path.join(self.source_folder, "include"), dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "di")
        self.cpp_info.set_property("cmake_target_name", "di::di")
        self.cpp_info.defines.append("BOOST_DI_CFG_DIAGNOSTICS_LEVEL={}".format(self.options.diagnostics_level))
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
