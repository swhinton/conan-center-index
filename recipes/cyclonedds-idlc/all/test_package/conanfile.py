import os
from conan import ConanFile

class CycloneDDSIdlTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def test(self):
        extension = ".exe" if self.settings_build.os == "Windows" else ""
        self.run(f"idlc{extension} HelloWorldData.idl")
        assert(os.path.isfile("HelloWorldData.h"))
        assert(os.path.isfile("HelloWorldData.c"))
