#ifndef CASM_clexulator_DoFSpace
#define CASM_clexulator_DoFSpace

#include <optional>
#include <set>

#include "casm/clexulator/DoFSpaceAxisInfo.hh"
#include "casm/crystallography/BasicStructure.hh"
#include "casm/crystallography/DoFDecl.hh"
#include "casm/crystallography/LinearIndexConverter.hh"
#include "casm/global/eigen.hh"

namespace CASM {
class AnisoValTraits;

namespace xtal {
class BasicStructure;
class Coordinate;
class UnitCell;
class UnitCellCoordIndexConverter;
}  // namespace xtal

namespace clexulator {
struct ConfigDoFValues;

/// \brief
struct DoFSpace {
 public:
  /// \brief Constructor
  DoFSpace(DoFKey const &dof_key,
           std::shared_ptr<xtal::BasicStructure const> const &prim,
           std::optional<Eigen::Matrix3l> transformation_matrix_to_super =
               std::nullopt,
           std::optional<std::set<Index>> sites = std::nullopt,
           std::optional<Eigen::MatrixXd> basis = std::nullopt);

  /// Type of degree of freedom that is under consideration (e.g., "disp",
  /// "Hstrain", "occ")
  DoFKey const dof_key;

  /// Store if dof_key names a global DoF type vs local DoF type
  bool const is_global;

  /// Shared prim
  std::shared_ptr<xtal::BasicStructure const> const prim;

  /// Specifies the supercell for a DoF space of site DoF. Has value for site
  /// DoF only.
  std::optional<Eigen::Matrix3l> const transformation_matrix_to_super;

  /// The sites included in a DoF space of site DoF. Has value for site DoF
  /// only.
  std::optional<std::set<Index>> const sites;

  /// The DoF space dimension (equal to number of rows in basis).
  Index const dim;

  /// The DoF space basis, as a column vector matrix. May be a subspace (cols <=
  /// rows).
  Eigen::MatrixXd const basis;

  /// The pseudo-inverse of basis.
  Eigen::MatrixXd const basis_inv;

  /// The DoF subspace dimension (equal to number of columns in basis).
  Index const subspace_dim;

  /// Holds description of each dimension (row) of the DoFSpace basis
  DoFSpaceAxisInfo const axis_info;

 private:
  friend DoFSpace make_dof_space(
      DoFKey const &dof_key,
      std::shared_ptr<xtal::BasicStructure const> const &prim,
      std::optional<Eigen::Matrix3l> transformation_matrix_to_super,
      std::optional<std::set<Index>> sites,
      std::optional<Eigen::MatrixXd> basis);

  /// \brief Private constructor, implemented to initialize const members
  DoFSpace(DoFKey const &_dof_key,
           std::shared_ptr<xtal::BasicStructure const> const &_prim,
           std::optional<Eigen::Matrix3l> &&_transformation_matrix_to_super,
           std::optional<std::set<Index>> &&_sites,
           std::optional<Eigen::MatrixXd> &&_basis,
           AnisoValTraits const &_aniso_val_traits,
           DoFSpaceAxisInfo &&_axis_glossary);
};

/// \brief Make a DoFSpace (global or local DoF)
DoFSpace make_dof_space(DoFKey const &dof_key,
                        std::shared_ptr<xtal::BasicStructure const> const &prim,
                        std::optional<Eigen::Matrix3l>
                            transformation_matrix_to_super = std::nullopt,
                        std::optional<std::set<Index>> sites = std::nullopt,
                        std::optional<Eigen::MatrixXd> basis = std::nullopt);

/// \brief Make a DoFSpace, convenience overload for global DoF
DoFSpace make_global_dof_space(
    DoFKey dof_key, std::shared_ptr<xtal::BasicStructure const> const &_prim,
    std::optional<Eigen::MatrixXd> basis = std::nullopt);

/// \brief Make a DoFSpace, convenience overload for local DoF
DoFSpace make_local_dof_space(
    DoFKey dof_key, std::shared_ptr<xtal::BasicStructure const> const &_prim,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    std::optional<std::set<Index>> sites = std::nullopt,
    std::optional<Eigen::MatrixXd> basis = std::nullopt);

/// \brief Return dimension of DoFSpace
Index get_dof_space_dimension(
    DoFKey dof_key, xtal::BasicStructure const &prim,
    std::optional<Eigen::Matrix3l> const &transformation_matrix_to_super =
        std::nullopt,
    std::optional<std::set<Index>> const &sites = std::nullopt);

/// True, if local DoF space with all sites in the supercell included
bool includes_all_sites(DoFSpace const &dof_space);

/// Return true if `dof_space` is valid for `transformation_matrix_to_super`
///
/// Checks that:
/// - For local DoF, that the transformation_matrix_to_super are equivalent
bool is_valid_dof_space(Eigen::Matrix3l const &transformation_matrix_to_super,
                        DoFSpace const &dof_space);

/// Throw if `!is_valid_dof_space(transformation_matrix_to_super, dof_space)`
void throw_if_invalid_dof_space(
    Eigen::Matrix3l const &transformation_matrix_to_super,
    DoFSpace const &dof_space);

/// \brief Perform conversions between site indices for an
///     arbitrary supercell and the supercell of a DoFSpace
struct DoFSpaceIndexConverter {
  DoFSpaceIndexConverter(
      xtal::UnitCellCoordIndexConverter const &_supercell_index_converter,
      DoFSpace const &dof_space);

  std::shared_ptr<xtal::BasicStructure const> const prim;
  xtal::UnitCellCoordIndexConverter const &supercell_index_converter;
  xtal::UnitCellCoordIndexConverter const dof_space_index_converter;

  /// Perform conversion from Coordinate to DoFSpace site index
  Index dof_space_site_index(xtal::Coordinate const &coord,
                             double tol = TOL) const;

  /// Perform conversion from DoFSpace site index to supercell site index
  Index dof_space_site_index(Index supercell_site_index) const;

  /// Perform conversion from Coordinate to supercell site index
  Index supercell_site_index(xtal::Coordinate const &coord,
                             double tol = TOL) const;

  /// Perform conversion from DoFSpace site index to supercell site index
  Index supercell_site_index(Index dof_space_site_index) const;

  /// \brief Perform conversion from DoFSpace site index to supercell site
  /// index, with additional translation within supercell
  Index supercell_site_index(Index dof_space_site_index,
                             xtal::UnitCell const &translation) const;
};

/// \brief Removes the homogeneous mode space from the DoFSpace basis
DoFSpace exclude_homogeneous_mode_space(DoFSpace const &dof_space);

/// \brief Make the homogeneous mode space of a local DoFSpace
Eigen::MatrixXd make_homogeneous_mode_space(DoFSpace const &dof_space);

/// Removes the default occupation modes from the DoFSpace basis
DoFSpace exclude_default_occ_modes(DoFSpace const &dof_space);

/// \brief A struct which gives out the mixing information of given
/// `column_vector_space` and a subspace
///
/// For example, consider a column_vector_space of 3 dimensions.
/// Let it be `[q1, q2, q3]` where `q1`, `q2` and `q3` are columns
/// of the vector space. If:
///
/// - `q1`: has a zero projection onto the given subspace,
/// - `q2`: has partial projection onto the subspace,
/// - `q3`: has a full projection onto the subspace,
///
/// then `axes_not_in_subspace` will be `{0}`, where 0 is the index of
/// the column of the `column_vector_space` which has zero projection
/// onto the given subspace.
///
/// Similarly, `axes_in_subspace` will be `{2}`, and
/// `axes_mixed_with_subspace` will be `{1}`. If any of the columns of
/// the given column_vector_space has a partial projection onto the
/// subspace, then `are_axes_mixed_with_subspace` will be `true`.
/// Otherwise it will be `false`.
struct VectorSpaceMixingInfo {
  VectorSpaceMixingInfo(Eigen::MatrixXd const &column_vector_space,
                        Eigen::MatrixXd const &subspace, double tol);
  std::vector<Index> axes_not_in_subspace;
  std::vector<Index> axes_in_subspace;
  std::vector<Index> axes_mixed_with_subspace;
  bool are_axes_mixed_with_subspace = true;
};

/// \brief Return DoF values as a unrolled coordinate in the prim basis
Eigen::VectorXd get_dof_vector_value(
    ConfigDoFValues const &dof_values,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    DoFSpace const &dof_space);

/// Return `config` DoF value as a coordinate in the DoFSpace basis
Eigen::VectorXd get_normal_coordinate(
    ConfigDoFValues const &dof_values,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    DoFSpace const &dof_space);

/// \brief Return DoF values as a unrolled coordinate in the prim basis for
///     the subset of the configuration located at a particular coordinate
Eigen::VectorXd get_dof_vector_value_at(
    ConfigDoFValues const &dof_values, DoFSpace const &dof_space,
    DoFSpaceIndexConverter const &index_converter,
    xtal::UnitCell integral_lattice_coordinate);

/// \brief Return DoF value in the DoFSpace basis of the subset of the
/// configuration located at a particular coordinate
Eigen::VectorXd get_normal_coordinate_at(
    ConfigDoFValues const &dof_values, DoFSpace const &dof_space,
    DoFSpaceIndexConverter const &index_converter,
    xtal::UnitCell integral_lattice_coordinate);

/// \brief Return mean DoF value of configuration as a unrolled coordinate in
///     the prim basis
Eigen::VectorXd get_mean_dof_vector_value(
    ConfigDoFValues const &dof_values,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    DoFSpace const &dof_space);

/// \brief Return mean DoF value of configuration in the DoFSpace basis
Eigen::VectorXd get_mean_normal_coordinate(
    ConfigDoFValues const &dof_values,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    DoFSpace const &dof_space);

/// \brief Set DoF values from a coordinate in the DoFSpace basis
///     (continuous DoF only)
void set_dof_value(ConfigDoFValues &dof_values,
                   Eigen::Matrix3l const &transformation_matrix_to_super,
                   DoFSpace const &dof_space,
                   Eigen::VectorXd const &dof_space_coordinate);

}  // namespace clexulator
}  // namespace CASM

#endif
