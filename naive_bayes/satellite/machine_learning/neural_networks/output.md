```
octave:2> Optimization
Loading and Visualizing Data ...
Training set has 3600 records.
Cross Validation set has 1200 records.
Testing set has 1200 records.

 First 10 records from Training set are: 
 X_train = 172.90, 93.90, 216.90, 162.10  ..., y_train =   0.0 
 X_train = 175.80, 94.50, 210.30, 150.50  ..., y_train = (0.1, 1] 
 X_train = 175.50, 92.70, 209.60, 145.40  ..., y_train =   0.0 
 X_train = 167.20, 88.10, 198.90, 136.40  ..., y_train =   0.0 
 X_train = 172.20, 88.70, 196.10, 127.70  ..., y_train =   0.0 
 X_train = 173.80, 92.90, 221.40, 168.30  ..., y_train =   0.0 
 X_train = 170.60, 91.00, 199.20, 132.10  ..., y_train = (0.01, 0.1] 
 X_train = 172.90, 92.90, 208.80, 151.00  ..., y_train =   0.0 
 X_train = 173.80, 93.90, 201.60, 135.80  ..., y_train =   0.0 
 X_train = 171.40, 91.80, 208.70, 149.10  ..., y_train =   0.0 
Program paused. Press enter to continue.

===Train Neural Network===
Training Set Accuracy: 90.916667
J_train =  0.54 

Cross Validation Set Accuracy: 90.750000
J_val =  0.56 

Testing Set Accuracy: 91.333333
J_test =  0.51 
Baseline Accuracy is:  0.88
Total time duration:  0.35 min.
```

```
===Learning Cure for Numbers of Training Samples===
# Training Examples	Train Error	Cross Validation Error
  	1		NaN	NaN
  	241		0.413273	0.630421
  	481		0.464802	0.574687
  	721		0.505448	0.558885
  	961		0.486862	0.583481
  	1201		0.490429	0.570148
  	1441		0.495222	0.559772
  	1681		0.525957	0.560374
  	1921		0.542252	0.563358
  	2161		0.562577	0.575808
  	2401		0.552987	0.563252
  	2641		0.536215	0.558945
  	2881		0.543215	0.567179
  	3121		0.531082	0.565910
  	3361		0.528883	0.563084
Program paused. Press enter to continue.
```

```
===Validation for Selecting Lambda===
lambda		Train Error	Validation Error
 0.000000	0.532020	0.559746
 0.100000	0.530707	0.555151
 0.300000	0.540812	0.565430
 1.000000	0.540122	0.563861
 3.000000	0.571414	0.581951
 10.000000	0.609099	0.607371
 30.000000	0.703933	0.674335
 100.000000	0.878231	0.796587
Program paused. Press enter to continue.
```

```
===Validation for Hidden Layer Size===
Hidden Layer Size		Train Error	Validation Error
 2.000000	0.664134	0.666408
 4.000000	0.542728	0.584293
 6.000000	0.531281	0.560523
 8.000000	0.539963	0.563210
 10.000000	0.535479	0.565256
 12.000000	0.531952	0.561790
 14.000000	0.541770	0.560251
 16.000000	0.547130	0.579266
Program paused. Press enter to continue.
octave:3> 
```