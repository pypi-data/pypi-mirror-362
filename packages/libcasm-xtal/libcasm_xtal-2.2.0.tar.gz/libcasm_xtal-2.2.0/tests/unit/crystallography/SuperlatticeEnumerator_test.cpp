#include <filesystem>

#include "Common.hh"
#include "autotools.hh"
#include "gtest/gtest.h"

/// What is being tested:
#include "casm/crystallography/Lattice.hh"

/// What is being used to test it:
#include "casm/casm_io/container/json_io.hh"
#include "casm/casm_io/json/jsonParser.hh"
#include "casm/crystallography/BasicStructure.hh"
#include "casm/crystallography/BasicStructureTools.hh"
#include "casm/crystallography/CanonicalForm.hh"
#include "casm/crystallography/Niggli.hh"
#include "casm/crystallography/SuperlatticeEnumerator.hh"
#include "casm/crystallography/SymTools.hh"
#include "casm/crystallography/SymType.hh"
#include "casm/crystallography/io/BasicStructureIO.hh"
#include "casm/external/Eigen/Dense"
#include "casm/misc/CASM_Eigen_math.hh"

using namespace CASM;
using xtal::BasicStructure;
using xtal::Lattice;
using xtal::ScelEnumProps;
using xtal::SuperlatticeEnumerator;

std::filesystem::path testdir(test::data_dir("crystallography"));

void autofail() {
  EXPECT_EQ(1, 0);
  return;
}

jsonParser mat_test_case(const std::string &pos_filename, int minvol,
                         int maxvol) {
  const BasicStructure test_struc = read_prim(testdir / pos_filename, TOL);
  const Lattice test_lat = test_struc.lattice();
  std::vector<xtal::SymOp> effective_pg = xtal::make_factor_group(test_struc);

  std::vector<Eigen::Matrix3i> enumerated_mats;

  ScelEnumProps enum_props(minvol, maxvol + 1);
  SuperlatticeEnumerator test_enumerator(test_lat, effective_pg, enum_props);

  double tol = TOL;
  for (auto it = test_enumerator.begin(); it != test_enumerator.end(); ++it) {
    enumerated_mats.push_back(it.matrix());

    // -- check niggli generation

    Lattice niggli1 = niggli(*it, tol);
    Lattice niggli2 = niggli(niggli1, tol);
    bool check_niggli =
        almost_equal(niggli1.lat_column_mat(), niggli2.lat_column_mat(), tol);

    EXPECT_EQ(check_niggli, true);

    // -- check canonical generation

    Lattice canon = xtal::canonical::equivalent(*it, effective_pg, tol);
    Lattice canon2 = xtal::canonical::equivalent(canon, effective_pg, tol);
    bool check =
        almost_equal(canon.lat_column_mat(), canon2.lat_column_mat(), tol);

    EXPECT_EQ(check, true);
  }

  jsonParser mat_dump;
  mat_dump["input"]["min_vol"] = minvol;
  mat_dump["input"]["max_vol"] = maxvol;
  mat_dump["input"]["source"] = pos_filename;
  mat_dump["output"]["mats"] = enumerated_mats;

  return mat_dump;
}

void trans_enum_test() {
  Lattice testlat(Lattice::fcc());
  std::vector<xtal::SymOp> pg = xtal::make_point_group(testlat);

  // int dims = 3;
  Eigen::Matrix3i transmat;

  transmat << -1, 1, 1, 1, -1, 1, 1, 1, -1;

  Lattice bigunit = make_superlattice(testlat, transmat);

  ScelEnumProps enum_props(1, 5 + 1, "abc", transmat);
  SuperlatticeEnumerator enumerator(testlat, pg, enum_props);

  std::vector<Lattice> enumerated_lat(enumerator.begin(), enumerator.end());

  for (Index i = 0; i > enumerated_lat.size(); i++) {
    EXPECT_TRUE(xtal::is_superlattice(enumerated_lat[i], bigunit,
                                      enumerated_lat[i].tol())
                    .first);
  }

  return;
}

void restricted_test() {
  std::vector<Lattice> all_test_lats;
  all_test_lats.push_back(Lattice::fcc());
  all_test_lats.push_back(Lattice::bcc());
  all_test_lats.push_back(Lattice::cubic());
  all_test_lats.push_back(Lattice::hexagonal());

  for (Index t = 0; t < all_test_lats.size(); t++) {
    Lattice testlat = all_test_lats[t];
    std::vector<xtal::SymOp> pg = xtal::make_point_group(testlat);

    // int dims = 1;

    ScelEnumProps enum_props(1, 15 + 1, "a");
    SuperlatticeEnumerator enumerator(testlat, pg, enum_props);

    int l = 1;
    for (auto it = enumerator.begin(); it != enumerator.end(); ++it) {
      Eigen::Matrix3i comp_transmat;
      comp_transmat << (l), 0, 0, 0, 1, 0, 0, 0, 1;

      EXPECT_TRUE(it.matrix() ==
                  canonical_hnf(pg.begin(), pg.end(), comp_transmat, testlat));
      l++;
    }
  }

  return;
}

TEST(SuperlatticeEnumeratorTest, RestrictedEnumeration) {
  trans_enum_test();
  restricted_test();
}
