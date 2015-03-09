% This optimization analysis for neural network machine learning
% is revised from:
% Stanford Machine Learning online class by Andrew Ng, 
% Exercise 5 | Regularized Linear Regression and Bias-Variance
% and programmed by Ke Li to fit the purpose of usage for neural network algo

%% Initialization
   clear ; close all; clc
warning('off','all');
%%===================Part 1: Loading and Visualizing Data==================
% We start the excercise by first loading and visualizing the dataset. 
% The following code will load the dataset into your environment and load
% the data.

% Load all data from ../X.csv and ../y.csv
fprintf('Loading and Visualizing Data ...\n')
X = csvread('../X.csv');
y = csvread('../y.csv');
m = size(X, 1);

%%============Part 2: Split Data into Train, Cross Validation, Test=========
% 60% of the data is randomly picked for training
% 20% for cross validation
% 20% for testing
%
% Training         ---> Xtrain, ytrain
% Cross Validation ---> Xval,   yval
% Testing          ---> Xtest,  ytest

  R = randperm(m);
indicesTrain = R(1:floor(0.6*m));
indicesVal = R(floor(0.6*m)+1: floor(0.8*m));
indicesTest = R(floor(0.8*m)+1: m);

Xtrain = X(indicesTrain, :);
ytrain = y(indicesTrain, :);
Xval = X(indicesVal, :);
yval = y(indicesVal, :);
Xtest = X(indicesTest, :);
ytest = y(indicesTest, :);

activity = struct('1', 'laying', '2', 'sitting', ...
		    '3', 'standing', '4', 'walk', '5', 'walkup', ...
		    '6', 'walkdown');

# print out first ten records with first 4 variables with activity
fprintf('Training set has %d records.\n', size(Xtrain, 1));
fprintf('Cross Validation set has %d records.\n', size(Xval, 1));
fprintf('Testing set has %d records.\n', size(Xtest, 1));
fprintf('\n First 10 records from Training set are: \n')
for ii = (1:10)
  fprintf(' X_train = %5.2f, %5.2f, %5.2f, %5.2f  ..., y_test = %s \n', ...
	    Xtrain(ii, 1:4), activity.(num2str(ytrain(ii, :)))
	 );
end


fprintf('Program paused. Press enter to continue.\n');
pause;
%% =========== Part 3: Train Neural Network =============
fprintf('\n===Train Neural Network===\n')
lambda = 0;
hidden_layer_size = 10;
num_labels = 6;
input_layer_size = size(Xtrain, 2);
[Theta1, Theta2, means, stds] =...
  trainNeuralNetwork(Xtrain, ytrain, ...
			lambda, hidden_layer_size, num_labels);
%training set
Xtrain = (Xtrain-means)./stds;
predtrain = predict(Theta1, Theta2, Xtrain);
fprintf('\nTraining Set Accuracy: %f\n', ...
	 mean(double(predtrain == ytrain)) * 100);

nn_params = [Theta1(:); Theta2(:)];
[Jtrain, gradtrain] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xtrain, ytrain, lambda
                                  );
fprintf('J_train = %5.2f \n', Jtrain);


%Cross Validation set
Xval= (Xval-means)./stds;
predval = predict(Theta1, Theta2, Xval);
fprintf('\nCross Validation Set Accuracy: %f\n', mean(double(predval == yval)) * 100);
[Jval, gradval] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xval, yval, 0.0
                                  );
fprintf('J_val = %5.2f \n', Jval);



%testing set
Xtest = (Xtest-means)./stds;
predtest = predict(Theta1, Theta2, Xtest);
fprintf('\nTesting Set Accuracy: %f\n', mean(double(predtest == ytest)) * 100);
[Jtest, gradtest] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xtest, ytest, 0.0
                                  );
fprintf('J_test = %5.2f \n', Jtest);
pause;
%%% =========== Part 4: Learning Curve for Number of Training Samples========
%% an experiment is made with Neural Network with various numbers 
%% of hidden layer unit
%fprintf('\n===Learning Cure for Numbers of Training Samples===\n')
%  lambda = 0.0;
%  [error_train, error_val] = ...
%    learningCurve(Xtrain, ytrain, Xval, yval, ...
%		  lambda, hidden_layer_size, num_labels);
%indices = (1:length(error_train))(error_train~=0);
%plot(indices, error_train(indices), indices, error_val(indices));
%title('Learning curves for Neural Network')
%legend('Train', 'Cross Validation')
%xlabel('Number of traning examples')
%ylabel('Error')
%
%
%fprintf('# Training Examples\tTrain Error\tCross Validation Error\n');
%for i = indices
%    fprintf('  \t%d\t\t%f\t%f\n', i, error_train(i), error_val(i));
%end
%
%fprintf('Program paused. Press enter to continue.\n');
%pause;
%
%%% =========== Part 8: Validation for Selecting Lambda =============
%%  You will now implement validationCurve to test various values of 
%%  lambda on a validation set. You will then use this to select the
%%  "best" lambda value.
%fprintf('\n===Validation for Selecting Lambda===\n')
%[lambda_vec, error_train, error_val] = ...
%  validationCurve(Xtrain, ytrain, Xval, yval, hidden_layer_size, num_labels);
%
%close all;
%plot(lambda_vec, error_train, lambda_vec, error_val);
%title('Validation Curves for Neural Network (lambda)')
%legend('Train', 'Cross Validation');
%xlabel('lambda');
%ylabel('Error');
%
%fprintf('lambda\t\tTrain Error\tValidation Error\n');
%for i = 1:length(lambda_vec)
%	fprintf(' %f\t%f\t%f\n', ...
%            lambda_vec(i), error_train(i), error_val(i));
%end
%
%fprintf('Program paused. Press enter to continue.\n');
%pause;
%
%% =========== Part 8: Validation for Hidden Layer Size =============
%  You will now implement validationCurve to test various values hidden
% layer size on a validation set. You will then use this to select the
%  "best" hidden layer size.

fprintf('\n===Validation for Hidden Layer Size===\n')
lambda = 0.0;
[hidden_layer_size_vec, error_train, error_val] = ...
  validationCurve_hl(Xtrain, ytrain, Xval, yval, lambda, num_labels);

close all;
plot(hidden_layer_size_vec, error_train, hidden_layer_size_vec, error_val);
title('Validation Curves for Neural Network (hidden layer size)')
legend('Train', 'Cross Validation');
xlabel('Hidden layer size');
ylabel('Error');

fprintf('Hidden Layer Size\t\tTrain Error\tValidation Error\n');
for i = 1:length(hidden_layer_size_vec)
	fprintf(' %f\t%f\t%f\n', ...
            hidden_layer_size_vec(i), error_train(i), error_val(i));
end

fprintf('Program paused. Press enter to continue.\n');
pause;





