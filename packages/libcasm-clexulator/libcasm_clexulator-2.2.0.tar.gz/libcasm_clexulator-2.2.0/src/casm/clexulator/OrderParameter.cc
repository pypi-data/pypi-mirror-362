#include "casm/clexulator/OrderParameter.hh"

#include "casm/clexulator/ConfigDoFValues.hh"
#include "casm/clexulator/DoFSpace.hh"
#include "casm/crystallography/Superlattice.hh"

namespace CASM {
namespace clexulator {

namespace OrderParameter_impl {

/// \brief Make a linear site index conversion table to map sites
///     between supercells, including periodic images
///
/// There are two supercells, s1 and s2. There is also s3, the
/// minimal commensurate supercell of s1 and s2. This returns a
/// lookup table for sites in s2 that periodic images of a given
/// site in s1 map onto when placed within s2.
///
/// Example, prim is simple cubic with 1 sublattice:
/// - s1 is a NxNxN supercell
/// - s2 is a 1x1x1 supercell
/// - s3 is the commensurate supercell (NxNxN)
/// - this returns:
///   - s1_to_s2_sites[0] = {0},
///   - s1_to_s2_sites[1] = {0},
///   - ...
///   - s1_to_s2_sites[N*N*N-1] = {0}
///
/// Example, prim is simple cubic with 1 sublattice:
/// - s1 is a 1x1x1 supercell
/// - s2 is a NxNxN supercell
/// - s3 is the commensurate supercell (NxNxN)
/// - this returns:
///   - s1_to_s2_sites[0] = {0, 1, ..., N*N*N-1}
///
/// Example, prim is simple cubic with 1 sublattice:
/// - s1 is a 2x2x2 supercell
/// - s2 is a 3x3x3 supercell
/// - s3 is the commensurate supercell (6x6x6)
/// - this returns:
///   - s1_to_s2_sites[0] = <size 27 vector>,
///   - s1_to_s2_sites[1] = <size 27 vector>,
///   - ...
///   - s1_to_s2_sites[7] = <size 27 vector>
///
/// \param s1_converter, a xtal::UnitCellCoordIndexConverter for s1
/// \param s1_T, the transformation_matrix_to_super for s1
/// \param s2_converter, a xtal::UnitCellCoordIndexConverter for s2
/// \param s1_to_s3_superlattice, a xtal::Superlattice of s1 and s3
/// \param s1_sites, a list of sites in s1 for which the lookup table
///     should be populated. If `s1_sites==std::nullopt` (default),
///     populate the lookup table for all sites in s1. For example,
///     if s1_sites has a value and the index l_s1, which is less than
///     `s1_converter.total_sites()`, is not included, then
///     `s1_to_s2_sites[l_s1].empty()==true`.
/// \param s2_sites, a list of sites in s2 which should be included in
///     the lookup table. If `s2_sites==std::nullopt` (default),
///     populate the lookup table for all sites in s2. For example,
///     if s2_sites has a value and the index l_s2, which is less than
///     `s2_converter.total_sites()`, is not included, then
///     `s1_to_s2_sites[i][j]!=l_s2` for all i, j.
///
/// \return s1_to_s2_sites, in which s1_to_s2_sites[l_s1] is a
///     std::vector<Index> providing the linear indices of sites in s2
///     which periodic images of l_s1 map onto when placed within s2.
std::vector<std::vector<Index>> make_commensurate_supercell_site_converter(
    xtal::UnitCellCoordIndexConverter const &s1_converter,
    Eigen::Matrix3l const &s1_T,
    xtal::UnitCellCoordIndexConverter const &s2_converter,
    xtal::Superlattice const &s1_to_s3_superlattice,
    std::optional<std::set<Index>> s1_sites = std::nullopt,
    std::optional<std::set<Index>> s2_sites = std::nullopt) {
  if (!s1_sites.has_value()) {
    std::set<Index> tmp;
    for (Index i = 0; i < s1_converter.total_sites(); ++i) {
      tmp.emplace(i);
    }
    s1_sites = tmp;
  }
  if (!s2_sites.has_value()) {
    std::set<Index> tmp;
    for (Index i = 0; i < s2_converter.total_sites(); ++i) {
      tmp.emplace(i);
    }
    s2_sites = tmp;
  }

  // xtal::Superlattice s1_tiling_lattice{s1_lattice, commensurate_lattice};
  xtal::UnitCellIndexConverter tile_converter{
      s1_to_s3_superlattice.transformation_matrix_to_super()};
  Index N_tiles = tile_converter.total_sites();

  std::vector<std::vector<Index>> s1_to_s2_sites;
  Index N_s1_sites = s1_converter.total_sites();
  s1_to_s2_sites.resize(N_s1_sites);
  for (Index l_s1 : s1_sites.value()) {
    xtal::UnitCellCoord bijk_0 = s1_converter(l_s1);

    std::vector<Index> &curr = s1_to_s2_sites[l_s1];
    for (Index i = 0; i < N_tiles; ++i) {
      xtal::UnitCell tile_ijk = tile_converter(i);
      xtal::UnitCell ijk = s1_T * tile_ijk;
      xtal::UnitCellCoord bijk_i(bijk_0.sublattice(), bijk_0.unitcell() + ijk);
      Index l_s2 = s2_converter(bijk_i);
      if (s2_sites.value().count(l_s2)) {
        curr.push_back(l_s2);
      }
    }
  }
  return s1_to_s2_sites;
}

}  // namespace OrderParameter_impl

/// \class OrderParameter
/// \brief Method to calculate order parameters based on a DoFSpace basis
///
/// Use the OrderParameter class to efficiently calculate order parameters
/// and changes in order parameters when done repeatedly, as in Monte Carlo
/// calculations.

/// \brief Constructor
///
/// \param dof_space A DoFSpace defining the order parameter through the
///     choice of DoF type, included sites, and basis.
OrderParameter::OrderParameter(DoFSpace const &dof_space)
    : m_supercell_T(Eigen::Matrix3l::Zero()),
      m_dof_space(dof_space),
      m_is_occ(m_dof_space.dof_key == "occ"),
      m_delta_value(Eigen::VectorXd(m_dof_space.subspace_dim)),
      m_multisite_delta_value(Eigen::VectorXd(m_dof_space.subspace_dim)) {}

/// \brief Calculate and return order parameter value
///
/// Equivalent to `update(configuration).value()`
Eigen::VectorXd const &OrderParameter::operator()(
    Eigen::Matrix3l const &transformation_matrix_to_super,
    xtal::UnitCellCoordIndexConverter const &supercell_index_converter,
    ConfigDoFValues const *dof_values) {
  return this
      ->update(transformation_matrix_to_super, supercell_index_converter,
               dof_values)
      .value();
}

/// \brief Set internal data to calculate order parameters in a different
///     supercell
///
/// \param transformation_matrix_to_super Transformation matrix that
///     generates the supercell in which to calculation order parameters
/// \param supercell_index_converter UnitCellCoordIndexConverter for the
///     supercell in which the order parameter is begin calculated, which
///     may be different and not directly commensurate with the DoFSpace.
/// \param dof_values Pointer to the ConfigDoFValues to be used as input for
///     calculating the order parameter.
OrderParameter &OrderParameter::update(
    Eigen::Matrix3l const &transformation_matrix_to_super,
    xtal::UnitCellCoordIndexConverter const &supercell_index_converter,
    ConfigDoFValues const *dof_values) {
  if (dof_values != nullptr) {
    set(dof_values);
  }
  // do not need to create supercell site index lookup tables for global DoF
  if (m_dof_space.is_global) {
    return *this;
  }
  // skip if same supercell as current data
  if (m_supercell_T == transformation_matrix_to_super) {
    return *this;
  }

  // convention:
  //   s1 is `supercell` with configuration order parameter is calculated for
  ///  s2 is DoF space supercell,
  //   s3 is minimal commensurate supercell of s1 and s2

  m_supercell_T = transformation_matrix_to_super;
  Eigen::Matrix3l const &s1_T = m_supercell_T;
  Eigen::Matrix3l const &s2_T =
      m_dof_space.transformation_matrix_to_super.value();

  xtal::Lattice const &P = m_dof_space.prim->lattice();
  xtal::Lattice s1 = xtal::make_superlattice(P, m_supercell_T);
  xtal::Lattice s2 = xtal::make_superlattice(P, s2_T);

  xtal::UnitCellCoordIndexConverter const &s1_converter =
      supercell_index_converter;
  int basis_size = m_dof_space.prim->basis().size();
  xtal::UnitCellCoordIndexConverter s2_converter{s2_T, basis_size};

  std::optional<std::set<Index>> s1_sites = std::nullopt;  // include all sites
  std::optional<std::set<Index>> const &s2_sites = m_dof_space.sites;

  std::vector<xtal::Lattice> lattices({s1, s2});
  xtal::Lattice s3 = xtal::make_superduperlattice(s1, s2);
  xtal::Superlattice s1_to_s3_superlattice{s1, s3};
  xtal::Superlattice s2_to_s3_superlattice{s2, s3};

  m_N_dof_space_tilings = s2_to_s3_superlattice.size();

  using OrderParameter_impl::make_commensurate_supercell_site_converter;
  m_supercell_to_dof_space_sites = make_commensurate_supercell_site_converter(
      s1_converter, s1_T, s2_converter, s1_to_s3_superlattice, s1_sites,
      s2_sites);

  m_dof_space_to_supercell_sites = make_commensurate_supercell_site_converter(
      s2_converter, s2_T, s1_converter, s2_to_s3_superlattice, s2_sites,
      s1_sites);

  return *this;
}

/// \brief Reset internal pointer to DoF values - must have the same supercell
///
/// \param _dof_values Pointer to the ConfigDoFValues to be used as input for
///     calculating the order parameter. The ConfigDoFValues object being
///     used as input may be modified between calls, but the pointers to the
///     underlying global and local DoF value vectors and matrices must remain
///     valid (i.e. they must not be erased) or a new OrderParameter
///     object should be used.
///
void OrderParameter::set(ConfigDoFValues const *_dof_values) {
  if (_dof_values == nullptr) {
    throw std::runtime_error(
        "Error in OrderParameter::set: _dof_values == nullptr");
  }
  m_dof_values = _dof_values;
  if (m_dof_space.is_global) {
    m_global_dof_values =
        &m_dof_values->global_dof_values.at(m_dof_space.dof_key);
  } else if (m_is_occ) {
    m_occ_values = &m_dof_values->occupation;
    m_prim_occ_values.resize(m_dof_space.dim);
  } else {
    m_local_dof_values =
        &m_dof_values->local_dof_values.at(m_dof_space.dof_key);
    m_prim_local_dof_values.resize(m_dof_space.dim);
  }
}

/// \brief Get internal pointer to DoF values
ConfigDoFValues const *OrderParameter::get() const { return m_dof_values; }

/// \brief Calculate and return current order parameter value
Eigen::VectorXd const &OrderParameter::value() {
  if (m_dof_space.is_global) {
    if (m_global_dof_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_value = m_dof_space.basis_inv * (*m_global_dof_values);
  } else if (m_is_occ) {
    if (m_occ_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_prim_occ_values.setZero();
    auto const &axis_site_index = *m_dof_space.axis_info.site_index;
    auto const &axis_dof_component = *m_dof_space.axis_info.dof_component;
    for (Index i = 0; i < axis_site_index.size(); ++i) {
      Index l_dof_space = axis_site_index[i];
      Index dof_component = axis_dof_component[i];
      for (Index l : m_dof_space_to_supercell_sites[l_dof_space]) {
        if ((*m_occ_values)(l) == dof_component) {
          m_prim_occ_values(i) += 1;
        }
      }
    }
    m_value = m_dof_space.basis_inv * m_prim_occ_values.cast<double>() /
              m_N_dof_space_tilings;
  } else {
    if (m_local_dof_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_prim_local_dof_values.setZero();
    auto const &axis_site_index = *m_dof_space.axis_info.site_index;
    auto const &axis_dof_component = *m_dof_space.axis_info.dof_component;
    for (Index i = 0; i < axis_site_index.size(); ++i) {
      Index l_dof_space = axis_site_index[i];
      Index dof_component = axis_dof_component[i];
      for (Index l : m_dof_space_to_supercell_sites[l_dof_space]) {
        m_prim_local_dof_values(i) += (*m_local_dof_values)(dof_component, l);
      }
    }
    m_value =
        m_dof_space.basis_inv * m_prim_local_dof_values / m_N_dof_space_tilings;
  }
  return m_value;
}

/// \brief Calculate and return change in order parameter value due to
///     an occupation change, relative to the current ConfigDoFValues
Eigen::VectorXd const &OrderParameter::occ_delta_value(Index linear_site_index,
                                                       Index new_occ) {
  Index N_images = m_supercell_to_dof_space_sites[linear_site_index].size();
  if (N_images) {
    if (m_occ_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_prim_occ_values.setZero();
    Index curr_occ = (*m_occ_values)[linear_site_index];
    auto const &basis_row_index = *m_dof_space.axis_info.basis_row_index;
    for (Index l_dof_space :
         m_supercell_to_dof_space_sites[linear_site_index]) {
      m_prim_occ_values(basis_row_index[l_dof_space][curr_occ]) -= 1;
      m_prim_occ_values(basis_row_index[l_dof_space][new_occ]) += 1;
    }
    m_delta_value = m_dof_space.basis_inv * m_prim_occ_values.cast<double>() /
                    m_N_dof_space_tilings;
  } else {
    m_delta_value.setZero();
  }
  return m_delta_value;
}

/// \brief Calculate change in order parameter value due to a
///     series of occupation changes
Eigen::VectorXd const &OrderParameter::occ_delta_value(
    std::vector<Index> const &linear_site_index,
    std::vector<int> const &new_occ) {
  // we need to store the current occupation and modify it to calculate a
  // multi-site delta we'll revert the occupation to its original values before
  // leaving...
  Eigen::VectorXi &occupation = const_cast<Eigen::VectorXi &>(*m_occ_values);
  if (m_tmp_occ.size() < new_occ.size()) {
    m_tmp_occ.resize(new_occ.size());
  }
  // calculate delta
  m_multisite_delta_value.setZero();
  for (Index i = 0; i < linear_site_index.size(); ++i) {
    Index l = linear_site_index[i];
    m_multisite_delta_value += this->occ_delta_value(l, new_occ[i]);
    // store original occupation
    m_tmp_occ[i] = occupation(l);
    occupation(l) = new_occ[i];
  }
  // revert occupation
  for (Index i = 0; i < linear_site_index.size(); ++i) {
    occupation(linear_site_index[i]) = m_tmp_occ[i];
  }
  return m_multisite_delta_value;
}

/// \brief Calculate and return change in order parameter value due to
///     a local DoF change, relative to the current ConfigDoFValues
Eigen::VectorXd const &OrderParameter::local_delta_value(
    Index linear_site_index, Eigen::VectorXd const &new_value) {
  Index N_images = m_supercell_to_dof_space_sites[linear_site_index].size();
  if (N_images) {
    if (m_local_dof_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_prim_local_dof_values.setZero();
    Eigen::VectorXd const &curr_value =
        m_local_dof_values->col(linear_site_index);
    auto const &basis_row_index = *m_dof_space.axis_info.basis_row_index;
    for (Index l_dof_space :
         m_supercell_to_dof_space_sites[linear_site_index]) {
      int j = 0;
      for (Index i : basis_row_index[l_dof_space]) {
        m_prim_local_dof_values(i) += (new_value(j) - curr_value(j));
        ++j;
      }
    }
    m_delta_value =
        m_dof_space.basis_inv * m_prim_local_dof_values / m_N_dof_space_tilings;
  } else {
    m_delta_value.setZero();
  }
  return m_delta_value;
}

/// \brief Calculate and return change in order parameter value due to
///     a local DoF change, relative to the current ConfigDoFValues
Eigen::VectorXd const &OrderParameter::local_delta_value(
    Index linear_site_index, Index dof_component, double new_value) {
  Index N_images = m_supercell_to_dof_space_sites[linear_site_index].size();
  if (N_images) {
    if (m_local_dof_values == nullptr) {
      throw std::runtime_error(
          "Error in OrderParameter: ConfigDoFValues not set");
    }
    m_prim_local_dof_values.setZero();
    double curr_value =
        m_local_dof_values->col(linear_site_index)(dof_component);
    auto const &basis_row_index = *m_dof_space.axis_info.basis_row_index;
    for (Index l_dof_space :
         m_supercell_to_dof_space_sites[linear_site_index]) {
      m_prim_local_dof_values(basis_row_index[l_dof_space][dof_component]) +=
          (new_value - curr_value);
    }
    m_delta_value =
        m_dof_space.basis_inv * m_prim_local_dof_values / m_N_dof_space_tilings;
  } else {
    m_delta_value.setZero();
  }
  return m_delta_value;
}

/// \brief Calculate and return change in order parameter value due to
///     a global DoF change, relative to the current ConfigDoFValues
Eigen::VectorXd const &OrderParameter::global_delta_value(
    Eigen::VectorXd const &new_value) {
  if (m_global_dof_values == nullptr) {
    throw std::runtime_error(
        "Error in OrderParameter: ConfigDoFValues not set");
  }
  m_delta_value = m_dof_space.basis_inv * (new_value - *m_global_dof_values);
  return m_delta_value;
}

/// \brief Calculate and return change in order parameter value due to
///     a global DoF change, relative to the current ConfigDoFValues
Eigen::VectorXd const &OrderParameter::global_delta_value(Index dof_component,
                                                          double new_value) {
  if (m_global_dof_values == nullptr) {
    throw std::runtime_error(
        "Error in OrderParameter: ConfigDoFValues not set");
  }
  m_delta_value = m_dof_space.basis_inv.col(dof_component) *
                  (new_value - (*m_global_dof_values)(dof_component));
  return m_delta_value;
}

}  // namespace clexulator
}  // namespace CASM
