#ifndef CASM_monte_Conversions
#define CASM_monte_Conversions

#include <set>
#include <string>
#include <vector>

#include "casm/crystallography/LinearIndexConverter.hh"
#include "casm/global/definitions.hh"

namespace CASM {
namespace xtal {
class UnitCell;
class UnitCellCoord;
class Molecule;
}  // namespace xtal

namespace monte {

/// \brief Performs conversions between various coordinate and asymmetric unit
///     orbit representations.
///
/// Conventions:
/// - l: linear index into supercell sites (site_index into `supercell` sites)
/// - b: prim basis site index (sublattice_index into prim.basis())
/// - ijk: prim unit cell indices
/// - bijk: prim basis site index + unit cell indices
/// - unitl: ref config basis site index (site_index in supercell speficied by
///   `unit_transformation_matrix_to_super()`)
/// - asym: asymmetric unit orbit index (value is the same for all sites which
///   are symmetrically equivalent *and* have  occupants listed in the same
///   order)
/// - occ_index: Index into occupant list for a site (index into
///   prim.basis()[b].occupant_dof(), for some b or asym)
/// - species_index: Index into the molecule list for the prim (index into
///   vector returned from xtal::struc_molecule)
///
/// Notes:
/// - There is a distinct species_index for each orientation of a Molecule
/// - When using with CASMcode_configuration, species_index should be made
///   to match orientation_index by using `molecule_list_all_orientations`
///    for `species_list` constructor arg
class Conversions {
 public:
  /// \brief Constructor (uses asymmetric unit determined from prim factor
  ///     group)
  Conversions(xtal::BasicStructure const &prim,
              Eigen::Matrix3l const &transformation_matrix_to_super);

  /// \brief Constructor (user specified asymmetric unit with reduced symmetry)
  Conversions(xtal::BasicStructure const &prim,
              Eigen::Matrix3l const &transformation_matrix_to_super,
              std::vector<Index> const &b_to_asym);

  /// \brief Constructor (user specified asymmetric unit with reduced
  ///     translational symmetry)
  Conversions(xtal::BasicStructure const &prim,
              std::vector<xtal::Molecule> const &species_list,
              Eigen::Matrix3l const &transformation_matrix_to_super,
              Eigen::Matrix3l const &unit_transformation_matrix_to_super,
              std::vector<Index> const &unitl_to_asym);

  Eigen::Matrix3d lat_column_mat() const;

  Index l_size() const;
  Index l_to_b(Index l) const;
  xtal::UnitCell l_to_ijk(Index l) const;
  xtal::UnitCellCoord l_to_bijk(Index l) const;
  Index l_to_unitl(Index l) const;
  Index l_to_asym(Index l) const;
  Eigen::Vector3d l_to_cart(Index l) const;
  Eigen::Vector3d l_to_frac(Index l) const;
  Eigen::Vector3d l_to_basis_cart(Index l) const;
  Eigen::Vector3d l_to_basis_frac(Index l) const;

  Index bijk_to_l(xtal::UnitCellCoord const &bijk) const;
  Index bijk_to_unitl(xtal::UnitCellCoord const &bijk) const;
  Index bijk_to_asym(xtal::UnitCellCoord const &bijk) const;

  Index unitl_size() const;
  Index unitl_to_b(Index unitl) const;
  xtal::UnitCellCoord unitl_to_bijk(Index unitl) const;
  Index unitl_to_asym(Index unitl) const;

  Index asym_size() const;
  std::set<Index> const &asym_to_b(Index asym) const;
  std::set<Index> const &asym_to_unitl(Index asym) const;

  Eigen::Matrix3l const &unit_transformation_matrix_to_super() const;
  Eigen::Matrix3l const &transformation_matrix_to_super() const;

  xtal::UnitCellIndexConverter const &unitcell_index_converter() const;

  xtal::UnitCellCoordIndexConverter const &unit_index_converter() const;
  xtal::UnitCellCoordIndexConverter const &index_converter() const;

  Index occ_size(Index asym) const;
  Index species_index(Index asym, Index occ_index) const;
  Index occ_index(Index asym, Index species_index) const;
  bool species_allowed(Index asym, Index species_index) const;

  Index species_size() const;
  Index species_index(std::string species_name) const;
  std::vector<xtal::Molecule> const &species_list() const;
  xtal::Molecule const &species_to_mol(Index species_index) const;
  std::string const &species_name(Index species_index) const;
  Index components_size(Index species_index) const;

 private:
  Eigen::Matrix3d m_lat_column_mat;
  std::vector<Eigen::Vector3d> m_basis_cart;
  std::vector<Eigen::Vector3d> m_basis_frac;

  xtal::UnitCellIndexConverter m_unitcell_index_converter;

  Eigen::Matrix3l m_unit_transformation_matrix_to_super;
  xtal::UnitCellCoordIndexConverter m_unitl_and_bijk_converter;

  Eigen::Matrix3l m_transformation_matrix_to_super;
  xtal::UnitCellCoordIndexConverter m_l_and_bijk_converter;

  std::vector<xtal::Molecule> m_struc_mol;
  std::vector<std::string> m_struc_molname;

  Index m_Nasym;
  std::vector<Index> m_unitl_to_asym;
  std::vector<std::set<Index>> m_asym_to_unitl;
  std::vector<std::set<Index>> m_asym_to_b;

  /// m_occ_to_species[asym][occ_index] -> species_index
  std::vector<std::vector<Index>> m_occ_to_species;

  /// m_species_to_occ[asym][species_index] -> occ_index
  std::vector<std::vector<Index>> m_species_to_occ;
};

}  // namespace monte
}  // namespace CASM

#endif
