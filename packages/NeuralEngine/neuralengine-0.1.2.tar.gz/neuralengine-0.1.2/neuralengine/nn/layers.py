from enum import Enum
from ..tensor import Tensor
from ..utils import *


class Mode(Enum):
    TRAIN = 'train'
    EVAL = 'eval'


class Layer:
    """Base class for all layers."""
    def __init__(self):
        self._mode: Mode = Mode.TRAIN
        self._in_size: tuple | None = None

    def __call__(self, x, *args, **kwargs) -> Tensor:
        """
        Calls the layer's forward method with the provided input.
        @param x: Input tensor.
        @return: Output tensor after applying the layer's forward pass.
        """
        x = x if isinstance(x, Tensor) else Tensor(x)
        return self.forward(x, *args, **kwargs)

    @property
    def mode(self) -> Mode:
        """Current mode of the layer (TRAIN or EVAL)."""
        return self._mode
    
    @mode.setter
    def mode(self, mode: Mode) -> None:
        if mode not in (Mode.TRAIN, Mode.EVAL):
            raise ValueError("mode must be either Mode.TRAIN or Mode.EVAL")
        
        self._mode = mode
        for _, attr in self.__dict__.items():
            if isinstance(attr, Layer):
                attr.mode = mode

    @property
    def in_size(self) -> tuple:
        """Input size of the layer."""
        return self._in_size
    
    @in_size.setter
    def in_size(self, size: tuple | int) -> None:
        size = size if isinstance(size, (tuple, list)) else (size,)
        if not all(isinstance(size, int) and size > 0 for size in size):
            raise ValueError("in_size must be all positive integers")
        
        self._in_size = size
        self._initialize_parameters()

    def _initialize_parameters(self) -> None:
        """Initializes layer parameters. To be implemented by subclasses."""
        pass

    def parameters(self):
        """Yields all trainable parameters for the layer."""
        for _, attr in self.__dict__.items():
            if isinstance(attr, Layer):
                yield from attr.parameters()
            elif isinstance(attr, Tensor):
                if attr.requires_grad:
                    yield attr


class Linear(Layer):
    """Fully connected layer."""
    def __init__(self, out_size: int, in_size: int | tuple = None, bias: bool = True, activation: Layer = None):
        """
        @param out_size: Number of output features.
        @param in_size: Number of input features or shape of input tensor.
        @param bias: Whether to include a bias term.
        @param activation: (optional) Activation layer to apply after the linear transformation.
        """
        super().__init__()
        self.has_bias = bias
        self.out_size = out_size
        if in_size: self.in_size = in_size

        if not isinstance(activation, (type(None), Layer)):
            raise ValueError("activation must be an instance of Layer class")
        self.activation = activation

    def _initialize_parameters(self) -> None:
        # Xavier initialization for weights
        self.W = randn((*self.in_size, self.out_size), xavier=True, requires_grad=True)
        if self.has_bias:
            self.b = zeros((1, self.out_size), requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        # z = x.W + b
        z = x @ self.W
        if self.has_bias:
            z += self.b
        if self.activation:
            z = self.activation(z)
        return z


class LSTM(Layer):
    """Long Short-Term Memory layer."""
    def __init__(self, lstm_units: int, in_size: int | tuple = None, n_timesteps: int = None, bias: bool = True, 
                 attention: bool = False, return_seq: bool = False, return_state: bool = False, 
                 bidirectional: bool = False, use_output: int | tuple = -1):
        """
        @param lstm_units: Number of LSTM units (output size).
        @param in_size: Number of input features or shape of input tensor.
        @param n_timesteps: Number of timesteps in the input sequence.
        @param bias: Include bias term.
        @param attention: Use multiplicative attention.
        @param return_seq: Return hidden states for all timesteps.
        @param return_state: Return final cell and hidden states.
        @param bidirectional: Use bidirectional LSTM.
        @param use_output: Output selection (-3: all hidden states, -2: cell state, -1: last hidden state).
        """
        super().__init__()
        self.has_bias = bias
        self.out_size = lstm_units
        if in_size: self.in_size = in_size
        self.n_timesteps = n_timesteps
        self.return_seq = return_seq
        self.return_state = return_state
        self.bidirectional = bidirectional
        self.use_output = (use_output,) if isinstance(use_output, int) else use_output
        self.attention = MultiplicativeAttention(lstm_units) if attention else None
        self.sigmoid = Sigmoid()
        self.tanh = Tanh()

    def _initialize_parameters(self) -> None:
        # LSTM gate weights and biases
        concat_size = self.out_size + self.in_size[-1] * (2 if self.attention else 1)
        self.Wf = randn((concat_size, self.out_size), xavier=True, requires_grad=True)
        self.Wi = randn((concat_size, self.out_size), xavier=True, requires_grad=True)
        self.Wc = randn((concat_size, self.out_size), xavier=True, requires_grad=True)
        self.Wo = randn((concat_size, self.out_size), xavier=True, requires_grad=True)

        if self.has_bias:
            self.bf = zeros((1, self.out_size), requires_grad=True)
            self.bi = zeros((1, self.out_size), requires_grad=True)
            self.bc = zeros((1, self.out_size), requires_grad=True)
            self.bo = zeros((1, self.out_size), requires_grad=True)

        if self.attention: self.attention.in_size = self.in_size

    def forward(self, x: Tensor, c: Tensor = None, h: Tensor = None):
        # LSTM forward pass
        c = c if c else zeros((x.shape[0], self.out_size))
        h = h if h else zeros((x.shape[0], self.out_size + (x.shape[-1] if self.attention else 0)))

        output = self.lstm_loop(x, range(self.n_timesteps or x.shape[-2]), c, h)
        if self.bidirectional:
            output_rev = self.lstm_loop(x, range(self.n_timesteps or (x.shape[-2] - 1), -1, -1), c, h)

            combinedOutput = []
            for o, r in zip(output, output_rev):
                # Concatenate outputs from both directions
                combinedOutput.append(concat(o, r, axis=-1))
            output = combinedOutput

        return output

    def lstm_loop(self, x: Tensor, timesteps: range, c: Tensor, h: Tensor):

        if self.return_seq: seq_output = []
        for t in timesteps:
            h_x = concat(h, x[:, t, :], axis=-1)
            f_t = self.sigmoid(h_x @ self.Wf + (self.bf if self.has_bias else 0))  # Forget gate f_t = σ(Wf.[h, x_t] + bf)
            i_t = self.sigmoid(h_x @ self.Wi + (self.bi if self.has_bias else 0))  # Input gate i_t = σ(Wi.[h, x_t] + bi)
            c_tilde = self.tanh(h_x @ self.Wc + (self.bc if self.has_bias else 0))  # Cell candidate c~_t = tanh(Wc.[h, x_t] + bc)
            c = f_t * c + i_t * c_tilde  # Cell state c_t = f_t * c_{t-1} + i_t * c~_t
            o_t = self.sigmoid(h_x @ self.Wo + (self.bo if self.has_bias else 0))  # Output gate o_t = σ(Wo.[h, x_t] + bo)
            h = o_t * self.tanh(c)  # Hidden state h_t = o_t * tanh(c_t)

            if self.attention:
                context = self.attention(h, x)
                h = concat(h, context, axis=-1)

            if self.return_seq: seq_output.append(h)

        output = [c, h] if self.return_state else [h]
        if self.return_seq: output.insert(0, stack(*seq_output, axis=1))
        return output


class MultiplicativeAttention(Layer):
    """Multiplicative (dot-product) attention layer."""
    def __init__(self, units: int, in_size: int | tuple = None):
        """
        @param units: Number of attention units (output size).
        @param in_size: Number of input features or shape of input tensor.
        """
        super().__init__()
        self.out_size = units
        self.softmax = Softmax(axis=-1)
        if in_size: self.in_size = in_size

    def _initialize_parameters(self) -> None:
        # Attention weight matrix
        self.Wa = randn((self.out_size, self.in_size[-1]), xavier=True, requires_grad=True)

    def forward(self, h: Tensor, x: Tensor) -> Tensor:
        # scores = (q.Wa.xᵗ) / √d_k
        q = h.reshape(h.shape[0], 1, -1)
        scores = (q @ self.Wa @ x.transpose(0, 2, 1)) / (self.out_size ** 0.5)
        attn_weights = self.softmax(scores)

        z = attn_weights @ x
        z = z.reshape(z.shape[0], -1)
        return z
    

class MultiHeadSelfAttention(Layer):
    """Multi-head self-attention layer."""
    def __init__(self, num_heads: int = 1, in_size: int | tuple = None):
        """
        @param num_heads: Number of attention heads.
        @param in_size: Number of input features or shape of input tensor.
        """
        super().__init__()
        self.num_heads = num_heads
        self.softmax = Softmax(axis=-1)
        if in_size: self.in_size = in_size

    def _initialize_parameters(self) -> None:
        self.out_size = self.in_size[-1]
        self.head_dim = self.out_size // self.num_heads # Dimension of each head's output
        # Initialize parameters for combined Q, K, V projections
        self.Wq = randn((self.out_size, self.out_size), xavier=True, requires_grad=True)
        self.Wk = randn((self.out_size, self.out_size), xavier=True, requires_grad=True)
        self.Wv = randn((self.out_size, self.out_size), xavier=True, requires_grad=True)
        
        # Output projection
        self.Wo = randn((self.out_size, self.out_size), xavier=True, requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        batch_size, seq_len, _ = x.shape

        q = x @ self.Wq
        k = x @ self.Wk
        v = x @ self.Wv

        # Result: (batch_size, num_heads, seq_len, head_dim)
        q = q.reshape(batch_size, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        k = k.reshape(batch_size, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        v = v.reshape(batch_size, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)

        # Result: (batch_size, num_heads, seq_len, seq_len)
        scores = (q @ k.transpose(0, 1, 3, 2)) / (self.head_dim ** 0.5)
        attn_weights = self.softmax(scores)

        # Result: (batch_size, num_heads, seq_len, head_dim)
        z = attn_weights @ v
        # Result: (batch_size, seq_len, num_heads * head_dim)
        z = z.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, self.out_size)
        z = z @ self.Wo # Final output projection
        return z


class Embedding(Layer):
    """Embedding layer for mapping indices to dense vectors."""
    def __init__(self, embed_size: int, vocab_size: int = None, n_timesteps: int = None):
        """
        @param embed_size: Size of the embedding vectors.
        @param vocab_size: Number of unique tokens in the vocabulary.
        @param n_timesteps: Number of timesteps in the input sequence (for positional encoding).
        """
        super().__init__()
        self.n_timesteps = n_timesteps
        self.out_size = embed_size
        if vocab_size: self.in_size = vocab_size

        if self.n_timesteps:
            # Positional encoding for n_timesteps
            self.PE = randn((self.n_timesteps, self.out_size), xavier=True, requires_grad=True)

    def _initialize_parameters(self) -> None:
        # Embedding matrix
        self.TE = randn((*self.in_size, self.out_size), xavier=True, requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        # z = TE[x]
        z = self.TE[x.data]
        if self.n_timesteps:
            # Add positional encoding if n_timesteps is specified
            z += self.PE[:self.n_timesteps].reshape(1, x.shape[1], -1)
        return z


class LayerNorm(Layer):
    """Layer normalization."""
    def __init__(self, norm_shape: tuple = None, eps: float = 1e-7):
        """
        @param norm_shape: Shape of the normalization parameters (gamma and beta).
        @param eps: Small value for numerical stability.
        """
        super().__init__()
        self.eps = eps
        if norm_shape:
            self.gamma = ones(norm_shape, requires_grad=True)
            self.beta = zeros(norm_shape, requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        # z = (x - μ) / (σ + ε)
        mean = x.mean(axis=-1, keepdims=True)
        std = sqrt(x.var(axis=-1, keepdims=True))
        z = (x - mean) / (std + self.eps)
        if self.gamma and self.beta:
            # z = γ · z + β
            z = self.gamma * z + self.beta
        return z


class Dropout(Layer):
    """Dropout regularization."""
    def __init__(self, prob: float = 0.5):
        """
        @param prob: Probability of dropping out a unit.
        """
        super().__init__()
        self.prob = prob

    def forward(self, x: Tensor) -> Tensor:
        # z = x · mask / (1 - p)
        if self.mode == Mode.EVAL:
            return x
        
        mask = rand(x.shape) < self.prob
        z = x.masked_fill(mask, 0)
        z /= (1 - self.prob)
        return z


class Flatten(Layer):
    """Flattens input tensor."""
    def __init__(self):
        super().__init__()

    def forward(self, x: Tensor) -> Tensor:
        if len(x.shape) < 2:
            raise ValueError("Input must have at least 2 dimensions (batch size and features)")
        z = x.reshape(x.shape[0], -1)
        return z
 

## Non-Linearity Layers:
class Sigmoid(Layer):
    """Sigmoid activation."""
    def __init__(self):
        super().__init__()

    def forward(self, x: Tensor) -> Tensor:
        # z = 1 / (1 + e^{-x})
        z = 1 / (1 + exp(-x))
        return z
    

class Tanh(Layer):
    """Tanh activation."""
    def __init__(self):
        super().__init__()
        self.sigmoid = Sigmoid()

    def forward(self, x: Tensor) -> Tensor:
        # z = 2 * σ(2x) - 1
        z = 2 * self.sigmoid(2 * x) - 1
        return z


class RELU(Layer):
    """ReLU activation."""
    def __init__(self, alpha: float = 0, parametric: bool = False):
        """
        @param alpha: (Leaky ReLU) Slope for negative inputs (0 for standard ReLU).
        @param parametric: (Parametric ReLU) Whether to use a learnable parameter for alpha.
        """
        super().__init__()
        self.alpha = Tensor(alpha, requires_grad=parametric)

    def forward(self, x: Tensor) -> Tensor:
        # ReLU: z = max(x, 0) or Leaky/Parametric: z = x if x > 0 else α · x
        z = where(x > 0, x, self.alpha * x)
        return z


class Softmax(Layer):
    """Softmax activation."""
    def __init__(self, axis: int = -1):
        """
        @param axis: Axis along which to compute the softmax (default is -1).
        """
        super().__init__()
        self.axis = axis

    def forward(self, x: Tensor) -> Tensor:
        # x = x - max(x) for numerical stability
        x -= x.max(axis=self.axis, keepdims=True)
        # z = e^x / Σ_j e^{x_j}
        z = exp(x)
        z /= sum(z, axis=self.axis, keepdims=True)
        return z