function [hidden_layer_size_vec, error_train, error_val] = ...
  validationCurve_hl(X, y, Xval, yval, lambda, num_labels)
%VALIDATIONCURVE Generate the train and validation errors needed to
%plot a validation curve that we can use to select lambda
%   [lambda_vec, error_train, error_val] = ...
%       VALIDATIONCURVE(X, y, Xval, yval) returns the train
%       and validation errors (in error_train, error_val)
%       for different values of lambda. You are given the training set (X,
%       y) and validation set (Xval, yval).
%

% Selected values of lambda (you should not change this)
  hidden_layer_size_vec = [2 4 6 8 10 12 14 16]';

% You need to return these variables correctly.
error_train = zeros(length(hidden_layer_size_vec), 1);
error_val = zeros(length(hidden_layer_size_vec), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return training errors in 
%               error_train and the validation errors in error_val. The 
%               vector hidden_layer_size_vec contains the different
%               hiidden layer sizes
%               to use for each calculation of the errors, i.e, 
%               error_train(i), and error_val(i) should give 
%               you the errors obtained after training with 
%               hidden_layer_size = hidden_layer_size_vec(i)
%
% Note: You can loop over hidden_layer_size_vec with the following:
%
input_layer_size = size(X, 2);
       for i = 1:length(hidden_layer_size_vec)
           hidden_layer_size = hidden_layer_size_vec(i);
           % Compute train / val errors when training Neural 
           % Network with regularization parameter lambda
           % You should store the result in error_train(i)
           % and error_val(i)
           [Theta1, Theta2, means, stds] = ...
                 trainNeuralNetwork(X, y, ...
                                    lambda, hidden_layer_size, num_labels);
           nn_params = [Theta1(:); Theta2(:)];
           X = (X-means)./stds;
           [Jtrain, gradtrain] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, 0.0
                                  );
          Xval = (Xval - means)./stds;
          [Jval, gradval] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, Xval, yval, 0.0
                                  );

           error_train(i) = Jtrain;
           error_val(i) = Jval;

           
       end
%










% =========================================================================

end
