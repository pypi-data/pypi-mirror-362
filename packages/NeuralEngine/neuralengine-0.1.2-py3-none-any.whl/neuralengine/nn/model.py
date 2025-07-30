import neuralengine.config as cf
from ..tensor import Tensor, array
from .layers import Layer, Mode, Flatten, LSTM
from .optim import Optimizer
from .loss import Loss


class Model:
    """A class to build and train a neural network model.
    Allows for defining the model architecture, optimizer, loss function, and metrics.
    The model can be trained and evaluated.
    """

    def __init__(self, input_size: tuple | int, optimizer: Optimizer = None, loss: Loss = None, metrics=()):
        """
        @param input_size: Tuple or int, shape of input data samples (int if 1D).
        @param optimizer: Optimizer instance.
        @param loss: Loss instance.
        @param metrics: List/tuple of Metric or Loss instances or func(x, y) → dict[str, float | np.ndarray].
        """

        self.input_size = input_size

        if not isinstance(optimizer, Optimizer):
            raise ValueError("optimizer must be an instance of Optimizer class")
        self.optimizer = optimizer

        if not isinstance(loss, Loss):
            raise ValueError("loss must be an instance of Loss class")
        self.loss = loss

        self.metrics = metrics if isinstance(metrics, (list, tuple)) else (metrics,)


    def __call__(self, *layers: Layer) -> None:
        """
        Allows the model to be called with layers to build the model.
        @param layers: Variable number of Layer instances to add to the model.
        """
        self.build(*layers)


    def build(self, *layers: Layer) -> None:
        """
        Builds the model by adding layers.
        @param layers: Variable number of Layer instances to add to the model.
        """

        parameters, prevLayer = [], None
        for layer in layers:

            if not isinstance(layer, Layer):
                raise ValueError("All layers must be instances of Layer class")
            
            # If stacking LSTM layers, update input size and output selection
            if isinstance(layer, LSTM) and isinstance(prevLayer, LSTM):
                out_size = prevLayer.out_size
                if prevLayer.attention: out_size += prevLayer.in_size[-1]
                if prevLayer.bidirectional: out_size *= 2
                self.input_size = (*prevLayer.in_size[:-1], out_size)
                prevLayer.return_seq = True
                if not 0 in prevLayer.use_output:
                    if prevLayer.return_state: prevLayer.use_output = (0, 1, 2)
                    else: prevLayer.use_output = (0,)
            prevLayer = layer

            if layer.in_size is None:
                layer.in_size = self.input_size
            self.input_size = layer.out_size if hasattr(layer, 'out_size') else self.input_size
            if isinstance(layer, Flatten):
                self.input_size = int(cf.nu.prod(array(self.input_size)))

            parameters.extend(layer.parameters()) # Collect parameters from the layer
            
        self.layers = layers
        self.optimizer.parameters = parameters


    def train(self, x, y, epochs: int = 10, batch_size: int = 64, random_seed: int = None) -> None:
        """
        Trains the model on data.
        @param x: Input data, shape (N, features)
        @param y: Target data, shape (N, target_features)
        @param epochs: Number of epochs
        @param batch_size: Batch size (None for full batch)
        @param random_seed: Seed for shuffling
        """

        for layer in self.layers:
            layer.mode = Mode.TRAIN

        x, y = array(x), array(y)

        if batch_size is None:
            batch_size = x.shape[0]
        if batch_size <= 0 or batch_size > x.shape[0]:
            raise ValueError("batch_size must be a positive integer ≤ number of samples")

        for i in range(epochs):

            loss_val, metric_vals = 0, {}
            cf.nu.random.seed(random_seed)
            shuffle_indices = cf.nu.random.permutation(x.shape[0])
            x, y = x[shuffle_indices], y[shuffle_indices] # Shuffle data

            for j in range(0, x.shape[0], batch_size):
                x_batch = x[j:j + batch_size]
                y_batch = y[j:j + batch_size]

                # Forward pass
                prevLayer = None
                for layer in self.layers:
                    # For stacked LSTM, pass outputs accordingly
                    if isinstance(prevLayer, LSTM):
                        x_batch, *args = [x_batch[i] for i in prevLayer.use_output]
                        x_batch = layer(x_batch, *args)
                    else: x_batch = layer(x_batch)
                    prevLayer = layer
                    
                # Compute loss
                loss = self.loss(x_batch, y_batch)
                loss_val += self.loss.loss_val

                loss.backward() # Backward pass

                # Compute metrics
                for metric in self.metrics:
                    metric_val = metric(x_batch, y_batch)
                    if isinstance(metric, Loss):
                        key = metric.__class__.__name__
                        metric_vals[key] = metric_vals.get(key, 0.0) + metric.loss_val
                        continue
                    for key, value in metric_val.items():
                        if value is None: continue
                        metric_vals[key] = metric_vals.get(key, 0.0) + value

                # Update parameters
                self.optimizer.step()
                self.optimizer.reset_grad() # Reset gradients

            loss_val /= (x.shape[0] / batch_size) # Average loss over batches
            output_str = f"Epoch {i + 1}/{epochs}, Loss: {loss_val:.4f}, "

            for key, value in metric_vals.items():
                value /= (x.shape[0] / batch_size) # Average metric over batches
                if isinstance(value, (cf.nu.ndarray)) and value.ndim == 1:
                    value = value.mean(keepdims=False)
                output_str += f"{key}: {value:.4f}, "

            print(output_str[:-2])


    def eval(self, x, y) -> Tensor:
        """
        Evaluates the model on data.
        @param x: Input data, shape (N, features)
        @param y: Target data, shape (N, target_features)
        @return: Output tensor after evaluation
        """

        for layer in self.layers:
            layer.mode = Mode.EVAL

        # Forward pass
        z, prevLayer = x, None
        for layer in self.layers:
            # For stacked LSTM, pass outputs accordingly
            if isinstance(prevLayer, LSTM):
                z, *args = [z[i] for i in prevLayer.use_output]
                z = layer(z, *args)
            else: z = layer(z)
            prevLayer = layer

        self.loss(z, y) # Compute loss

        # Compute metrics
        cm = False
        for metric in self.metrics:
            metric(z, y)
            cm = metric.cm if hasattr(metric, 'cm') else cm

        print(f"Evaluation: (Loss) {self.loss}", *self.metrics, sep=", ")
        if cm is not False:
            print(f"Confusion Matrix:\n{cm}")
        return z