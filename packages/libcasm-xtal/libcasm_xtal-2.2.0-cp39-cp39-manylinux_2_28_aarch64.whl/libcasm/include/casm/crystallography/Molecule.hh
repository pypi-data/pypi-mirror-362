#ifndef MOLECULE_HH
#define MOLECULE_HH

#include <array>
#include <iostream>
#include <string>
#include <vector>

#include "casm/container/Permutation.hh"
#include "casm/crystallography/Adapter.hh"
#include "casm/crystallography/SpeciesProperty.hh"
#include "casm/global/definitions.hh"
#include "casm/misc/Comparisons.hh"

namespace CASM {
namespace xtal {
class Molecule;

/** \defgroup Molecule
 *  \ingroup Crystallography
 *  \brief Relates to Molecule
 *  @{
 */

/// \brief An atomic species associated with a position in space
class AtomPosition {
 public:
  /// \brief Construct with x,y,z position coordinates and atom name
  AtomPosition(double _pos1, double _pos2, double _pos3,
               std::string const &_species);

  /// \brief Construct with vector position and atom name
  AtomPosition(Eigen::Ref<const Eigen::Vector3d> const &_pos,
               std::string const &_species);

  /// Const access of species name
  std::string const &name() const;

  /// \brief Const access of Cartesian position of atom
  Eigen::Vector3d const &cart() const;

  bool time_reversal_active() const;

  std::map<std::string, SpeciesProperty> const &properties() const;

  void set_properties(std::map<std::string, SpeciesProperty> _property);

  /// \brief Comparison with tolerance (max allowed distance between LHS and
  /// RHS, in Angstr.)
  bool identical(AtomPosition const &RHS, double _tol) const;

 private:
  /// Atomic species
  std::string m_species;

  /// Cartesian position; origin is centered at site
  Eigen::Vector3d m_position;

  std::map<std::string, SpeciesProperty> m_property_map;
};

bool compare_type(AtomPosition const &A, AtomPosition const &B, double tol);

/** \defgroup Molecule
 *  \ingroup Crystallography
 *  \brief Relates to Molecule
 *  @{
 */

/// \brief Class representing a Molecule
///
/// - A Molecule is a vector of AtomPosition, with a name
/// - Vacancies are represented as a single atom Molecule, with molecule name ==
/// atom name == "Va"
/// - "make_atom" makes a Molecule with a single atom, with molecule name same
/// as atom name
/// - "make_vacancy" makes a Molecule with a single atom, with molecule name ==
/// atom name == "Va"
///
class Molecule {
 public:
  /// \brief Return an atomic Molecule with specified name
  static Molecule make_atom(std::string const &atom_name);

  /// \brief Return an atomic Molecule with specified name
  static Molecule make_unknown();

  /// \brief Return a vacancy Molecule
  static Molecule make_vacancy();

  ///\brief Construct with designated name, a list of atoms, and whether
  /// molecule is chemically divisible
  Molecule(std::string const &_name, std::vector<AtomPosition> _atoms = {},
           bool _divisible = false);

  /// \brief Number of atoms contained Molecule
  Index size() const;

  ///\brief Designated name of Molecule (may be unrelated to constituent
  /// species)
  std::string const &name() const;

  ///\brief Const access of all contained AtomPositions
  std::vector<AtomPosition> const &atoms() const;

  ///\brief returns i'th atom position
  AtomPosition const &atom(Index i) const;

  ///\brief True if Molecule is atom with no other properties
  bool is_atomic() const;

  ///\brief True if Molecule represents vacancy
  bool is_vacancy() const;

  ///\brief True if Molecule contains properties that are affected by time
  /// reversal
  bool time_reversal_active() const;

  ///\brief Returns dictionary of all constituent properties of the Molecule
  /// Does not include properties associated with individual atoms
  std::map<std::string, SpeciesProperty> const &properties() const;

  ///\brief Set all constitutent properties of Molecule
  /// overwrites any existing properties
  void set_properties(std::map<std::string, SpeciesProperty> _property);

  ///\brief set all constituent atoms of Molecule
  /// overwrites any existing atoms
  void set_atoms(std::vector<AtomPosition> _atoms);

  /// \brief Check equality of two molecules, within specified tolerance.
  /// Compares atoms, irrespective of order, and properties (name is not
  /// checked)
  bool identical(Molecule const &RHS, double _tol) const;

  /// \brief Check equality of two molecules, within specified tolerance.
  /// Compares atoms, irrespective of order, and attributes (name is not
  /// checked) and sets permutation of atom positions if true
  bool identical(Molecule const &RHS, double _tol,
                 Permutation &atom_position_perm) const;

  /// \brief Returns true of molecule contains atom of specified name
  bool contains(std::string const &atom_name) const;

  bool is_divisible() const;

  bool is_indivisible() const;

 private:
  std::string m_name;
  std::vector<AtomPosition> m_atoms;
  bool m_divisible;

  std::map<std::string, SpeciesProperty> m_property_map;
};

bool operator==(Molecule const &A, Molecule const &B);

/// \brief A vacancy is any Specie/Molecule with (name == "VA" || name == "va"
/// || name == "Va")
bool is_vacancy(const std::string &name);

/// \brief Return true if Molecule name matches 'name', including Va checks
bool is_molecule_name(const Molecule &mol, std::string name);

// --- Inline definitions ---

/// \brief Construct with x,y,z position coordinates and atom name
inline AtomPosition::AtomPosition(double _pos1, double _pos2, double _pos3,
                                  std::string const &_species)
    : m_species(_species), m_position(_pos1, _pos2, _pos3) {}

/// \brief Construct with vector position and atom name
inline AtomPosition::AtomPosition(Eigen::Ref<const Eigen::Vector3d> const &_pos,
                                  std::string const &_species)
    : m_species(_species), m_position(_pos) {}

/// Const access of species name
inline std::string const &AtomPosition::name() const { return m_species; }

/// \brief Const access of Cartesian position of atom
inline Eigen::Vector3d const &AtomPosition::cart() const { return m_position; }

inline bool AtomPosition::time_reversal_active() const {
  for (auto const &_property : properties()) {
    if (_property.second.traits().time_reversal_active()) return true;
  }
  return false;
}

inline std::map<std::string, SpeciesProperty> const &AtomPosition::properties()
    const {
  return m_property_map;
}

inline void AtomPosition::set_properties(
    std::map<std::string, SpeciesProperty> _property) {
  m_property_map = std::move(_property);
}

inline Molecule Molecule::make_atom(std::string const &atom_name) {
  return Molecule(atom_name, {AtomPosition(0., 0., 0., atom_name)});
}

/// \brief Return an atomic Molecule with specified name
inline Molecule Molecule::make_unknown() { return make_atom("UNKNOWN"); }

inline Molecule Molecule::make_vacancy() {
  // return Molecule("Va", {});
  return make_atom("Va");
}

///\brief Construct with designated name, a list of atoms, and whether
/// molecule is chemically divisible
inline Molecule::Molecule(std::string const &_name,
                          std::vector<AtomPosition> _atoms, bool _divisible)
    : m_name(_name), m_atoms(std::move(_atoms)), m_divisible(_divisible) {
  if (m_atoms.empty()) m_atoms.emplace_back(0., 0., 0., m_name);
}

/// \brief Number of atoms contained Molecule
inline Index Molecule::size() const { return m_atoms.size(); }

///\brief Designated name of Molecule (may be unrelated to constituent
/// species)
inline std::string const &Molecule::name() const { return m_name; }

///\brief Const access of all contained AtomPositions
inline std::vector<AtomPosition> const &Molecule::atoms() const {
  return m_atoms;
}

///\brief returns i'th atom position
inline AtomPosition const &Molecule::atom(Index i) const { return m_atoms[i]; }

///\brief True if Molecule contains properties that are affected by time
/// reversal
inline bool Molecule::time_reversal_active() const {
  for (auto const &_atom : atoms()) {
    if (_atom.time_reversal_active()) return true;
  }
  for (auto const &_property : properties()) {
    if (_property.second.traits().time_reversal_active()) return true;
  }
  return false;
}

///\brief Returns dictionary of all constituent properties of the Molecule
/// Does not include properties associated with individual atoms
inline std::map<std::string, SpeciesProperty> const &Molecule::properties()
    const {
  return m_property_map;
}

///\brief Set all constitutent properties of Molecule
/// overwrites any existing properties
inline void Molecule::set_properties(
    std::map<std::string, SpeciesProperty> _property) {
  m_property_map = std::move(_property);
}

///\brief set all constituent atoms of Molecule
/// overwrites any existing atoms
inline void Molecule::set_atoms(std::vector<AtomPosition> _atoms) {
  m_atoms = std::move(_atoms);
  if (m_atoms.empty()) {
    throw std::runtime_error(
        "Error in Molecule::set_atoms: atoms is not allowed to be set to "
        "empty");
  }
}

inline bool Molecule::is_divisible() const { return m_divisible; }

inline bool Molecule::is_indivisible() const { return !m_divisible; }

inline bool operator==(Molecule const &A, Molecule const &B) {
  return A.identical(B, TOL);
}

/// \brief A vacancy is any Specie/Molecule with (name == "VA" || name == "va"
/// || name == "Va")
inline bool is_vacancy(const std::string &name) {
  return (name == "VA" || name == "va" || name == "Va");
}

/// \brief Return true if Molecule name matches 'name', including Va checks
inline bool is_molecule_name(const Molecule &mol, std::string name) {
  return mol.name() == name || (mol.is_vacancy() && is_vacancy(name));
}

/** @} */
}  // namespace xtal
}  // namespace CASM

namespace CASM {
namespace sym {
xtal::AtomPosition &apply(const xtal::SymOp &op,
                          xtal::AtomPosition &mutating_atom_pos);
xtal::AtomPosition copy_apply(const xtal::SymOp &op,
                              xtal::AtomPosition atom_pos);

template <typename ExternSymOp>
xtal::AtomPosition copy_apply(const ExternSymOp &op,
                              xtal::AtomPosition atom_pos) {
  return sym::copy_apply(adapter::Adapter<xtal::SymOp, ExternSymOp>()(op),
                         atom_pos);
}

xtal::Molecule &apply(const xtal::SymOp &op, xtal::Molecule &mutating_mol);
xtal::Molecule copy_apply(const xtal::SymOp &op, xtal::Molecule mol);

template <typename ExternSymOp>
xtal::Molecule copy_apply(const ExternSymOp &op, xtal::Molecule mol) {
  return sym::copy_apply(adapter::Adapter<xtal::SymOp, ExternSymOp>()(op), mol);
}
}  // namespace sym
}  // namespace CASM

#endif
