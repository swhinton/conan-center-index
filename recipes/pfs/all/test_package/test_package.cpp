#include <iostream>
#include <pfs/procfs.hpp>

int main() {
    try {
        pfs::procfs pfs;
        auto buddyinfo = pfs.get_buddyinfo();
        auto cmdline = pfs.get_cmdline();
        auto modules = pfs.get_modules();
        auto filesystems = pfs.get_filesystems();
        auto loadavg = pfs.get_loadavg();
        auto uptime = pfs.get_uptime();
        auto stats = pfs.get_stat();
        auto meminfo = pfs.get_meminfo();
        auto version = pfs.get_version();
        auto version_signature = pfs.get_version_signature();
        auto controllers = pfs.get_cgroups();
        return 0;
    } catch (const std::exception& e) {
        std::cout << "exception: " << e.what() << std::endl;
    }
}
