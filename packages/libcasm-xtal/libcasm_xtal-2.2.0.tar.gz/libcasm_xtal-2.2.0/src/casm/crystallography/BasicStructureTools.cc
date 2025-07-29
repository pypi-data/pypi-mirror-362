#include "casm/crystallography/BasicStructureTools.hh"

#include <algorithm>
#include <atomic>
#include <tuple>
#include <unordered_set>
#include <utility>
#include <vector>

#include "casm/crystallography/BasicStructure.hh"
#include "casm/crystallography/Coordinate.hh"
#include "casm/crystallography/DoFSet.hh"
#include "casm/crystallography/IntegralCoordinateWithin.hh"
#include "casm/crystallography/Lattice.hh"
#include "casm/crystallography/Niggli.hh"
#include "casm/crystallography/OccupantDoFIsEquivalent.hh"
#include "casm/crystallography/Site.hh"
#include "casm/crystallography/Superlattice.hh"
#include "casm/crystallography/SuperlatticeEnumerator.hh"
#include "casm/crystallography/SymTools.hh"
#include "casm/crystallography/SymType.hh"
#include "casm/crystallography/SymTypeComparator.hh"
#include "casm/crystallography/UnitCellCoord.hh"
#include "casm/external/Eigen/Core"
#include "casm/external/Eigen/src/Core/Matrix.h"
#include "casm/external/Eigen/src/Core/PermutationMatrix.h"
#include "casm/external/Eigen/src/Core/util/Constants.h"
#include "casm/global/definitions.hh"
#include "casm/misc/CASM_Eigen_math.hh"
#include "casm/misc/UnaryCompare.hh"

namespace {
using namespace CASM;

/// Returns false if the given operation does not create an equivalent degree of
/// freedom. For example, a structure with only zz strain must have uniaxial
/// symmetry, but this won't be taken into account when generating the point
/// group of the lattice. This method is used to discard operations from the
/// factor group that aren't compatible with degrees of freedom that weren't
/// taken into account during its creation.
bool global_dofs_are_compatible_with_operation(
    const xtal::SymOp &operation,
    const std::map<DoFKey, xtal::DoFSet> &global_dof_map) {
  for (const auto &name_dof_pr : global_dof_map) {
    const xtal::DoFSet &dof = name_dof_pr.second;
    xtal::DoFSet transformed_dof = sym::copy_apply(operation, dof);
    if (!xtal::DoFSetIsEquivalent_f(dof, TOL)(transformed_dof)) {
      return false;
    }
  }
  return true;
}

/// Doubles the number of symmetry operations by multiplying each one with a
/// time reversal flip
void expand_with_time_reversal(xtal::SymOpVector *growing_point_group) {
  int size = growing_point_group->size();
  for (int ix = 0; ix < size; ++ix) {
    growing_point_group->emplace_back(growing_point_group->at(ix) *
                                      xtal::SymOp::time_reversal());
  }
  return;
}

/// Returns pair (success, drift). 'success' is true if translatable_basis +
/// translation can be permuted to map onto 'basis', to within distance 'tol'
/// (in Angstr.). 'drift' is vector from center of mass of 'translatable_basis'
/// to center of mass of 'basis'
std::pair<bool, xtal::Coordinate> map_translated_basis_and_calc_drift(
    const std::vector<xtal::Site> &basis,
    const std::vector<xtal::Site> &translatable_basis,
    const xtal::Coordinate &translation, double tol) {
  xtal::Coordinate drift = xtal::Coordinate::origin(translation.lattice());

  if (basis.size() != translatable_basis.size()) return {false, drift};

  for (const xtal::Site &s_tb : translatable_basis) {
    Index ix = xtal::find_index(basis, s_tb + translation, tol);
    if (ix >= basis.size())
      return {false, xtal::Coordinate::origin(translation.lattice())};
    // (basis[ix]-s_tb) is exact_translation for mapping pair, translation is
    // proposed translation translation.min_translation(exact_translation) is
    // vector FROM nearest periodic image of exact_translation TO proposed
    // translation. Average of this vector is CoM drift due to proposed
    // translation
    drift += translation.min_translation(basis[ix] - s_tb);
  }

  drift.cart() /= double(basis.size());
  return {true, drift};
}

/// Takes each translation from the SymOp and brings it within the lattice
void bring_within(std::vector<xtal::SymOp> *symmetry_group,
                  const xtal::Lattice &tiling_unit) {
  for (xtal::SymOp &operation : *symmetry_group) {
    xtal::Coordinate translation_coord(operation.translation, tiling_unit,
                                       CART);
    translation_coord.within();
    operation.translation = translation_coord.const_cart();
  }
  return;
}

/// Generates the factor group by applying every possible translation to the
/// provided point group, and checking if the structure maps onto itself. This
/// routine is slow for non primitive structures!
xtal::SymOpVector make_factor_group_from_point_group(
    const xtal::BasicStructure &struc, const xtal::SymOpVector &point_group,
    bool is_primitive, double tol) {
  if (struc.basis().size() == 0) {
    return point_group;
  }

  xtal::SymOpVector factor_group;
  Index i = 0;
  for (const xtal::SymOp &point_group_operation : point_group) {
    ++i;

    if (!::global_dofs_are_compatible_with_operation(point_group_operation,
                                                     struc.global_dofs())) {
      continue;
    }

    // apply the point group operation to tall the sites
    std::vector<xtal::Site> transformed_basis;
    for (const xtal::Site &s : struc.basis()) {
      transformed_basis.emplace_back(point_group_operation * s);
    }

    // Using the symmetrically transformed basis, find all possible
    // translations that MIGHT map the symmetrically transformed basis onto
    // the original basis
    const xtal::Site &reference_site = struc.basis()[0];
    for (const xtal::Site &transformed_site : transformed_basis) {
      // If the types don't match don't even bother with anything else
      if (!reference_site.compare_type(transformed_site)) {
        continue;
      }

      xtal::Coordinate translation = reference_site - transformed_site;
      translation.within();

      xtal::Coordinate drift(struc.lattice());
      bool success = false;
      // By construction, the current transformed_site matches the first
      // basis site, do the rest of them match too?
      // Determine if mapping is successful, and calculate center-of-mass drift
      std::tie(success, drift) = map_translated_basis_and_calc_drift(
          struc.basis(), transformed_basis, translation, tol);

      // The mapping failed, continue to the next site for a new translation
      if (!success) {
        continue;
      }

      // You found a valid translation! BUT, before you construct the
      // symmetry operation, remove some bias from the translation. We want
      // the average mapping error to be zero, but we arbitrarily
      // constructed the translation by taking the first basis site of the
      // structure as a reference. Here we use the average mapping error to
      // correct this.
      translation -= drift;

      // If components of the translation are very close to zero,
      // just set them to zero
      {
        Eigen::VectorXd translation_cart = translation.const_cart();
        for (int i = 0; i < 3; ++i) {
          if (CASM::almost_zero(translation_cart[i], tol * 1e-5)) {
            translation_cart[i] = 0.0;
          }
        }
        translation.cart() = translation_cart;
      }

      // Now that the translation has been adjusted, create the symmetry
      // operation and add it if we don't have an equivalent one already
      xtal::SymOp translation_operation =
          xtal::SymOp::translation_operation(translation.const_cart());
      xtal::SymOp new_factor_group_operation(translation_operation *
                                             point_group_operation);
      UnaryCompare_f<xtal::SymOpPeriodicCompare_f>
          equals_new_factor_group_operation(new_factor_group_operation,
                                            struc.lattice(), tol);

      if (std::find_if(factor_group.begin(), factor_group.end(),
                       equals_new_factor_group_operation) ==
          factor_group.end()) {
        factor_group.push_back(new_factor_group_operation);
      }

      if (is_primitive) {
        // If structure is primitive, there is no need to attempt other
        // translations
        break;
      }
    }
  }

  xtal::close_group<xtal::SymOpPeriodicCompare_f>(&factor_group,
                                                  struc.lattice(), tol);
  bring_within(&factor_group, struc.lattice());

  return factor_group;
}

xtal::SymOpVector make_translation_group(const xtal::BasicStructure &struc,
                                         double tol) {
  xtal::SymOpVector identity_group{xtal::SymOp::identity()};
  xtal::SymOpVector translation_group =
      make_factor_group_from_point_group(struc, identity_group, false, tol);
  return translation_group;
}

/// Given a structure, make it primitive and calculate its factor group. Return
/// the primitive structure and the factor group of the primitive structure
std::pair<xtal::BasicStructure, xtal::SymOpVector> make_primitive_factor_group(
    const xtal::BasicStructure &non_primitive_struc, double tol) {
  xtal::BasicStructure primitive_struc =
      xtal::make_primitive(non_primitive_struc, tol);

  xtal::SymOpVector primitive_point_group =
      xtal::make_point_group(primitive_struc.lattice());
  if (primitive_struc.is_time_reversal_active()) {
    // Duplicate each symmetry operation so that the second version has time
    // reversal enabled
    ::expand_with_time_reversal(&primitive_point_group);
  }

  xtal::SymOpVector primitive_factor_group =
      ::make_factor_group_from_point_group(primitive_struc,
                                           primitive_point_group, true, tol);
  return std::make_pair(primitive_struc, primitive_factor_group);
}

}  // namespace

namespace CASM {
namespace xtal {
Index find_index(const std::vector<Site> &basis, const Site &test_site,
                 double tol) {
  for (Index i = 0; i < basis.size(); i++) {
    if (basis[i].compare_type(test_site) &&
        basis[i].min_dist(test_site) < tol) {
      return i;
    }
  }
  return basis.size();
}

bool is_primitive(const BasicStructure &struc, double tol) {
  SymOpVector translation_group = ::make_translation_group(struc, tol);
  // For a primitive structure, the only possible translation is no translation
  return translation_group.size() == 1;
}

BasicStructure make_primitive(const BasicStructure &non_primitive_struc,
                              double tol) {
  if (non_primitive_struc.basis().size() == 0) {
    return non_primitive_struc;
  }
  SymOpVector translation_group =
      ::make_translation_group(non_primitive_struc, tol);
  double minimum_possible_volume =
      std::abs(0.5 * non_primitive_struc.lattice().volume() /
               non_primitive_struc.basis().size());

  // The candidate lattice vectors are the original lattice vectors, plus all
  // the possible translations that map the basis of the non primitive structure
  // onto itself
  std::vector<Eigen::Vector3d> possible_lattice_vectors{
      non_primitive_struc.lattice()[0], non_primitive_struc.lattice()[1],
      non_primitive_struc.lattice()[2]};

  for (const SymOp &trans_op : translation_group) {
    Coordinate debug(trans_op.translation, non_primitive_struc.lattice(), CART);
    possible_lattice_vectors.push_back(trans_op.translation);
  }

  // Attempt every combination of vectors, picking one that doesn't have
  // colinearity (minimum volume check), but results in the smallest lattice
  // possible (running lattice volume check)
  double minimum_volume = std::abs(2 * non_primitive_struc.lattice().volume());
  Eigen::Vector3d a_vector_primitive, b_vector_primitive, c_vector_primitive;
  for (Eigen::Vector3d const &a_vector_candidate : possible_lattice_vectors) {
    for (Eigen::Vector3d const &b_vector_candidate : possible_lattice_vectors) {
      for (Eigen::Vector3d const &c_vector_candidate :
           possible_lattice_vectors) {
        double possible_volume = std::abs(triple_product(
            a_vector_candidate, b_vector_candidate, c_vector_candidate));
        if (possible_volume < minimum_volume &&
            possible_volume > minimum_possible_volume) {
          minimum_volume = possible_volume;
          a_vector_primitive = a_vector_candidate;
          b_vector_primitive = b_vector_candidate;
          c_vector_primitive = c_vector_candidate;
        }
      }
    }
  }
  Lattice non_reduced_form_primitive_lattice(
      a_vector_primitive, b_vector_primitive, c_vector_primitive);
  Lattice primitive_lattice = niggli(non_reduced_form_primitive_lattice,
                                     non_primitive_struc.lattice().tol());

  // The primitive lattice could be noisy, so we smoothen it out to match an
  // integer transformation to the original lattice exactly
  Superlattice prim_to_original = Superlattice::smooth_prim(
      primitive_lattice, non_primitive_struc.lattice());
  primitive_lattice = prim_to_original.prim_lattice();

  // Fill up the basis
  BasicStructure primitive_struc(primitive_lattice);
  std::vector<std::vector<std::string>> _unique_names;
  Index i_site = 0;
  for (Site site_for_prim : non_primitive_struc.basis()) {
    site_for_prim.set_lattice(primitive_struc.lattice(), CART);
    if (find_index(primitive_struc.basis(), site_for_prim, tol) ==
        primitive_struc.basis().size()) {
      site_for_prim.within();
      primitive_struc.set_basis().emplace_back(std::move(site_for_prim));
      if (!non_primitive_struc.unique_names().empty()) {
        _unique_names.push_back(non_primitive_struc.unique_names()[i_site]);
      }
    }
    i_site++;
  }
  primitive_struc.set_unique_names(_unique_names);

  // TODO: Do we want this?
  primitive_struc.set_title(non_primitive_struc.title());
  return primitive_struc;
}

/// \brief Calculates the rotation angle and axis of a symmetry operation. This
/// function is almost exactly identical to the constructor of SymInfo::SymInfo
std::pair<double, Eigen::Vector3d> calc_rotation_angle_and_axis(
    const SymOp &op, const Lattice &lat) {
  auto matrix = op.matrix;
  double angle;
  Eigen::Vector3d rotation_axis, _axis;

  // Simplest case is identity: has no axis and no location
  if (almost_equal(matrix.trace(), 3.) || almost_equal(matrix.trace(), -3.)) {
    angle = 0;
    _axis = Eigen::Vector3d::Zero();
    rotation_axis = Coordinate(_axis, lat, CART).const_frac();
    return std::make_pair(angle, rotation_axis);
  }

  // det is -1 if improper and +1 if proper
  int det = round(matrix.determinant());

  // Find eigen decomposition of proper operation (by multiplying by
  // determinant)
  Eigen::EigenSolver<Eigen::Matrix3d> t_eig(det * matrix);

  // 'axis' is eigenvector whose eigenvalue is +1
  for (Index i = 0; i < 3; i++) {
    if (almost_equal(t_eig.eigenvalues()(i), std::complex<double>(1, 0))) {
      _axis = t_eig.eigenvectors().col(i).real();
      break;
    }
  }

  // Sign convention for 'axis': first non-zero element is positive
  for (Index i = 0; i < 3; i++) {
    if (!almost_zero(_axis[i])) {
      _axis *= float_sgn(_axis[i]);
      break;
    }
  }

  // get vector orthogonal to axis: ortho,
  // apply matrix: rot
  // and check angle between ortho and det*rot,
  // using determinant to get the correct angle for improper
  // (i.e. want angle before inversion for rotoinversion)
  Eigen::Vector3d ortho = _axis.unitOrthogonal();
  Eigen::Vector3d rot = det * (matrix * ortho);
  angle = fmod(
      (180. / M_PI) * atan2(_axis.dot(ortho.cross(rot)), ortho.dot(rot)) + 360.,
      360.);
  rotation_axis = Coordinate(_axis, lat, CART).const_frac();
  return std::make_pair(angle, rotation_axis);
}

/// \brief Generate key for sorting xtal::SymOp
///
/// Note:
/// - compare on vector of '-det', '-trace', 'angle', 'axis', 'tau'
symop_sort_key_type make_symop_sort_key(xtal::SymOp const &op,
                                        xtal::Lattice const &lat) {
  Eigen::Matrix<double, 10, 1> vec;
  int offset = 0;
  double sym_angle;
  Eigen::Vector3d sym_frac;
  std::tie(sym_angle, sym_frac) = calc_rotation_angle_and_axis(op, lat);

  vec[offset] = double(op.is_time_reversal_active);
  offset++;

  vec[offset] = -op.matrix.determinant();
  offset++;

  vec[offset] = -op.matrix.trace();
  offset++;

  vec[offset] = sym_angle;
  offset++;

  vec.segment<3>(offset) = sym_frac;
  offset += 3;

  vec.segment<3>(offset) = Coordinate(op.translation, lat, CART).const_frac();
  offset += 3;

  return vec;
}

SymOpSortKeyCompare::SymOpSortKeyCompare(double _tol) : tol(_tol) {}

bool SymOpSortKeyCompare::operator()(const symop_sort_key_type &A,
                                     const symop_sort_key_type &B) const {
  return float_lexicographical_compare(A, B, tol);
}

/// \brief Sort SymOp
///
/// SymOp are sorted by lexicographical comparison of: (-det, -trace, angle,
/// axis, tau)
/// - angle is positive
/// - axis[0] is positive
///
/// This function is an *not* an identical clone of CASM::SymGroup::sort(),
/// which sorts by conjugacy class.
void sort_factor_group(std::vector<SymOp> &factor_group, const Lattice &lat) {
  // floating point comparison tolerance
  double tol = TOL;

  // Just sorts elements - does not sort by class
  SymOpSortKeyCompare op_compare(tol);
  std::map<symop_sort_key_type, SymOp, SymOpSortKeyCompare> all_op(op_compare);
  for (auto const &op : factor_group) {
    all_op.emplace(make_symop_sort_key(op, lat), op);
  }

  // copy symop back into group
  int j = 0;
  for (auto const &pair : all_op) {
    factor_group[j] = pair.second;
    ++j;
  }
}

/// Create the factor group of the given structure
///
/// \param struct BasicStructure for which the factor group is constructed
///
/// \returns The sorted factor group
///
/// Notes:
/// - If the structure has no degrees of freedom affected by time reversal,
/// time reversal is ignored. Otherwise symmetry operations are checked for
/// time reversal
/// - For consistency, uses `struc.lattice().tol()` for comparing lattice
/// vectors and site coordinates.
std::vector<SymOp> make_factor_group(const BasicStructure &struc) {
  return make_factor_group(struc, struc.lattice().tol());
}

/// Create the factor group of the given structure. (deprecated)
///
/// \param struct BasicStructure for which the factor group is constructed
/// \param tol Crystallography tolerance used for comparing lattice vectors and
/// site coordinates. Should use `struc.lattice().tol()` for consistency.
///
/// \returns The sorted factor group
///
/// Notes:
/// - If the structure has no degrees of freedom affected by time reversal,
/// time reversal is ignored. Otherwise symmetry operations are checked for
/// time reversal
std::vector<SymOp> make_factor_group(const BasicStructure &struc, double tol) {
  auto prim_factor_group_pair = ::make_primitive_factor_group(struc, tol);
  const BasicStructure &primitive_struc = prim_factor_group_pair.first;
  const std::vector<SymOp> &primitive_factor_group =
      prim_factor_group_pair.second;

  auto all_lattice_points = make_lattice_points(
      primitive_struc.lattice(), struc.lattice(), struc.lattice().tol());

  std::vector<SymOp> point_group = make_point_group(struc.lattice());
  std::vector<SymOp> factor_group;

  for (const SymOp &prim_op : primitive_factor_group) {
    // If the primitive factor group operation with translations removed can't
    // map the original structure's lattice onto itself, then ditch that
    // operation.
    UnaryCompare_f<SymOpMatrixCompare_f> equals_prim_op_ignoring_trans(prim_op,
                                                                       tol);
    if (std::find_if(point_group.begin(), point_group.end(),
                     equals_prim_op_ignoring_trans) == point_group.end()) {
      continue;
    }

    // Otherwise take that factor operation, and expand it by adding additional
    // translations within the structure
    for (const UnitCell &lattice_point : all_lattice_points) {
      xtal::Coordinate lattice_point_coordinate = make_superlattice_coordinate(
          lattice_point, primitive_struc.lattice(), struc.lattice());
      factor_group.emplace_back(
          SymOp::translation_operation(lattice_point_coordinate.cart()) *
          prim_op);
    }
  }
  sort_factor_group(factor_group, struc.lattice());
  return factor_group;
}

/// Construct the crystal point group from the sorted factor group
///
/// \param sorted_factor_group A factor group. Must be sorted, as returned by
/// make_factor_group, or done by sort_factor_group.
/// \param tol Tolerance used for comparing SymOp matrices.
///
std::vector<SymOp> make_crystal_point_group(
    std::vector<SymOp> const &sorted_factor_group, double tol) {
  SymOpVector point_group;
  point_group.push_back(SymOp::identity());
  for (SymOp const &op : sorted_factor_group) {
    if (!almost_equal(get_matrix(op), get_matrix(point_group.back()), tol) ||
        get_time_reversal(op) != get_time_reversal(point_group.back())) {
      point_group.push_back(op);
      point_group.back().translation.setZero();
    }
  }
  return point_group;
}

/// Get the internal translations from the sorted factor group
///
/// Returns internal translations that map the parent crystal onto itself. Must
/// contain at least (0,0,0).
///
/// \param factor_group A factor group, as returned by make_factor_group.
/// \param tol Tolerance used for comparing SymOp matrices.
///
std::vector<Eigen::Vector3d> make_internal_translations(
    std::vector<SymOp> const &factor_group, double tol) {
  std::vector<Eigen::Vector3d> internal_translations;

  for (SymOp const &op : factor_group) {
    if (get_matrix(op).isIdentity(tol) && !get_time_reversal(op)) {
      internal_translations.push_back(get_translation(op));
    }
  }

  return internal_translations;
}

/// Create the permutation group of a structure.
///
/// The permutation group can be used to identify how the basis of a
/// structure is transformed under the application of a symmetry operation. The
/// permutation representation for a structure is obtained by applying each
/// factor group operation to the structure and identifying the index of the
/// symmetry transformed site.
///
/// \param struc The input structure
/// \param factor_group The factor group of `struc`, such as generated with
///     `xtal::make_factor_group(struc)`.
///
/// \return The permutation matrix at index `idx` corresponds to the effect of
/// the symmetry operation in `factor_group[idx]` on the basis.
///
/// The Eigen::PermutationMatrix value is stored in a vector of `indices()`:
/// - values_after = values_before * permutation_matrix;
/// - values_after[permutation_matrix.indices()[i]] = values_before[i]
///
std::vector<Eigen::PermutationMatrix<Eigen::Dynamic, Eigen::Dynamic, Index>>
make_permutation_representation(const xtal::BasicStructure &struc,
                                const std::vector<SymOp> &factor_group) {
  std::string clr(100, ' ');
  if (factor_group.size() <= 0) {
    std::cout << "ERROR in xtal::make_permutation_representation" << std::endl;
    std::cout << "Factor group is empty." << std::endl;
    exit(1);
  }
  std::vector<xtal::UnitCellCoord> sitemap;

  Eigen::PermutationMatrix<Eigen::Dynamic, Eigen::Dynamic, Index> init_perm_mat;
  init_perm_mat.setIdentity(struc.basis().size());
  std::vector<Eigen::PermutationMatrix<Eigen::Dynamic, Eigen::Dynamic, Index>>
      perm_rep(factor_group.size(), init_perm_mat);

  for (Index s = 0; s < factor_group.size(); ++s) {
    auto const &op = factor_group[s];
    std::vector<Index> _perm(struc.basis().size(), -1);
    sitemap = xtal::symop_site_map(op, struc);

    for (Index b = 0; b < struc.basis().size(); ++b) {
      auto const &dofref_to =
          struc.basis()[sitemap[b].sublattice()].occupant_dof();
      auto const &dofref_from = struc.basis()[b].occupant_dof();
      OccupantDoFIsEquivalent eq(dofref_from);
      // adapter::Adapter<SymOp, CASM::SymOp>()(op)
      if (eq(op, dofref_to)) {
        _perm[b] = sitemap[b].sublattice();
      } else
        throw std::runtime_error(
            "In Structure::_generate_basis_symreps(), Sites originally "
            "identified as equivalent cannot be mapped by symmetry.");
    }
    Eigen::Map<Eigen::Matrix<Index, Eigen::Dynamic, 1>> index_matrix(
        _perm.data(), _perm.size());
    perm_rep[s].indices() = index_matrix;
  }
  return perm_rep;
}

/// Return indices of equivalent basis sites
///
/// \param struc Input structure
/// \param factor_group Symmetry operations of the input structure.
///
/// \returns One `std::set<Index>` for each orbit of equivalent basis sites.
///
/// Note:
/// - This function assumes the operations in `factor_group` do in fact map
///   sites onto equivalents sites and does not double-check site equivalence.
std::set<std::set<Index>> make_asymmetric_unit(
    const xtal::BasicStructure &struc, const std::vector<SymOp> &factor_group) {
  double tol = struc.lattice().tol();

  auto transformed_site_index = [&](Site const &site, SymOp const &op) {
    Site transformed_site = op * site;
    return UnitCellCoord::from_coordinate(struc, transformed_site, tol)
        .sublattice();
  };

  std::set<std::set<Index>> asym_unit;
  for (Site const &site : struc.basis()) {
    std::set<Index> equivalent_sites;
    for (SymOp const &op : factor_group) {
      equivalent_sites.insert(transformed_site_index(site, op));
    }
    asym_unit.insert(equivalent_sites);
  }
  return asym_unit;
}

/// Return indices of equivalent basis sites
///
/// Equivalent to:
/// \code
/// std::vector<SymOp> factor_group = make_factor_group(struc,
///                                                     struc.lattice().tol());
/// return make_asymmetric_unit(struc, factor_group);
/// \endcode
std::set<std::set<Index>> make_asymmetric_unit(
    const xtal::BasicStructure &struc) {
  std::vector<SymOp> factor_group =
      make_factor_group(struc, struc.lattice().tol());
  return make_asymmetric_unit(struc, factor_group);
}

BasicStructure symmetrize(const BasicStructure &structure,
                          const std::vector<SymOp> &enforced_group) {
  // All your sites need to be within
  auto symmetrized_structure = structure;

  // First make a copy of your current basis
  // This copy will eventually become the new average basis.
  auto avg_basis = structure.basis();

  // Loop through given symmetry group an fill a temporary "operated basis"
  decltype(avg_basis) operated_basis;

  // Loop through given symmetry group an fill a temporary "operated basis"
  for (const SymOp &enforce_group_operation : enforced_group) {
    operated_basis.clear();
    for (const auto &symmetrized_structure_site :
         symmetrized_structure.basis()) {
      operated_basis.push_back(enforce_group_operation *
                               symmetrized_structure_site);
    }

    // Now that you have a transformed basis, find the closest mapping of atoms
    // Then average the distance and add it to the average basis
    for (Index b = 0; b < symmetrized_structure.basis().size(); b++) {
      double smallest = 1000000;
      Coordinate bshift(symmetrized_structure.lattice());
      for (const auto &operated_basis_site : operated_basis) {
        double dist =
            operated_basis_site.min_dist(symmetrized_structure.basis()[b]);
        if (dist < smallest) {
          bshift = operated_basis_site.min_translation(
              symmetrized_structure.basis()[b]);
          smallest = dist;
        }
      }
      bshift.cart() *= (1.0 / enforced_group.size());
      avg_basis[b] += bshift;
    }
  }
  symmetrized_structure.set_basis(avg_basis);
  return symmetrized_structure;
}

template <typename IntegralType, int Options>
BasicStructure make_superstructure(
    const BasicStructure &tiling_unit,
    const Eigen::Matrix<IntegralType, 3, 3, Options> &transformation_matrix) {
  static_assert(std::is_integral<IntegralType>::value,
                "Transformation matrix must be integer matrix");
  Lattice superlat =
      make_superlattice(tiling_unit.lattice(), transformation_matrix);
  BasicStructure superstruc(superlat);

  std::vector<UnitCell> all_lattice_points =
      make_lattice_points(tiling_unit.lattice(), superlat, superlat.tol());

  std::vector<Site> superstruc_basis;
  for (const Site &unit_basis_site : tiling_unit.basis()) {
    for (const UnitCell &lattice_point : all_lattice_points) {
      Coordinate lattice_point_coordinate = make_superlattice_coordinate(
          lattice_point, tiling_unit.lattice(), superlat);
      superstruc_basis.emplace_back(unit_basis_site + lattice_point_coordinate);
    }
  }
  superstruc.set_basis(superstruc_basis, CART);
  return superstruc;
}

template BasicStructure make_superstructure<int, 0>(
    const BasicStructure &tiling_unit,
    const Eigen::Matrix<int, 3, 3, 0> &transformation_matrix);
template BasicStructure make_superstructure<long, 0>(
    const BasicStructure &tiling_unit,
    const Eigen::Matrix<long, 3, 3, 0> &transformation_matrix);

}  // namespace xtal
}  // namespace CASM
