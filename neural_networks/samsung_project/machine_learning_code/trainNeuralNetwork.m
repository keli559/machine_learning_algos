function [Theta1, Theta2, means, stds] =...
  trainNeuralNetwork(X, y, lambda, hidden_layer_size, num_labels)
  % This is a function to compute 2 layer neural network.
  % That is to say, the neural network has only 1 hidden layer
  %
  % Theta1 and Theta2: weights calculated
  % means: the column mean of X 
  % stds: the column standard deviation of X
  % X, y: the training data
  % lambda: regularization parameter
  % hidden_layer_size: the number of elements at the hidden layer



%%Neural Network Learning code
%% revised from Stanford Machine Learning online class by Prof. Andrew Ng
% subfunctions needed for this function:
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


%% Initialization
%% Setup the parameters you will use for this exercise
input_layer_size  = size(X, 2);  % number of variables in data X
% hidden_layer_size:   % number of hidden units
%num_labels           % number of labels


%%  ================ Part 2: Scale the Data ================ 
% Before we train the data, the data is scaled to ranging 
%in (0~1.0), with a standard deviation of 1.0 for each variable. 
  [X, means, stds] =  featureNormalize(X);

%% ================ Part 3: Initializing Pameters ================
%  In this part of the exercise, you will be starting to implment a two
%  layer neural network that classifies digits. You will start by
%  implementing a function to initialize the weights of the neural network
%  (randInitializeWeights.m)
%
initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);
% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];

%% =================== Part 6: Training NN ===================
%  You have now implemented all the code necessary to train a neural 
%  network. To train your neural network, we will now use "fmincg", which
%  is a function which works similarly to "fminunc". Recall that these
%  advanced optimizers are able to train our cost functions efficiently as
%  long as we provide them with the gradient computations.
%

%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 80);

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


