#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>    // ✅ Add this for flushing
#include <cstdio>      // ✅ Needed for fflush()

extern "C" int main_convex(int argc, char** argv);

namespace py = pybind11;

PYBIND11_MODULE(_optmsa_cnv, m) {
    m.doc() = "MSAMDD convex-gap alignment";

    m.def("run_convex",
        [](const std::vector<std::string>& flags) {
            std::vector<const char*> argv;
            argv.reserve(flags.size() + 1);
            argv.push_back("optmsa_cnv");
            for (auto& s : flags)
                argv.push_back(s.c_str());

            int result = main_convex((int)argv.size(), const_cast<char**>(argv.data()));

            // ✅ FLUSH both C++ and C std streams
            std::cout << std::flush;
            std::cerr << std::flush;
            fflush(stdout);
            fflush(stderr);

            return result;
        },
        py::arg("flags") = std::vector<std::string>{}
    );
}
