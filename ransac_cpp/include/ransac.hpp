////////////////////////////////////////////////////////////////////////////////
//
// Filename:      ransac.hpp
// Authors:       Yu-Han, Hsueh
//
//////////////////////////////// FILE INFO /////////////////////////////////////
//
// Ransac algorithm (curve-fitting)
//
/////////////////////////////////// LICENSE ////////////////////////////////////
//
// Copyright (C) 2020 Yu-Han, Hsueh <zero000.ece07g@nctu.edu.tw>
//
// This file is part of {ransac_cpp}.
//
//////////////////////////////////// NOTES /////////////////////////////////////
//
////////////////////////////////////////////////////////////////////////////////

#pragma once
#include <vector>
#include <Eigen/Geometry>

namespace ransac_cpp {
typedef Eigen::Vector2d Vector2;
typedef Eigen::Vector3d Vector3;

class Ransac {
 public:
  explicit Ransac(const std::vector<Vector2>& data);
  virtual ~Ransac();

  void setMaxIterations(const int max_iterations);
  void setProbability(const double probability);
  void setDistanceThreshold(const double threshold);

  std::vector<int> getInliers();
  Vector3 getModel();

  std::vector<int> alsoInliers(const Vector3& curve_params);
  bool computeModel();

 private:
  int max_iterations_;
  double probability_;
  double threshold_;
  bool hypo_success;
  std::vector<Vector2> data_;
  std::vector<int> inliers_;
  Vector3 curve_params_;
};
}  // namespace ransac_cpp
