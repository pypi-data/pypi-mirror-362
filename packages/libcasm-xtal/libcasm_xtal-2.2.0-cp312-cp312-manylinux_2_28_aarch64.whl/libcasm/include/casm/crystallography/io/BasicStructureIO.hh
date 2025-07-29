#ifndef CASM_xtal_BasicStructure_io
#define CASM_xtal_BasicStructure_io

#include <filesystem>
#include <map>
#include <string>

#include "casm/global/definitions.hh"
#include "casm/global/eigen.hh"
#include "casm/global/enum.hh"

namespace CASM {
namespace xtal {
class Lattice;
class SpeciesProperty;
class AtomPosition;
class Molecule;
class Site;
class BasicStructure;
}  // namespace xtal

namespace fs = std::filesystem;

// --- These functions are for casm I/O -----------

class AnisoValTraits;
template <typename T>
class ParsingDictionary;
template <typename T>
struct jsonConstructor;
template <typename T>
struct jsonMake;
class jsonParser;

// --------- PrimIO Declarations
// --------------------------------------------------

/// \brief Read SpeciesProperty from json
jsonParser const &from_json(xtal::SpeciesProperty &_attr,
                            jsonParser const &json);

/// \brief From SpeciesProperty to json
jsonParser &to_json(xtal::SpeciesProperty const &_attr, jsonParser &json);

/// \brief Print AtomPosition to json after applying affine transformation
/// cart2frac*cart()+trans
jsonParser &to_json(const xtal::AtomPosition &apos, jsonParser &json,
                    Eigen::Ref<const Eigen::Matrix3d> const &cart2frac);

/// \brief Read AtomPosition from json and then apply affine transformation
/// cart2frac*cart()
void from_json(xtal::AtomPosition &apos, const jsonParser &json,
               Eigen::Ref<const Eigen::Matrix3d> const &frac2cart,
               ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);

template <>
struct jsonConstructor<xtal::AtomPosition> {
  /// \brief Read from json [b, i, j, k], using 'unit' for AtomPosition::unit()
  static xtal::AtomPosition from_json(
      const jsonParser &json, Eigen::Matrix3d const &f2c_mat,
      ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);
};

jsonParser &to_json(const xtal::Molecule &mol, jsonParser &json,
                    Eigen::Ref<const Eigen::Matrix3d> const &c2f_mat);

void from_json(xtal::Molecule &mol, const jsonParser &json,
               Eigen::Ref<const Eigen::Matrix3d> const &f2c_mat,
               ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);

template <>
struct jsonConstructor<xtal::Molecule> {
  static xtal::Molecule from_json(
      const jsonParser &json, Eigen::Ref<const Eigen::Matrix3d> const &f2c_mat,
      ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);
};

template <>
struct jsonConstructor<xtal::Site> {
  static xtal::Site from_json(
      const jsonParser &json, xtal::Lattice const &_home, COORD_TYPE coordtype,
      std::map<std::string, xtal::Molecule> const &mol_map,
      std::vector<std::vector<std::string>> &unique_names,
      ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);
};

jsonParser &to_json(const xtal::Site &value, jsonParser &json,
                    COORD_TYPE coordtype);

void from_json(xtal::Site &value, const jsonParser &json,
               xtal::Lattice const &_home, COORD_TYPE coordtype,
               std::map<std::string, xtal::Molecule> const &mol_map,
               std::vector<std::string> &site_unique_names,
               ParsingDictionary<AnisoValTraits> const &_aniso_val_dict);

xtal::BasicStructure read_prim(
    fs::path filename, double xtal_tol,
    ParsingDictionary<AnisoValTraits> const *_aniso_val_dict = nullptr);

xtal::BasicStructure read_prim(
    fs::path filename, double xtal_tol,
    ParsingDictionary<AnisoValTraits> const *_aniso_val_dict,
    std::string &prim_file_type);

xtal::BasicStructure read_prim(
    jsonParser const &json, double xtal_tol,
    ParsingDictionary<AnisoValTraits> const *_aniso_val_dict = nullptr);

/// \brief Write prim.json to file
void write_prim(const xtal::BasicStructure &prim, fs::path filename,
                COORD_TYPE mode, bool include_va = false);

/// \brief Write prim.json as JSON
void write_prim(const xtal::BasicStructure &prim, jsonParser &json,
                COORD_TYPE mode, bool include_va = false);

template <>
struct jsonConstructor<xtal::BasicStructure> {
  static xtal::BasicStructure from_json(
      jsonParser const &json, double xtal_tol,
      ParsingDictionary<AnisoValTraits> const *_aniso_val_dict = nullptr);
};

template <>
struct jsonMake<xtal::BasicStructure> {
  static std::unique_ptr<xtal::BasicStructure> make_from_json(
      jsonParser const &json, double xtal_tol,
      ParsingDictionary<AnisoValTraits> const *_aniso_val_dict = nullptr);
};

void from_json(
    xtal::BasicStructure &prim, jsonParser const &json, double xtal_tol,
    ParsingDictionary<AnisoValTraits> const *_aniso_val_dict = nullptr);

jsonParser &to_json(const xtal::BasicStructure &prim, jsonParser &json,
                    COORD_TYPE mode, bool include_va = false);

}  // namespace CASM

#endif
