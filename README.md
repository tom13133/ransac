# ransac
A repository to implement ransac algorithm

## Content
### Python version:
#### 1. ransac_curve.py
Read **test_curve.csv** and perform curve fitting using ransac  
* Result:
<img src="https://github.com/tom13133/ransac/blob/master/images/Figure_1.png" width="500">

#### 2. ransac_plane.py
Read **test_plane.csv** and perform plane fitting using ransac  
* Result:
<img src="https://github.com/tom13133/ransac/blob/master/images/Figure_2.png" width="500">

### C++ version
#### 1. package ransac_cpp
Read **test_curve.csv** and perform curve fitting using ransac  

##### Dependencies
Eigen3

* Compile and execute  
```
cd ~/ransac_cpp
cmake ../ransac_cpp
make
./devel/lib/ransac_cpp/ransac_curve
```

## Reference
* Wiki pedia  
