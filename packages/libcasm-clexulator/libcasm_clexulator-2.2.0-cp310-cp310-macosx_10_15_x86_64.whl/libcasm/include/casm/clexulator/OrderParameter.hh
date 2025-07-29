#ifndef CASM_clexulator_OrderParameter
#define CASM_clexulator_OrderParameter

#include <optional>

#include "casm/clexulator/DoFSpace.hh"
#include "casm/crystallography/DoFDecl.hh"

namespace CASM {
namespace clexulator {

/// \brief Method to calculate order parameters based on a DoFSpace basis
class OrderParameter {
 public:
  /// \brief Constructor
  OrderParameter(DoFSpace const &dof_space);

  /// \brief Calculate and return order parameter value
  Eigen::VectorXd const &operator()(
      Eigen::Matrix3l const &transformation_matrix_to_super,
      xtal::UnitCellCoordIndexConverter const &supercell_index_converter,
      ConfigDoFValues const *dof_values);

  /// \brief If necessary, reset internal data to calculate order
  ///     parameters in a different supercell
  OrderParameter &update(
      Eigen::Matrix3l const &transformation_matrix_to_super,
      xtal::UnitCellCoordIndexConverter const &supercell_index_converter,
      ConfigDoFValues const *dof_values = nullptr);

  /// \brief Reset internal pointer to DoF values - must have the same supercell
  void set(ConfigDoFValues const *dof_values);

  /// \brief Get internal pointer to DoF values
  ConfigDoFValues const *get() const;

  /// \brief Calculate and return current order parameter value
  Eigen::VectorXd const &value();

  /// \brief Calculate and return change in order parameter value due to
  ///     an occupation change, relative to the current ConfigDoFValues
  Eigen::VectorXd const &occ_delta_value(Index linear_site_index,
                                         Index new_occ);

  /// \brief Calculate change in order parameter value due to a
  ///     series of occupation changes
  Eigen::VectorXd const &occ_delta_value(
      std::vector<Index> const &linear_site_index,
      std::vector<int> const &new_occ);

  /// \brief Calculate and return change in order parameter value due to
  ///     a local DoF change, relative to the current ConfigDoFValues
  Eigen::VectorXd const &local_delta_value(Index linear_site_index,
                                           Eigen::VectorXd const &new_value);

  /// \brief Calculate and return change in order parameter value due to
  ///     a local DoF change, relative to the current ConfigDoFValues
  Eigen::VectorXd const &local_delta_value(Index linear_site_index,
                                           Index dof_component,
                                           double new_value);

  /// \brief Calculate and return change in order parameter value due to
  ///     a global DoF change, relative to the current ConfigDoFValues
  Eigen::VectorXd const &global_delta_value(Eigen::VectorXd const &new_value);

  /// \brief Calculate and return change in order parameter value due to
  ///     a global DoF change, relative to the current ConfigDoFValues
  Eigen::VectorXd const &global_delta_value(Index dof_component,
                                            double new_value);

 private:
  /// Supercell transformation matrix corresponding to internal data
  Eigen::Matrix3l m_supercell_T;

  /// DoFSpace to use
  DoFSpace const m_dof_space;

  /// Note if occupation degrees of freedom. Set at construction.
  bool m_is_occ;

  /// Holds order parameter value when it has been calculated
  Eigen::VectorXd m_value;

  /// Holds delta order parameter value when it has been calculated
  Eigen::VectorXd m_delta_value;

  /// Used to temporarily hold occupation values when calculating delta values
  std::vector<int> m_tmp_occ;

  /// Holds multi-site change delta order parameter value when it has been
  /// calculated
  Eigen::VectorXd m_multisite_delta_value;

  /// Holds occupation DoF values as a temporary, for example to do:
  ///     m_value = m_dof_space.basis_inv * m_prim_occ_values
  Eigen::VectorXi m_prim_occ_values;

  /// Holds local DoF values as a temporary, for example to do:
  ///     m_value = m_dof_space.basis_inv * m_prim_local_dof_values
  Eigen::VectorXd m_prim_local_dof_values;

  /// DoF values to use
  ConfigDoFValues const *m_dof_values;

  /// Pointer to global DoF values. Set when m_dof_values is set.
  Eigen::VectorXd const *m_global_dof_values;

  /// Pointer to occupation DoF values. Set when m_dof_values is set.
  Eigen::VectorXi const *m_occ_values;

  /// Pointer to local DoF values. Set when m_dof_values is set.
  Eigen::MatrixXd const *m_local_dof_values;

  /// Number of times the DoF space tiles into a commensurate
  /// superlattice of supercell and DoF space, cast to double.
  /// Used for normalization.
  double m_N_dof_space_tilings;

  /// If supercell site l is included in the order parameter
  /// calculation, then m_supercell_to_dof_space_sites[l] is a
  /// vector<Index> giving the DoF space site index for each time it
  /// occurs in the mean value calculation; otherwise it is an empty
  /// vector. Used for efficient calculation of deltas.
  std::vector<std::vector<Index>> m_supercell_to_dof_space_sites;

  /// If DoF space site l is included in the DoF space, then
  /// m_dof_space_to_supercell_sites[l] is a vector<Index> giving
  /// the supercell linear site index for each time it occurs in
  /// the mean value calculation; otherwise it is an empty vector.
  /// Used for efficient calculation of order parameter value.
  std::vector<std::vector<Index>> m_dof_space_to_supercell_sites;
};

}  // namespace clexulator
}  // namespace CASM

#endif
