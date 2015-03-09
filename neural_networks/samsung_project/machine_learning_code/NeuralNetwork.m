%%Neural Network Learning code
%% revised from Stanford Machine Learning online class by Prof. Andrew Ng

%  Instructions
%  ------------
% 
%  This file contains code that helps you get started on the
%  linear exercise. You will need to complete the following functions 
%  in this exericse:
%
%     sigmoidGradient.m
%     checkNNGradients.m
%     featureNormalize.m
%     predict.m
%     debugInitializeWeights.m
%     computeNumericalGradients.m
%     fmincg.m
%     randInitializeWeights.m
%     nnCostFunction.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
%clear ; 
close all; clc

%% Setup the parameters you will use for this exercise
input_layer_size  = 561;  % 561 variables in data sub1
hidden_layer_size = 10;   % number of hidden units
num_labels = 6;          % 6 labels as 6 activities, from 1 to 6   

%% =========== Part 1: Loading and Visualizing Data =============
%  We start the exercise by first loading and visualizing the dataset. 
%  You will be working with a dataset that contains handwritten digits.
% Load Training Data
fprintf('Loading and Visualizing Data ...\n')

Xall = csvread('../X.csv');
yall = csvread('../y.csv');
m = size(Xall, 1);

%% =========== Part 1.5: Split data into Training/Test=============
% 70% of the data is randomly picked for training
		 % Training Set ----> X, y
		 % Testing Set ----> Xtest, ytest
R = randperm(m);
indicesTrain = R(1:floor(0.7*m));
indicesTest = R(floor(0.7*m)+1: m);
X = Xall(indicesTrain, :);
y = yall(indicesTrain, :);
Xtest = Xall(indicesTest, :);
ytest = yall(indicesTest, :);
activity = struct('1', 'laying', '2', 'sitting', ...
		    '3', 'standing', '4', 'walk', '5', 'walkup', ...
		    '6', 'walkdown');

# print out top ten first ten variables with activity
fprintf('Training sets have %d records.\n', size(X, 1));
fprintf('First 10 records are: \n')
for ii = (1:10)
  fprintf(' X_train = %5.2f, %5.2f, %5.2f, %5.2f  ..., y_test = %s \n', ...
	    X(ii, 1:4), activity.(num2str(y(ii, :)))
	 );
end
fprintf('Testing sets have %d records.\n', size(Xtest, 1));
fprintf('First 10 records are: \n')
for ii =(1:10)
  fprintf(' X_test = %5.2f, %5.2f, %5.2f, %5.2f  ..., y_test = %s \n', ...
	    Xtest(ii, 1:4), activity.(num2str(ytest(ii, :)))
	);
end
%pause;

%%  ================ Part 2: Scale the Data ================ 
% Before we train the data, the data is scaled to ranging 
%in (0~1.0), with a standard deviation of 1.0 for each variable. 
  [X, means, stds] =  featureNormalize(X);
  Xtest = (Xtest-means)./stds;


%% ================ Part 3: Initializing Pameters ================
%  In this part of the exercise, you will be starting to implment a two
%  layer neural network that classifies digits. You will start by
%  implementing a function to initialize the weights of the neural network
%  (randInitializeWeights.m)
%
fprintf('\nInitializing Neural Network Parameters ...\n')

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];


%%% =============== Part 4: Implement Backpropagation ===============
%%%  Once your cost matches up with ours, you should proceed to implement the
%%%  backpropagation algorithm for the neural network. You should add to the
%%%  code you've written in nnCostFunction.m to return the partial
%%%  derivatives of the parameters.
%%%
%%fprintf('\nChecking Backpropagation... \n');
%%
%%%  Check gradients by running checkNNGradients
%checkNNGradients;
%%
%%fprintf('\nProgram paused. Press enter to continue.\n');
%%pause;
%%
%%
%%% =============== Part 5: Implement Regularization ===============
%%  Once your backpropagation implementation is correct, you should now
%%  continue to implement the regularization with the cost and gradient.
%%
%
%fprintf('\nChecking Backpropagation (w/ Regularization) ... \n')
%
%%  Check gradients by running checkNNGradients
%lambda = 3;
%checkNNGradients(lambda);
%
%% =================== Part 6: Training NN ===================
%  You have now implemented all the code necessary to train a neural 
%  network. To train your neural network, we will now use "fmincg", which
%  is a function which works similarly to "fminunc". Recall that these
%  advanced optimizers are able to train our cost functions efficiently as
%  long as we provide them with the gradient computations.
%
fprintf('\nTraining Neural Network... \n')

%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 50);

%  You should also try different values of lambda
lambda = 30;

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);

% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size *...
                  (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

fprintf('Program paused. Press enter to continue.\n');
%pause;
%
%
%
%% ================= Part 7: Validation=================
%  After training the neural network, we now predict
%  the labels. "predict" function is implemented using the
%  neural network to predict the labels of the training set. 
%  Both training set and testing set are computed.

%testing set
pred = predict(Theta1, Theta2, Xtest);
fprintf('\nTesting Set Accuracy: %f\n', mean(double(pred == ytest)) * 100);
size(nn_params)
input_layer_size
hidden_layer_size
num_labels,
size(Xtest)
size(ytest)
[Jtest, gradtest] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xtest, ytest, 0.0
                                  );
fprintf('J_test = %5.2f \n', Jtest);


%training set
pred = predict(Theta1, Theta2, X);
fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);
[Jtrain, gradtrain] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda
                                  );
fprintf('J_train = %5.2f \n', Jtrain);


