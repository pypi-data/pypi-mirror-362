#include "casm/configuration/clusterography/io/json/IntegralClusterOrbitGenerator_json_io.hh"

#include "casm/casm_io/container/json_io.hh"
#include "casm/casm_io/json/InputParser_impl.hh"
#include "casm/casm_io/json/jsonParser.hh"
#include "casm/configuration/clusterography/IntegralClusterOrbitGenerator.hh"
#include "casm/configuration/clusterography/io/json/IntegralCluster_json_io.hh"

namespace CASM {

/// Write custom orbit specs to JSON
jsonParser &to_json(const clust::IntegralClusterOrbitGenerator &orbit_generator,
                    jsonParser &json, xtal::BasicStructure const &prim) {
  to_json(orbit_generator.prototype, json, prim);
  json["include_subclusters"] = orbit_generator.include_subclusters;
  return json;
}

/// Parse vector of IntegralClusterOrbitGenerator ("orbit_specs") from JSON
///
/// Format:
/// \code
/// [
///   {
///     "coordinate_mode" : ("FRAC", "CART", "INT" (default)) (optional)
///     "sites" : [ // also accepts "prototype"
///       [b, i, j, k],
///       ...
///     ],
///     "include_subclusters": <bool, optional, default=true>
///   },
///   ...
/// ]
/// \endcode
///
/// - Also accepts "prototype" in place of "sites"
void parse(
    InputParser<std::vector<clust::IntegralClusterOrbitGenerator>> &parser,
    xtal::BasicStructure const &prim) {
  const jsonParser &json = parser.self;

  if (!json.is_array()) {
    parser.error.insert(
        "Error reading orbit generating clusters: Expected a JSON array");
    return;
  }

  parser.value =
      notstd::make_unique<std::vector<clust::IntegralClusterOrbitGenerator>>();
  auto &custom_generators = *parser.value;
  try {
    // for each custom orbit
    Index i = 0;
    for (auto it = json.begin(); it != json.end(); ++it) {
      // read orbit generating cluster from JSON
      fs::path relpath = std::to_string(i);
      auto subparser = parser.subparse<clust::IntegralCluster>(relpath, prim);

      if (subparser->valid()) {
        // check if subclusters should be included (yes by default)
        bool include_subclusters;
        parser.optional_else(include_subclusters,
                             relpath / "include_subclusters", true);

        custom_generators.emplace_back(*(subparser->value),
                                       include_subclusters);
      } else {
        return;
      }
      ++i;
    }
  } catch (std::exception &e) {
    parser.error.insert(
        std::string("Error: Could not read orbit generating clusters: ") +
        e.what());
  }
}
}  // namespace CASM
