#include <unistd.h>
#include <iostream>
#include <fstream>

#include <ransac.hpp>

using ransac_cpp::Vector2;
using ransac_cpp::Ransac;
int main() {
  // Read data
  std::vector<Vector2> input;

  std::fstream file;

  char *path = NULL;
  size_t size;
  path = getcwd(path, size);
  std::string file_name(path);
  file_name += "/test_curve.csv";

  file.open(file_name);
  std::vector<double> pair_data;
  std::string line;
  std::string data;
  if (file.good()) {
    while (getline(file, line, '\n')) {
      pair_data.clear();
      std::istringstream templine(line);
      while (getline(templine, data, ',')) {
        pair_data.push_back(std::atof(data.c_str()));
      }
      Vector2 p_c{pair_data[0], pair_data[1]};
      input.push_back(p_c);
    }

    std::vector<int> inliers;
    Ransac ransac(input);
    ransac.setMaxIterations(1000);
    ransac.setDistanceThreshold(1);
    ransac.setProbability(0.99);
    ransac.computeModel();
    inliers = ransac.getInliers();
    for (int i = 0; i < input.size(); i++) {
      std::cout << input[i].x() << ", " << input[i].y() << ", ";
      if (std::find(inliers.begin(), inliers.end(), i) != inliers.end())
        std::cout << "1" << std::endl;
      else
        std::cout << "0" << std::endl;
    }

  } else {
    std::cout << "Cannot load file " << file_name << std::endl;
  }
  return 0;
}
