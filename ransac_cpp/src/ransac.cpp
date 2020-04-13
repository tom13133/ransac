#include <iostream>
#include <random>
#include <ransac.hpp>

namespace ransac_cpp {
Ransac::Ransac(const std::vector<Vector2>& data) {
  data_.assign(data.begin(), data.end());
  max_iterations_ = 100;
  probability_ = 0.99;
  threshold_ = 0.1;
  hypo_success = true;
  curve_params_ = Vector3{0, 0, 0};
}

Ransac::~Ransac() {}
void Ransac::setMaxIterations(const int max_iterations) {
  max_iterations_ = max_iterations;
}

void Ransac::setProbability(const double probability) {
  probability_ = probability;
}

void Ransac::setDistanceThreshold(const double threshold) {
  threshold_ = threshold;
}

std::vector<int> Ransac::getInliers() {
  if (!hypo_success)
    inliers_.clear();
  return inliers_;
}

Vector3 Ransac::getModel() {
  return curve_params_;
}

std::vector<int> Ransac::alsoInliers(const Vector3& curve_params) {
  std::vector<int> res;
  int x, y, y_pred;
  for (int i = 0; i < data_.size(); i++) {
    x = data_[i].x();
    y = data_[i].y();
    y_pred = curve_params[0]*x*x + curve_params[1]*x + curve_params[2];
    if (std::fabs(y - y_pred) < threshold_)
      res.push_back(i);
  }
  return res;
}

Vector3 curve_fit(const std::vector<Vector2>& hypo_inliers) {
  Vector2 p1 = hypo_inliers[0];
  Vector2 p2 = hypo_inliers[1];
  Vector2 p3 = hypo_inliers[2];

  Eigen::MatrixXd M(3, 3), y(3, 1), res(3, 1);
  M << p1.x() * p1.x(), p1.x(), 1,
       p2.x() * p2.x(), p2.x(), 1,
       p3.x() * p3.x(), p3.x(), 1;
  y << p1.y(),
       p2.y(),
       p3.y();

  res = M.inverse() * y;
  Vector3 res_(res(0, 0), res(1, 0), res(2, 0));
  return res_;
}

bool Ransac::computeModel() {
  int max_count = 0;
  std::uniform_int_distribution<unsigned> u(0, data_.size()-1);
  std::default_random_engine e;
  std::vector<Vector2> hypo_inliers;
  std::vector<int> temp_inliers, inliers;
  Vector3 curve_params;
  for (int i = 0; i < max_iterations_; i++) {
    hypo_inliers.clear();
    int count = 0;
    while (hypo_inliers.size() < 3) {
      count++;
      if (count > 100) {
        std::cout << "Input data is not enough to find hypo_inliers" << std::endl;
        hypo_success = false;
        return false;
      }
      int choice = u(e);
      bool valid = true;
      for (int j = 0; j < hypo_inliers.size(); j++) {
        if ((data_[choice]-hypo_inliers[j]).norm() < 1e-5) {
          valid = false;
          break;
        }
      }
      if (valid) {
        hypo_inliers.push_back(data_[choice]);
      }
    }
    curve_params = curve_fit(hypo_inliers);
    temp_inliers = alsoInliers(curve_params);
    if (temp_inliers.size() > max_count) {
      max_count = temp_inliers.size();
      inliers_ = temp_inliers;
      curve_params_ = curve_params;
    }
    if (inliers.size()/data_.size() > probability_) {
      return true;
    }
  }
  return false;
}
}  // namespace ransac_cpp
