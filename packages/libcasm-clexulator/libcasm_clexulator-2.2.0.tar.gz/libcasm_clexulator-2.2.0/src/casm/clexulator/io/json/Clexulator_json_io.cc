#include "casm/clexulator/io/json/Clexulator_json_io.hh"

#include "casm/casm_io/json/InputParser_impl.hh"
#include "casm/clexulator/Clexulator.hh"
#include "casm/system/RuntimeLibrary.hh"

namespace CASM {
namespace clexulator {

namespace {

fs::path resolve_path(fs::path p, std::vector<fs::path> search_path) {
  fs::path resolved_path;
  if (fs::exists(p)) {
    return p;
  } else {
    for (fs::path root : search_path) {
      if (fs::exists(root / p)) {
        return root / p;
      }
    }
  }
  return p;
}

}  // namespace

/// \param parser An InputParser, as genrated by
///     `InputParser::subparse<std::shared_ptr<Clexulator>>` or one of the other
///     `subparse` methods.
/// \param prim_neighbor_list If not empty, will be used to share neighbor lists
///      among multiple cluster expansions. If sharing, may throw if the
///      Clexulator require different parameters.
///
/// Expected JSON format:
///   source: string (required)
///     Path to a Clexulator source file implementing a basis set.
///
///   compile_options: (optional)
///     Options used to compile the Clexulator source file, if it is not yet
///     compiled. Example: "g++ -O3 -Wall -fPIC --std=c++17 -I/path/to/include"
///
///   so_options: (optional)
///     Options used to compile the Clexulator shared object file, if it is not
///     yet compiled. Example: "g++ -shared -L/path/to/lib -lcasm_clexulator "
void parse(InputParser<Clexulator> &parser,
           std::shared_ptr<PrimNeighborList> &prim_neighbor_list,
           std::vector<fs::path> search_path) {
  // parse "source"
  std::string _clexulator_src;
  parser.require(_clexulator_src, "source");
  fs::path clexulator_src = resolve_path(_clexulator_src, search_path);
  if (!fs::exists(clexulator_src)) {
    parser.insert_error("source", "Error: \"source\" file does not exist.");
  }

  if (!parser.valid()) {
    return;
  }

  // - name of Clexulator source file (excluding .cc extension)
  std::string clexulator_name = clexulator_src.stem();

  // - directory where the Clexulator source file is found
  fs::path clexulator_dirpath = clexulator_src.parent_path();

  // - set Clexulator compilation options
  //   ex: g++ -O3 -Wall -fPIC --std=c++17 -I/path/to/include
  std::string default_clexulator_compile_options =
      //
      // uses $CASM_CXX, else default="g++"
      RuntimeLibrary::default_cxx().first + " " +
      //
      // uses $CASM_CXXFLAGS, else default="-O3 -Wall -fPIC --std=c++17"
      RuntimeLibrary::default_cxxflags().first + " " +
      //
      // uses -I$CASM_INCLUDEDIR,
      //   else -I$CASM_PREFIX/include,
      //   else tries to find "ccasm" or "casm" executable on PATH and looks
      //     for standard include paths relative from there,
      //   else fails with "/not/found"
      include_path(RuntimeLibrary::default_casm_includedir().first);

  std::string clexulator_compile_options;
  parser.optional_else(clexulator_compile_options, "compile_options",
                       default_clexulator_compile_options);

  // - set Clexulator shared object compilation options
  //   ex: g++ -shared -L/path/to/lib -lcasm_global -lcasm_crystallography
  //     -lcasm_clexulator -lcasm_monte
  std::string default_clexulator_so_options =
      //
      // uses $CASM_CXX, else default="g++"
      RuntimeLibrary::default_cxx().first + " " +
      //
      // uses $CASM_SOFLAGS, else default="-shared"
      RuntimeLibrary::default_soflags().first + " " +
      //
      // uses -L$CASM_LIBDIR,
      //   else -L$CASM_PREFIX/lib,
      //   else tries to find "ccasm" or "casm" executables on PATH and looks
      //     for libcasm at standard relative paths from there,
      //   else fails with "-L/not/found"
      link_path(RuntimeLibrary::default_casm_libdir().first) + " " +
      //
      // requires libcasm_clexulator:
      "-lcasm_clexulator ";

  std::string clexulator_so_options;
  parser.optional_else(clexulator_so_options, "so_options",
                       default_clexulator_so_options);

  // notes:
  // - The prim_neighbor_list will be constructed / expanded as necessary
  // - Standard practice if >1 clexulator is needed is that the
  //   prim_neighbor_list will be the same for all clexulator. However, this
  //   is not strictly necessary. If clexulator require different
  //   PrimNeighborList, then different SuperNeighborList are also required
  //   to be contructed from each PrimNeighborList.
  if (parser.valid()) {
    parser.value = std::make_unique<Clexulator>(
        make_clexulator(clexulator_name, clexulator_dirpath, prim_neighbor_list,
                        clexulator_compile_options, clexulator_so_options));
  }
}

/// \param parser An InputParser, as genrated by
///     `InputParser::subparse<std::vector<Clexulator>>` or one of the other
///     `subparse` methods.
/// \param prim_neighbor_list If not empty, will be used to share neighbor lists
///      among multiple cluster expansions. If sharing, may throw if the
///      Clexulator require different parameters.
///
/// Expected JSON format:
///   source: string (required)
///     Path to a directory containing local Clexulators.
///
///   compile_options: (optional)
///     Options used to compile the Clexulator source file, if it is not yet
///     compiled. Example: "g++ -O3 -Wall -fPIC --std=c++17 -I/path/to/include"
///
///   so_options: (optional)
///     Options used to compile the Clexulator shared object file, if it is not
///     yet compiled. Example: "g++ -shared -L/path/to/lib -lcasm_clexulator "
void parse(InputParser<std::vector<Clexulator>> &parser,
           std::shared_ptr<PrimNeighborList> &prim_neighbor_list,
           std::vector<fs::path> search_path) {
  // parse "source"
  std::string _clexulator_src;
  parser.require(_clexulator_src, "source");
  fs::path clexulator_src = resolve_path(_clexulator_src, search_path);

  if (!fs::exists(clexulator_src)) {
    parser.insert_error("source", "Error: \"source\" file does not exist.");
  }

  if (!parser.valid()) {
    return;
  }

  // - name of Clexulator source file (excluding .cc extension)
  std::string clexulator_name = clexulator_src.stem();

  // - directory where the Clexulator source file is found
  fs::path clexulator_dirpath = clexulator_src.parent_path();

  // - set Clexulator compilation options
  //   ex: g++ -O3 -Wall -fPIC --std=c++17 -I/path/to/include
  std::string default_clexulator_compile_options =
      //
      // uses $CASM_CXX, else default="g++"
      RuntimeLibrary::default_cxx().first + " " +
      //
      // uses $CASM_CXXFLAGS, else default="-O3 -Wall -fPIC --std=c++17"
      RuntimeLibrary::default_cxxflags().first + " " +
      //
      // uses -I$CASM_INCLUDEDIR,
      //   else -I$CASM_PREFIX/include,
      //   else tries to find "ccasm" or "casm" executable on PATH and looks
      //     for standard include paths relative from there,
      //   else fails with "/not/found"
      include_path(RuntimeLibrary::default_casm_includedir().first);

  std::string clexulator_compile_options;
  parser.optional_else(clexulator_compile_options, "compile_options",
                       default_clexulator_compile_options);

  // - set Clexulator shared object compilation options
  //   ex: g++ -shared -L/path/to/lib -lcasm_global -lcasm_crystallography
  //     -lcasm_clexulator -lcasm_monte
  std::string default_clexulator_so_options =
      //
      // uses $CASM_CXX, else default="g++"
      RuntimeLibrary::default_cxx().first + " " +
      //
      // uses $CASM_SOFLAGS, else default="-shared"
      RuntimeLibrary::default_soflags().first + " " +
      //
      // uses -L$CASM_LIBDIR,
      //   else -L$CASM_PREFIX/lib,
      //   else tries to find "ccasm" or "casm" executables on PATH and looks
      //     for libcasm at standard relative paths from there,
      //   else fails with "-L/not/found"
      link_path(RuntimeLibrary::default_casm_libdir().first) + " " +
      //
      // requires libcasm_clexulator:
      "-lcasm_clexulator ";

  std::string clexulator_so_options;
  parser.optional_else(clexulator_so_options, "so_options",
                       default_clexulator_so_options);

  // notes:
  // - The prim_neighbor_list will be constructed / expanded as necessary
  // - Standard practice if >1 clexulator is needed is that the
  //   prim_neighbor_list will be the same for all clexulator. However, this
  //   is not strictly necessary. If clexulator require different
  //   PrimNeighborList, then different SuperNeighborList are also required
  //   to be contructed from each PrimNeighborList.
  if (parser.valid()) {
    parser.value =
        std::make_unique<std::vector<Clexulator>>(make_local_clexulator(
            clexulator_name, clexulator_dirpath, prim_neighbor_list,
            clexulator_compile_options, clexulator_so_options));
  }
}

}  // namespace clexulator
}  // namespace CASM
