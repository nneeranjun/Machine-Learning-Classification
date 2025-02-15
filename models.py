import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.get_weights(), x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x)) >= 0:
            return 1
        else:
            return -1


    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        not_converged = True
        while not_converged:
            not_converged = False
            for x, y in dataset.iterate_once(1):
                pred = self.get_prediction(x)
                if nn.as_scalar(y) != pred:
                    not_converged = True
                    nn.Parameter.update(self.get_weights(), x, nn.as_scalar(y))

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.05
        self.first_weight = nn.Parameter(1, 120)
        self.second_weight = nn.Parameter(120, 1)
        self.bias_1 = nn.Parameter(1, 120)
        self.bias_2 = nn.Parameter(1, 1)
        

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        plus_b = nn.AddBias(nn.Linear(x, self.first_weight), self.bias_1)
        lt = nn.Linear(nn.ReLU(plus_b), self.second_weight)
        return nn.AddBias(lt, self.bias_2)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        model_r = self.run(x)
        return nn.SquareLoss(model_r, y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        arr = [-0.003, -0.008, -0.004, -0.01]
        while True:
            for x, y in dataset.iterate_once(1):
                arr2 = [self.first_weight, self.second_weight, self.bias_1, self.bias_2]
                gradient = nn.gradients(self.get_loss(x, y), arr2)
                self.first_weight.update(gradient[0], arr[0])
                self.second_weight.update(gradient[1], arr[1])
                self.bias_1.update(gradient[2], arr[2])
                self.bias_2.update(gradient[3], arr[3])
            gl2 = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))

            if nn.as_scalar(gl2) <= .02:
                return


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.05
        self.first_weight = nn.Parameter(784, 120)
        self.second_weight = nn.Parameter(120, 10)
        self.bias_1 = nn.Parameter(1, 120)
        self.bias_2 = nn.Parameter(1, 10)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        plus_b = nn.AddBias(nn.Linear(x, self.first_weight), self.bias_1)
        lt = nn.Linear(nn.ReLU(plus_b), self.second_weight)
        return nn.AddBias(lt, self.bias_2)


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        r = self.run(x)
        return nn.SoftmaxLoss(r, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        arr = [-0.0062, -0.0061, -0.0051, -0.0063]
        while True:
            for x, y in dataset.iterate_once(1):
                arr2 = [self.first_weight, self.second_weight, self.bias_1, self.bias_2]
                gradient = nn.gradients(self.get_loss(x, y), arr2)
                self.first_weight.update(gradient[0], arr[0])
                self.second_weight.update(gradient[1], arr[1])
                self.bias_1.update(gradient[2], arr[2])
                self.bias_2.update(gradient[3], arr[3])
            if dataset.get_validation_accuracy() > .97:
                return


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]


        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.hidden_layers = 400
        self.weightInitial = nn.Parameter(self.num_chars, self.hidden_layers)
        self.weightHidden = nn.Parameter(self.hidden_layers, self.hidden_layers)
        self.weightTerminal = nn.Parameter(self.hidden_layers, 5)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        init = nn.Linear(xs[0], self.weightInitial)
        copy = init
        enum = enumerate(xs[1:])
        for j, v in enum:
            nn2 = nn.Linear(copy, self.weightHidden)
            copy = nn.Add(nn.Linear(v, self.weightInitial), nn2)
        return nn.Linear(copy, self.weightTerminal)


    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        r = self.run(xs)
        return nn.SoftmaxLoss(r, y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        arr = [-.0005, -.0005, -.0005]
        while True:
            for x, y in dataset.iterate_once(3):
                arr2 = [self.weightInitial, self.weightHidden, self.weightTerminal]
                gradient = nn.gradients(self.get_loss(x, y), arr2)
                self.weightInitial.update(gradient[0], arr[0])
                self.weightHidden.update(gradient[1], arr[1])
                self.weightTerminal.update(gradient[2], arr[2])
            if dataset.get_validation_accuracy() > .80:
                return
