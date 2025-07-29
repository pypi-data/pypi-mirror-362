#include "casm/crystallography/BasicStructure.hh"

#include <fstream>
#include <iomanip>
#include <stdexcept>

#include "casm/crystallography/Adapter.hh"
#include "casm/crystallography/IntegralCoordinateWithin.hh"
#include "casm/crystallography/Molecule.hh"
#include "casm/crystallography/Niggli.hh"
#include "casm/crystallography/SimpleStructureTools.hh"
#include "casm/crystallography/Site.hh"
#include "casm/crystallography/UnitCellCoord.hh"
#include "casm/crystallography/io/VaspIO.hh"
#include "casm/misc/algorithm.hh"

namespace CASM {
namespace xtal {
BasicStructure BasicStructure::from_poscar_stream(std::istream &poscar_stream,
                                                  double tol) {
  BasicStructure poscar_structure;
  poscar_structure.read(poscar_stream, tol);
  poscar_structure.set_unique_names(
      allowed_molecule_unique_names(poscar_structure));
  return poscar_structure;
}

//***********************************************************

BasicStructure::BasicStructure(const BasicStructure &RHS)
    : m_lattice(RHS.lattice()),
      m_title(RHS.title()),
      m_basis(RHS.basis()),
      m_global_dof_map(RHS.m_global_dof_map),
      m_unique_names(RHS.m_unique_names) {
  for (Index i = 0; i < basis().size(); i++) {
    m_basis[i].set_lattice(lattice(), CART);
  }
}

//***********************************************************

BasicStructure &BasicStructure::operator=(const BasicStructure &RHS) {
  m_lattice = RHS.lattice();
  m_title = RHS.title();
  set_basis(RHS.basis());
  m_global_dof_map = RHS.m_global_dof_map;
  m_unique_names = RHS.m_unique_names;

  for (Index i = 0; i < basis().size(); i++)
    m_basis[i].set_lattice(lattice(), CART);

  return *this;
}

//************************************************************

DoFSet const &BasicStructure::global_dof(std::string const &_dof_type) const {
  auto it = m_global_dof_map.find(_dof_type);
  if (it != m_global_dof_map.end()) {
    return (it->second);
  } else {
    throw std::runtime_error(
        std::string("In BasicStructure::dof(), this structure does not contain "
                    "any global DoF's of type " +
                    _dof_type));
  }
}

void BasicStructure::within() {
  for (Index i = 0; i < basis().size(); i++) {
    m_basis[i].within();
  }
  return;
}

//***********************************************************

void BasicStructure::set_lattice(const Lattice &new_lat, COORD_TYPE mode) {
  m_lattice = new_lat;

  for (Index nb = 0; nb < basis().size(); nb++) {
    m_basis[nb].set_lattice(lattice(), mode);
  }
}

//***********************************************************

void BasicStructure::set_title(std::string const &_title) { m_title = _title; }

//\Liz D 032514
//***********************************************************
/**
 * Allows for the basis elements of a basic structure to be
 * manually set, e.g. as in jsonParser.cc.
 */
//***********************************************************

void BasicStructure::set_basis(std::vector<Site> const &_basis,
                               COORD_TYPE mode) {
  m_basis.clear();
  m_basis.reserve(_basis.size());
  for (Site const &site : _basis) push_back(site, mode);
}

void BasicStructure::push_back(Site const &_site, COORD_TYPE mode) {
  m_basis.push_back(_site);
  m_basis.back().set_lattice(lattice(), mode);
}

/// Set the names used to distinguish occupants with the same chemical name
void BasicStructure::set_unique_names(
    std::vector<std::vector<std::string>> const &_unique_names) {
  m_unique_names = _unique_names;
}

/// Get the unique names
std::vector<std::vector<std::string>> const &BasicStructure::unique_names()
    const {
  return m_unique_names;
}

//************************************************************
/// Counts sites that allow vacancies
Index BasicStructure::max_possible_vacancies() const {
  Index result(0);
  for (Index i = 0; i < basis().size(); i++) {
    if (m_basis[i].contains("Va")) ++result;
  }
  return result;
}

//************************************************************
// read a POSCAR like file and collect all the structure variables
// modified to read PRIM file and determine which basis to use
// Changed by Ivy to read new VASP POSCAR format

void BasicStructure::read(std::istream &stream, double tol) {
  int i, t_int;
  char ch;
  std::vector<double> num_elem;
  std::vector<std::string> elem_array;
  bool read_elem = false;
  std::string tstr;
  std::stringstream tstrstream;

  Site tsite(lattice());

  bool SD_flag = false;
  getline(stream, m_title);
  if (title().back() == '\r')
    throw std::runtime_error(std::string(
        "Structure file is formatted for DOS. Please convert to Unix format. "
        "(This can be done with the dos2unix command.)"));

  m_lattice.read(stream);
  m_lattice.set_tol(tol);

  stream.ignore(100, '\n');

  // Search for Element Names
  ch = stream.peek();
  while (ch != '\n' && !stream.eof()) {
    if (isalpha(ch)) {
      read_elem = true;
      stream >> tstr;
      elem_array.push_back(tstr);
      ch = stream.peek();
    } else if (ch == ' ' || ch == '\t') {
      stream.ignore();
      ch = stream.peek();
    } else if (ch >= '0' && ch <= '9') {
      break;
    } else {
      throw std::runtime_error(std::string(
          "Error attempting to read Structure. Error reading atom names."));
    }
  }

  if (read_elem == true) {
    stream.ignore(10, '\n');
    ch = stream.peek();
  }

  // Figure out how many species
  int num_sites = 0;
  while (ch != '\n' && !stream.eof()) {
    if (ch >= '0' && ch <= '9') {
      stream >> t_int;
      num_elem.push_back(t_int);
      num_sites += t_int;
      ch = stream.peek();
    } else if (ch == ' ' || ch == '\t') {
      stream.ignore();
      ch = stream.peek();
    } else {
      throw std::runtime_error(std::string(
          "Error in line 6 of structure input file. Line 6 of structure input "
          "file should contain the number of sites."));
    }
  }
  stream.get(ch);

  // fractional coordinates or cartesian
  COORD_MODE input_mode(FRAC);

  stream.get(ch);
  while (ch == ' ' || ch == '\t') {
    stream.get(ch);
  }

  if (ch == 'S' || ch == 's') {
    SD_flag = true;
    stream.ignore(1000, '\n');
    stream.get(ch);
    while (ch == ' ' || ch == '\t') {
      stream.get(ch);
    }
  }

  if (ch == 'D' || ch == 'd') {
    input_mode.set(FRAC);
  } else if (ch == 'C' || ch == 'c') {
    input_mode.set(CART);
  } else if (!SD_flag) {
    throw std::runtime_error(std::string(
        "Error in line 7 of structure input file. Line 7 of structure input "
        "file should specify Direct, Cartesian, or Selective Dynamics."));
  } else if (SD_flag) {
    throw std::runtime_error(
        std::string("Error in line 8 of structure input file. Line 8 of "
                    "structure input file should specify Direct or Cartesian "
                    "when Selective Dynamics is on."));
  }

  stream.ignore(1000, '\n');
  // Clear basis if it is not empty
  if (basis().size() != 0) {
    std::cerr << "The structure is going to be overwritten." << std::endl;
    m_basis.clear();
  }

  if (read_elem) {
    int j = -1;
    int sum_elem = 0;
    m_basis.reserve(num_sites);
    for (i = 0; i < num_sites; i++) {
      if (i == sum_elem) {
        j++;
        sum_elem += num_elem[j];
      }

      tsite.read(stream, elem_array[j], SD_flag);
      push_back(tsite);
    }
  } else {
    // read the site info
    m_basis.reserve(num_sites);
    for (i = 0; i < num_sites; i++) {
      tsite.read(stream, SD_flag);
      if ((stream.rdstate() & std::ifstream::failbit) != 0) {
        std::cerr << "Error reading site " << i + 1
                  << " from structure input file." << std::endl;
        exit(1);
      }
      push_back(tsite);
    }
  }

  // Check whether there are additional sites listed in the input file
  std::string s;
  getline(stream, s);
  std::istringstream tmp_stream(s);
  Eigen::Vector3d coord;
  tmp_stream >> coord;
  if (tmp_stream.good()) {
    throw std::runtime_error(
        std::string("ERROR: too many sites listed in structure input file."));
  }

  return;
}

//***********************************************************

void BasicStructure::print_xyz(std::ostream &stream, bool frac) const {
  stream << basis().size() << '\n';
  stream << title() << '\n';
  stream.precision(7);
  stream.width(11);
  stream.flags(std::ios::showpoint | std::ios::fixed | std::ios::right);
  stream << "      a       b       c" << '\n';
  stream << lattice().lat_column_mat() << '\n';
  for (Index i = 0; i < basis().size(); i++) {
    std::string site_label = basis()[i].allowed_occupants().size() == 1
                                 ? basis()[i].allowed_occupants()[0]
                                 : "?";
    stream << std::setw(2) << site_label << " ";
    if (frac) {
      stream << std::setw(12) << basis()[i].frac().transpose() << '\n';
    } else {
      stream << std::setw(12) << basis()[i].cart() << '\n';
    }
  }
}

//***********************************************************

BasicStructure &BasicStructure::operator+=(const Coordinate &shift) {
  for (Index i = 0; i < basis().size(); i++) {
    m_basis[i] += shift;
  }

  return (*this);
}

//***********************************************************

BasicStructure &BasicStructure::operator-=(const Coordinate &shift) {
  for (Index i = 0; i < basis().size(); i++) {
    m_basis[i] -= shift;
  }
  // factor_group -= shift;
  // asym_unit -= shift;
  return (*this);
}

//***********************************************************

/* BasicStructure operator*(const Lattice &LHS, const BasicStructure &RHS) { */
/*   BasicStructure tsuper(LHS); */
/*   tsuper.fill_supercell(RHS); */
/*   return tsuper; */
/* } */

//***********************************************************

/// \brief Returns true if structure has DoF or properties affected by time
/// reversal private for now, expose if necessary
bool BasicStructure::is_time_reversal_active() const {
  for (auto const &dof : m_global_dof_map)
    if (dof.second.traits().time_reversal_active()) return true;
  for (Site const &site : basis())
    if (site.time_reversal_active()) return true;
  return false;
}

//***********************************************************

/// To which site a SymOp transforms each basis site
///
/// The resulting value satisifies, for all b:
/// \code
/// double _tol = _struc.lattice().tol();
/// result[b] == UnitCellCoord::from_coordinate(_op * _struc.basis()[b], _tol)
/// \endcode
std::vector<UnitCellCoord> symop_site_map(SymOp const &_op,
                                          BasicStructure const &_struc) {
  return symop_site_map(_op, _struc, _struc.lattice().tol());
}

//***********************************************************

/// To which site a SymOp transforms each basis site
///
/// The resulting value satisifies, for all b:
/// \code
/// result[b] == UnitCellCoord::from_coordinate(_op * _struc.basis()[b], _tol)
/// \endcode
std::vector<UnitCellCoord> symop_site_map(SymOp const &_op,
                                          BasicStructure const &_struc,
                                          double _tol) {
  std::vector<UnitCellCoord> result;
  // Determine how basis sites transform from the origin unit cell
  for (int b = 0; b < _struc.basis().size(); b++) {
    Site transformed_basis_site = _op * _struc.basis()[b];
    result.emplace_back(
        UnitCellCoord::from_coordinate(_struc, transformed_basis_site, _tol));
  }
  return result;
}

//************************************************************

/// Returns an std::vector of each *possible* Specie in this Structure
std::vector<std::string> struc_species(BasicStructure const &_struc) {
  std::vector<Molecule> tstruc_molecule = struc_molecule(_struc);
  std::set<std::string> result;

  Index i, j;

  // For each molecule type
  for (i = 0; i < tstruc_molecule.size(); i++) {
    // For each atomposition in the molecule
    for (j = 0; j < tstruc_molecule[i].size(); j++)
      result.insert(tstruc_molecule[i].atom(j).name());
  }

  return std::vector<std::string>(result.begin(), result.end());
}

//************************************************************

/// Returns an std::vector of each *possible* Molecule in this Structure
std::vector<Molecule> struc_molecule(BasicStructure const &_struc) {
  std::vector<Molecule> tstruc_molecule;
  Index i, j;

  // loop over all Sites in basis
  for (i = 0; i < _struc.basis().size(); i++) {
    // loop over all Molecules in Site
    for (j = 0; j < _struc.basis()[i].occupant_dof().size(); j++) {
      // Collect unique Molecules
      if (!contains(tstruc_molecule, _struc.basis()[i].occupant_dof()[j])) {
        tstruc_molecule.push_back(_struc.basis()[i].occupant_dof()[j]);
      }
    }
  }  // end loop over all Sites

  return tstruc_molecule;
}

//************************************************************
/// Returns an std::vector of each *possible* Molecule in this Structure
std::vector<std::string> struc_molecule_name(BasicStructure const &_struc) {
  // get Molecule allowed in struc
  std::vector<Molecule> struc_mol = struc_molecule(_struc);

  // store Molecule names in vector
  std::vector<std::string> struc_mol_name;
  for (int i = 0; i < struc_mol.size(); i++) {
    struc_mol_name.push_back(struc_mol[i].name());
  }

  return struc_mol_name;
}

//************************************************************
/// Returns an std::vector of each *possible* Molecule in this Structure
std::vector<std::vector<std::string>> allowed_molecule_unique_names(
    BasicStructure const &_struc) {
  // construct name_map
  std::map<std::string, std::vector<Molecule>> name_map;
  for (Index b = 0; b < _struc.basis().size(); ++b) {
    for (Index j = 0; j < _struc.basis()[b].occupant_dof().size(); ++j) {
      Molecule const &mol(_struc.basis()[b].occupant_dof()[j]);
      auto it = name_map.find(mol.name());
      if (it == name_map.end()) {
        name_map[mol.name()].push_back(mol);
      } else {
        Index i = find_index(it->second, mol);
        if (i == it->second.size()) {
          it->second.push_back(mol);
        }
      }
    }
  }

  // construct unique names
  std::vector<std::vector<std::string>> result(_struc.basis().size());
  for (Index b = 0; b < _struc.basis().size(); ++b) {
    for (Index j = 0; j < _struc.basis()[b].occupant_dof().size(); ++j) {
      Molecule const &mol(_struc.basis()[b].occupant_dof()[j]);
      result[b].push_back(mol.name());
      auto it = name_map.find(mol.name());
      if (it->second.size() > 1) {
        Index i = find_index(it->second, mol);
        result[b][j] += ("." + std::to_string(i + 1));
      }
    }
  }
  return result;
}

//************************************************************
/// Returns a vector with a list of allowed molecule names at each site
std::vector<std::vector<std::string>> allowed_molecule_names(
    BasicStructure const &_struc) {
  std::vector<std::vector<std::string>> result(_struc.basis().size());

  for (Index b = 0; b < _struc.basis().size(); ++b)
    result[b] = _struc.basis()[b].allowed_occupants();

  return result;
}

//****************************************************************************************************//

std::vector<DoFKey> all_local_dof_types(BasicStructure const &_struc) {
  std::set<std::string> tresult;

  for (Site const &site : _struc.basis()) {
    auto sitetypes = site.dof_types();
    tresult.insert(sitetypes.begin(), sitetypes.end());
    if (site.occupant_dof().size() > 1) {
      tresult.insert("occ");  // TODO: single source for occupation dof name
    }
  }
  return std::vector<std::string>(tresult.begin(), tresult.end());
}

std::vector<DoFKey> continuous_local_dof_types(BasicStructure const &_struc) {
  std::set<std::string> tresult;

  for (Site const &site : _struc.basis()) {
    auto sitetypes = site.dof_types();
    tresult.insert(sitetypes.begin(), sitetypes.end());
  }
  return std::vector<std::string>(tresult.begin(), tresult.end());
}

std::vector<DoFKey> global_dof_types(BasicStructure const &_struc) {
  std::vector<std::string> result;
  for (auto const &dof : _struc.global_dofs()) result.push_back(dof.first);
  return result;
}

std::vector<DoFKey> all_dof_types(BasicStructure const &_struc) {
  std::vector<std::string> result;
  for (auto const &global_dof_name : global_dof_types(_struc))
    result.push_back(global_dof_name);
  for (auto const &local_dof_name : all_local_dof_types(_struc))
    result.push_back(local_dof_name);
  return result;
}

std::map<DoFKey, Index> local_dof_dims(BasicStructure const &_struc) {
  std::map<DoFKey, Index> result;
  for (DoFKey const &type : continuous_local_dof_types(_struc))
    result[type] = local_dof_dim(type, _struc);

  return result;
}

std::map<DoFKey, Index> global_dof_dims(BasicStructure const &_struc) {
  std::map<DoFKey, Index> result;
  for (auto const &type : _struc.global_dofs())
    result[type.first] = type.second.dim();
  return result;
}

Index local_dof_dim(DoFKey const &_name, BasicStructure const &_struc) {
  Index result = 0;
  for (Site const &site : _struc.basis()) {
    if (site.has_dof(_name)) result = max(result, site.dof(_name).dim());
  }
  return result;
}

bool has_strain_dof(xtal::BasicStructure const &structure) {
  std::vector<DoFKey> global_dof_types = xtal::global_dof_types(structure);
  Index istrain = find_index_if(global_dof_types, [](DoFKey const &other) {
    return other.find("strain") != std::string::npos;
  });
  return istrain != global_dof_types.size();
}

DoFKey get_strain_dof_key(xtal::BasicStructure const &structure) {
  std::vector<DoFKey> global_dof_types = xtal::global_dof_types(structure);
  Index istrain = find_index_if(global_dof_types, [](DoFKey const &other) {
    return other.find("strain") != std::string::npos;
  });
  if (istrain == global_dof_types.size()) {
    throw std::runtime_error(
        "Error in get_strain_dof_key: Structure does not have strain DoF.");
  }
  return global_dof_types[istrain];
}

DoFKey get_strain_metric(DoFKey strain_dof_key) {
  auto pos = strain_dof_key.find("strain");
  if (pos != std::string::npos) {
    return strain_dof_key.substr(0, pos);
  }
  std::stringstream msg;
  msg << "Error in get_strain_metric: Failed to get metric name from '"
      << strain_dof_key << "'.";
  throw std::runtime_error(msg.str());
}

/// Returns 'converter' which converts Site::site_occupant indices to 'mol_list'
/// indices:
///   mol_list_index = converter[basis_site][site_occupant_index]
std::vector<std::vector<Index>> make_index_converter(
    const BasicStructure &struc, std::vector<xtal::Molecule> mol_list) {
  std::vector<std::vector<Index>> converter(struc.basis().size());

  for (Index i = 0; i < struc.basis().size(); i++) {
    converter[i].resize(struc.basis()[i].occupant_dof().size());

    for (Index j = 0; j < struc.basis()[i].occupant_dof().size(); j++) {
      converter[i][j] =
          CASM::find_index(mol_list, struc.basis()[i].occupant_dof()[j]);
    }
  }

  return converter;
}

/// Returns 'converter' which converts Site::site_occupant indices to
/// 'mol_name_list' indices:
///   mol_name_list_index = converter[basis_site][site_occupant_index]
std::vector<std::vector<Index>> make_index_converter(
    const BasicStructure &struc, std::vector<std::string> mol_name_list) {
  std::vector<std::vector<Index>> converter(struc.basis().size());

  for (Index i = 0; i < struc.basis().size(); i++) {
    converter[i].resize(struc.basis()[i].occupant_dof().size());

    for (Index j = 0; j < struc.basis()[i].occupant_dof().size(); j++) {
      converter[i][j] = CASM::find_index(
          mol_name_list, struc.basis()[i].occupant_dof()[j].name());
    }
  }

  return converter;
}

/// Returns 'converter_inverse' which converts 'mol_name_list' indices to
/// Site::site_occupant indices:
///  site_occupant_index = converter_inverse[basis_site][mol_name_list_index]
///
/// If mol is not allowed on basis_site, return
/// struc.basis()[basis_site].occupant_dof().size()
std::vector<std::vector<Index>> make_index_converter_inverse(
    const BasicStructure &struc, std::vector<std::string> mol_name_list) {
  std::vector<std::vector<Index>> converter_inv(struc.basis().size());

  for (Index i = 0; i < struc.basis().size(); i++) {
    converter_inv[i].resize(mol_name_list.size());

    std::vector<std::string> site_occ_name_list;
    for (Index j = 0; j < struc.basis()[i].occupant_dof().size(); j++) {
      site_occ_name_list.push_back(struc.basis()[i].occupant_dof()[j].name());
    }

    for (Index j = 0; j < mol_name_list.size(); j++) {
      converter_inv[i][j] =
          CASM::find_index(site_occ_name_list, mol_name_list[j]);
    }
  }

  return converter_inv;
}

}  // namespace xtal
}  // namespace CASM
