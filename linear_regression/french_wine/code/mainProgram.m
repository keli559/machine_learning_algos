% Linear regression with multiple variables

% Instructions
%-------------
%
% The following functions are included in this
% main program
%
%% Initialization

%% ===============Part 1: Feature Normalization =================

   clear; close all; clc
   fprintf('Loading data ...\n');

%% Load data
pkg load dataframe
data = dataframe('../wine.csv');
X = data(:, [4, 5]);
y = data(:, 2);
[m,n] = size(X);

% Print out some data points
fprintf('Fist 10 examples from the dataset:\n');
X = reshape(X(:), m, n);
  y = y(:);
fprintf('X = [%8.2f %8.2f], y =  %8.2f\n', [X(1:10, :) y(1:10, :)]');

fprintf('Program paused. Press enter to continue. \n');
pause;

% Scale features and set them to zero mean
fprintf('Normalizing Features ...\n');

[X mu sigma] = featureNormalize(X);

% Add intercept term to X
X = [ones(m, 1) X];


%==================== Part 2: Gradient Descent =============

fprintf('Running gradient descent ...\n');

% Choose some alpha value
alpha = 0.03;
num_iters = 400;

%Init Theta and Run gradient Descent
theta = zeros(3,1);
[theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);


% Plot the convergence graph
figure;
plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Cost J');
print('Figure.png')

% Display gradient descent's result
	fprintf('Theta computed from gradient descent: \n');
	fprintf(' %f \n', theta);
	fprintf('\n');
% Estimate the testing data
data_test = dataframe('../wine_test.csv');
Xtest = data_test(:, [4, 5]);
	[mtest, ntest] = size(Xtest);
	Xtest = reshape(Xtest(:), mtest, ntest);
ytest = data_test(:, 2);
	ytest = ytest(:);

	yprediction = [ones(mtest, 1), (Xtest - mu)./sigma]*theta;
%%  ====================== Part3: Validation =============================

	% SSE, sum squre error = sum((test-test_predict)^2)
	SSE = sum((yprediction - ytest).^2.0);
	% SST, sum squre total = sum((test-training_mean)^2)
	SST = sum((yprediction - mean(y)).^2.0);
	R2 = 1.0-SSE/SST;
	fprintf('\n')
	fprintf('The predicted price: y_predict = %.2f, the actual price: y= %.2f\n', [yprediction, ytest]);
	fprintf('\n For out-of-sampling, he R2 ')
	fprintf('(coefficient of determination) is:\n')
	fprintf('%f\n', R2)
