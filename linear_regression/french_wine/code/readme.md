# Code documentation

This octave/matlab code is written to predict the French Wine price using multivariate linear regression algorithm. 

##The main program: mainProgram.m
The main program does the following task:

### Part 1. Feature Normalization
This part includes downloading the data, scaling the data to center at 0.0 with standard deviation of 1.0, and prepare the data for gradient descent algorithm.

#### subfunctions used: 
featureNormalize.m

### Part 2: Gradient Descent

This part uses gradient descent to calculate the cost function J. The cost function is defined as the difference between hypothesis (h(x)) and actual data (y).

 J(theta, X) = sum((h(x, theta) - y)^2.0)

With cost function and its gradient with thetas, gradient descent is used to find the thetas that minimize the cost function J. 

#### subfunctions used:

* gradientDescentMulti.m
compute through iteration to find the thetas that minimize cost function J. 
* computeCostMulti.m
compute the cost function for multiviate linear regression.

### Part 3: Validation

Use test data (data_test) to validate the linear regression model. The wine prices is predicted (yprediction). The prediction is compared with the given prices in the test data. 

both Squre Sum Error (SSE) and Squre Sum Total (SST) to calculate coefficient of determination R-squared:

R-squared = 1.0 - SSE/SST

