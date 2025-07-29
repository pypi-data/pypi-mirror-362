#include "casm/clexulator/ImpactTable.hh"

namespace CASM {
namespace clexulator {

/// \brief Constructor
///
/// \param prim_event_list A vector of EventImpactInfo, providing the impact
///     information for all possible events in the origin unit cell.
/// \param transformation_matrix_to_super Defines the supercell in which events
///     will be occuring (S = P * T, where S = supercell lattice column matrix,
///     P = prim lattice column matrix, T = transformation_matrix_to_super)
RelativeEventImpactTable::RelativeEventImpactTable(
    std::vector<EventImpactInfo> const &prim_event_list,
    Eigen::Matrix3l const &transformation_matrix_to_super)
    : m_impact_table(make_relative_impact_table(prim_event_list)),
      m_unitcell_converter(transformation_matrix_to_super) {}

/// \brief Constructor
///
/// \param prim_event_list A vector of EventImpactInfo, providing the impact
///     information for all possible events in the origin unit cell.
/// \param transformation_matrix_to_super Defines the supercell in which events
///     will be occuring (S = P * T, where S = supercell lattice column matrix,
///     P = prim lattice column matrix, T = transformation_matrix_to_super)
SupercellEventImpactTable::SupercellEventImpactTable(
    std::vector<EventImpactInfo> const &prim_event_list,
    Eigen::Matrix3l const &transformation_matrix_to_super)
    : m_n_prim_events(prim_event_list.size()) {
  RelativeEventImpactTable relative_impact_table(
      prim_event_list, transformation_matrix_to_super);

  Index n_unitcells = transformation_matrix_to_super.determinant();
  EventID event_id;

  // loop order matters, it must be consistent
  //   with the linear_index definition in operator()
  for (Index unitcell_index = 0; unitcell_index < n_unitcells;
       ++unitcell_index) {
    for (Index prim_event_index = 0; prim_event_index < m_n_prim_events;
         ++prim_event_index) {
      event_id.prim_event_index = prim_event_index;
      event_id.unitcell_index = unitcell_index;
      m_impact_table.push_back(relative_impact_table(event_id));
    }
  }
}

namespace {

/// \brief Make translations which map phenomenal_sites onto sites in the
/// required_update_neighborhood
///
/// Impact translations are all 'trans' such that:
///
///     neighborhood_site == phenom_site + trans
///
std::set<xtal::UnitCell> make_impact_translations(
    std::set<xtal::UnitCellCoord> const &required_update_neighborhood,
    std::vector<xtal::UnitCellCoord> const &phenomenal_sites) {
  std::set<xtal::UnitCell> translations;
  for (xtal::UnitCellCoord const &nbor_site : required_update_neighborhood) {
    for (xtal::UnitCellCoord const &phenom_site : phenomenal_sites) {
      if (nbor_site.sublattice() == phenom_site.sublattice()) {
        translations.insert(nbor_site.unitcell() - phenom_site.unitcell());
      }
    }
  }
  return translations;
}

}  // namespace

/// \brief Return an impact table for events in the origin unit cell
///
/// \param prim_event_list A vector of EventImpactInfo, providing the impact
///     information for all possible events in the origin unit cell.
///
/// \returns relative_impact_table, where relative_impact_table[i] is the
///     vector of events (specified relative to the origin unit cell) which are
///     impacted by the occurance of event `prim_event_list[i]` in the origin
///     unit cell.
///
std::vector<std::vector<RelativeEventID>> make_relative_impact_table(
    std::vector<EventImpactInfo> const &prim_event_list) {
  std::vector<std::vector<RelativeEventID>> impact_table;
  impact_table.resize(prim_event_list.size());
  RelativeEventID relative_event_id;
  xtal::UnitCell zero_translation(0, 0, 0);

  for (Index i = 0; i < prim_event_list.size(); ++i) {
    for (Index j = 0; j < prim_event_list.size(); ++j) {
      // translations are 'trans' such that:
      // event (j, trans) impacts event (i, zero)
      std::set<xtal::UnitCell> translations = make_impact_translations(
          prim_event_list[i].required_update_neighborhood,
          prim_event_list[j].phenomenal_sites);

      for (xtal::UnitCell const &trans : translations) {
        if (i == j && trans == zero_translation) continue;
        // -> event (j, zero) impacts event (i, -trans)
        relative_event_id.prim_event_index = i;
        relative_event_id.translation = -trans;
        impact_table[j].push_back(relative_event_id);
      }
    }
  }
  return impact_table;
}

}  // namespace clexulator
}  // namespace CASM
