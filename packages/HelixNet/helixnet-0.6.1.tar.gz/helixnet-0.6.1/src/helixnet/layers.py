"""
This module contains layers.
"""
from typing import List, Dict, Tuple, Optional
from abc import ABC
from numbers import Integral  # Max Pooling
import inspect

from mygrad.operation_base import Operation
from mygrad.tensor_base import Tensor
from mygrad.nnet.layers.utils import sliding_window_view

import numpy as np
import mygrad as mg
from mygrad import nnet

from . import activations

names: Dict[str, int] = {}


class Layer(ABC):
    """
    :param List[mg.Tensor] trainable_params: A list that consists of the parameters that
        will be trained by the optimiser. Pass an empty list to indicate that it has no
        trainable parameters

    This the base class of all layers that gives them a unique name
    if they have trainable parameters and if they don't they will just
    use their type name without counting.
    """

    def __init__(self, trainable_params: List[mg.Tensor],) -> None:
        self.type = self.__class__.__name__
        # self.total_params = total_params
        self._config = self._get_current_config()
        self.trainable_params: List[mg.Tensor] = trainable_params

        if trainable_params != []:
            # In case of the layer doesn't have any trainable parameters.
            # We won't add numbers for it

            if (number := names.get(self.__class__.__name__)):
                self.name = self.__class__.__name__ + " " + str(number)
                names[self.__class__.__name__] += 1
            else:

                self.name = self.__class__.__name__ + " 1"
                names[self.__class__.__name__] = 2  # Because we already used `1`
            for i, parameter in enumerate(trainable_params):
                if isinstance(parameter, np.ndarray):
                    parameter = mg.tensor(parameter, constant=False)
                    self.trainable_params[i] = parameter
                elif isinstance(parameter, mg.Tensor):
                    continue
                else:
                    raise TypeError(f"The parameter of {type(parameter)} at index {i}"
                                    f" must be np.ndarray or mygrad.Tensor")
        else:

            self.name = self.__class__.__name__

    def __call__(self, *args, **kwargs) -> mg.Tensor:
        """
        This operator should perform a forward propagation
        """  # This behaviour will change
        self.forward(*args, **kwargs)

    # pylint: disable-next=C0103
    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """
        :param mg.Tensor | np.ndarray X: The data that should be forward propagated
        :return: The prediction of the layer
        :rtype: mg.Tensor

        this method performs forward propagation
        """
    @mg.no_autodiff
    def predict(self, *args, **kwargs) -> mg.Tensor:
        """
        :param mg.Tensor X: The data of forward pass
        :return: The prediction of the layer
        :rtype: mg.Tensor

        This function should in inference not in training because
        it doesn't track the gradients
        """
        return self.forward(*args, **kwargs)

    def null_grad(self):
        """
        This function resets the gradients of parameters.
        This method should not be modified by children

        This function should be used we want to be sure the gradients don't stack up
        :return: This method doesn't return anything
        """
        for parameter in self.trainable_params:
            parameter.null_grad()

    def output_shape(self, prev_shape: Optional[Tuple[int]] = ()) -> Tuple[int]:
        """
        A simple method that gets the shape of layer's output

        This function should be overloaded in order to get the shape
        but still can work on it's own but it'll need previous shapes
        in order to work properly
        """
        return self.predict(np.zeros((1, *prev_shape))).shape[1:]

    def total_params(self):
        """This method can calculate the number of parameters in each layer

        :rtype: int
        """
        params = 0
        for parameter in self.trainable_params:
            params += np.array(parameter.shape).prod()
        return params

    def _get_current_config(self) -> dict:
        """
        An internal helper to automatically capture the constructor's arguments.
        This is a bit of advanced Python ("introspection").
        """
        # Get the class of the object being created (e.g., Dense, Conv2D)
        cls = self.__class__
        # Get the signature of its __init__ method
        init_signature = inspect.signature(cls.__init__)

        # Get the names of the arguments
        arg_names = [p.name for p in init_signature.parameters.values() if p.name != 'self']

        # Create a dictionary of these arguments and their current values
        config = {"class_name": self.type}
        for name in arg_names:
            if hasattr(self, name):
                value = getattr(self, name)
                # Make it JSON-safe
                if callable(value):
                    config[name] = value.__name__
                elif isinstance(value, (int, str, float, bool, list, tuple, type(None))):
                    config[name] = value
        return config

    def get_config(self) -> dict:
        """Public method to get the stored configuration."""
        return self._config

    def get_weights(self) -> List[np.ndarray]:
        """
        returns a list of weights of them model.
        """
        return [p.data for p in self.trainable_params]

    def set_weights(self, weights: List[np.ndarray]):
        """
        Sets the weights of them model.

        :param List[np.ndarray] weights: This should be the return value of get_weights
        """
        for param, weight_array in zip(self.trainable_params, weights):
            param.data = weight_array

    def populate_self(self, population: dict) -> None:
        """
        This function used in inhereitance in order to
        to get the arguments in and save ``self`` to enable automatic saving

        :param dict population: the argument should be ``local()``
        """
        for key, value in population.items():
            setattr(self, key, value)


class Dense(Layer):
    """
    :param int inputs: The size of inputs.
    :param int params: The size of parameters. It is the size of the output.
    :param activation: The activation function that will be used with the layer.
        Any function or object with ``__call__()`` method.
    :param bool use_bias: Whether to have a bias or not.
    :param dtype: The data type of the parameters of the layers also using
        data types from **MyGrad** is preferred over NumPy

    A simple dense layer.
    """

    # pylint: disable-next=R0913
    def __init__(self, inputs: int, params: int, activation,
                 use_bias: bool = True, dtype=mg.float32) -> None:
        self.inputs = inputs
        self.params = params
        he_stddev = np.sqrt(2. / np.array(inputs).sum())
        self.use_bias = use_bias
        self.activation = activation
        self.out_sh = tuple([params]) if isinstance(params, int) else params
        inputs = tuple([inputs]) if isinstance(inputs, int) else inputs
        self.weights = mg.tensor(np.random.randn(*inputs, *self.out_sh) * he_stddev, constant=False,
                                 dtype=dtype)
        if self.use_bias:
            self.bias = mg.tensor(np.random.randn(1, *self.out_sh), constant=False,
                                  dtype=dtype)

            super().__init__([self.weights, self.bias])
        else:

            super().__init__([self.weights])

    def forward(self, X: np.array):
        """
        :param mg.Tensor X: the inputs of the layer
        :return mg.Tensor: The layer predictions
        """
        output = mg.matmul(X, self.weights)
        if self.use_bias:
            output += self.bias
        return self.activation(output)

    def output_shape(self, prev_shape: Optional[Tuple[int]] = None) -> Tuple[int]:
        return self.out_sh

# Well class _MaxPoolND taken from MyGrad.nnet implementation but it doesn't use
# Floor division so I had to create mine with floor division


class _MaxPoolND(Operation):
    def __call__(self, x, pool, stride):
        self.variables = (x,)  # data: ((N0, ...), C0, ...)
        x = x.data

        assert isinstance(pool, (tuple, list, np.ndarray)) and all(
            i >= 0 and isinstance(i, Integral) for i in pool
        )
        pool = np.asarray(pool, dtype=int)
        assert all(i > 0 for i in pool)
        assert x.ndim >= len(
            pool
        ), "The number of pooled dimensions cannot exceed the dimensionality of the data."

        stride = (
            np.array([stride] * len(pool))
            if isinstance(stride, Integral)
            else np.asarray(stride, dtype=int)
        )
        assert len(stride) == len(pool) and all(
            s >= 1 and isinstance(s, Integral) for s in stride
        )
        # pylint: disable-next= W0201
        self.pool = pool  # (P0, ...)

        self.stride = stride  # (S0, ...) # pylint: disable= W0201

        num_pool = len(pool)
        num_no_pool = x.ndim - num_pool

        x_shape = np.array(x.shape[num_no_pool:])
        w_shape = pool
        # MODIFIED: BY ME `//` instead of `/`
        out_shape = (x_shape - w_shape) // stride + 1

        if not all(i.is_integer() and i > 0 for i in out_shape):
            msg = "Stride and kernel dimensions are incompatible: \n"
            msg += f"Input dimensions: {(tuple(x_shape))}\n"
            msg += f"Stride dimensions: {(tuple(stride))}\n"
            msg += f"Pooling dimensions: {(tuple(w_shape))}\n"
            raise ValueError(msg)

        pool_axes = tuple(-(i + 1) for i in range(num_pool))

        # (G0, ...) is the tuple of grid-positions for placing each window (not including stride)
        # sliding_window_view(x): ((N0, ...), C0, ...)          -> (G0, ..., (N0, ...), P0, ...)
        # max-pool:               (G0, ..., (N0, ...), P0, ...) -> (G0, ..., (N0, ...))
        maxed = sliding_window_view(
            x, self.pool, self.stride).max(axis=pool_axes)
        axes = tuple(range(maxed.ndim))

        # (G0, ..., (N0, ...)) -> ((N0, ...), G0, ...)
        out = maxed.transpose(axes[-num_no_pool:] + axes[:-num_no_pool])
        return out if out.flags["C_CONTIGUOUS"] else np.ascontiguousarray(out)

    def backward_var(self, grad, index, **kwargs): # pylint: disable= R0914
        """Parameters
        ----------
        grad : numpy.ndarray, shape=((N0, ...), G0, ...),
        index : int"""
        var = self.variables[index]
        x = var.data
        num_pool = len(self.pool)

        sl = sliding_window_view(x, self.pool, self.stride)
        grid_shape = sl.shape
        maxed = sl.reshape(*sl.shape[:-num_pool], -1).argmax(-1)
        axes = tuple(range(maxed.ndim))

        # argmax within a given flat-window
        maxed = maxed.transpose(
            axes[num_pool:] + axes[:num_pool]
        )  # ((N0, ...), G0, ...)

        # flat-index offset associated with reshaped window within `x`
        row_major_offset = tuple(np.cumprod(
            x.shape[-num_pool:][:0:-1])[::-1]) + (1,)

        # flat index of argmax, updated based on position within window, according to shape of `x`
        in_window_offset = sum(
            ind * off
            for ind, off in zip(np.unravel_index(maxed, self.pool), row_major_offset)
        )

        # flat-index of strided window placement, relative to `x`
        window_offset = sum(
            ind * s * off
            for ind, s, off in zip(
                np.indices(grid_shape[:num_pool]
                           ), self.stride, row_major_offset
            )
        )

        # indices required to traverse pool-axis-flattened array
        # ((N0, ...) G0*...)
        flat_grid_shape = (
            *maxed.shape[:-num_pool], np.prod(maxed.shape[-num_pool:]))
        index = np.indices(flat_grid_shape)

        # update trailing indices to traverse location of max entries within pooled axes
        index[-1] = (in_window_offset + window_offset).reshape(
            *flat_grid_shape[:-1], -1
        )

        # accumulate gradient within pool-axis-flattened dx, then reshape to match shape of `x`
        dx = np.zeros(x.shape[:-num_pool] + (np.prod(x.shape[-num_pool:]),))
        np.add.at(dx, tuple(index), grad.reshape(*x.shape[:-num_pool], -1))
        return dx.reshape(x.shape)


def _max_pool(
    x,
    pool,
    stride,
    *,
    constant=None,
) -> Tensor:
    # pylint: disable-next= W0212
    return Tensor._op(_MaxPoolND, x, op_args=(pool, stride), constant=constant)


class Conv2D(Layer):
    """
    :param int input_channel: the expected number of input channels.
    :param int output_channel: The number of channels should the layer output.
    :param int kernel_size: the size of the kernel.
    :param activation: The activation function that will be used with the layer.
        Any function or object with ``__call__()`` method.
    :param bool use_bias: Whether to have a bias or not.

    :class:`helixnet.layers.Conv2D` assumes input data is of
        shape **(N, C_in, H, W)**:

    **N**: batch size

    **C_in**: number of input channels

    **H**: height of the input feature map

    **W**: width of the input feature map
    """

    def __init__(self, input_channels: int, output_channels: int, kernel_size,
                 stride=1, padding=0, activation=None, use_bias: bool = True):

        self.populate_self(locals())
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)

        # Xavier/Glorot initialization for weights (filters)
        # Shape: (C_out, C_in, K_H, K_W)
        weight_shape = (output_channels, input_channels, *kernel_size)
        self.weights = mg.tensor(
            np.random.randn(*weight_shape)
            * np.sqrt(2.
                    / (input_channels * kernel_size[0] * kernel_size[1]))
        )

        self.use_bias = use_bias
        self.activation = activation
        self.kernel_size = kernel_size
        if self.use_bias:
            # Bias has one value per output channel
            self.bias = mg.tensor(np.zeros(output_channels))
            super().__init__([self.weights, self.bias])
        else:
            self.bias = None
            super().__init__([self.weights])

        self.stride = stride
        self.padding = padding

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """
        Performs a forward pass.

        Also the images needs t be in the following shape
        (batch_size, color_channels, length, width)
        """
        conv_result = nnet.conv_nd(X, self.weights, stride=self.stride,
                                   padding=self.padding)

        if self.use_bias:
            # Reshape bias for broadcasting: (C_out,) -> (1, C_out, 1, 1)
            conv_result = conv_result + self.bias.reshape(1, -1, 1, 1)
        return self.activation(conv_result)


class Flatten(Layer):
    """
    A simple flatten layer that turns it's inputs into a flat layer
    """

    def __init__(self):
        super().__init__([])

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """
        :param mg.Tensor X: The tensor that will be flattened
        :return mg.Tensor: A flat tensor

        Takes an input of shape (N, C, H, W) and flattens it
        to a shape of (N, C*H*W).
        """

        # The first dimension (batch size, N) is preserved.
        # The rest of the dimensions are flattened.

        return X.reshape(X.data.shape[0], -1)

    def output_shape(self, prev_shape: Tuple[int] = ()) -> Tuple[int]:
        return (np.array(prev_shape)[0:].prod(),)


class MaxPooling2D(Layer):
    """
    :param int | Tuple[int, int] pool_size: the pool size can be integer for square
        pools and can be a tuple for rectangular tuples

    A layer to perform max pooling over a 4D input (No_samples, Channels, Height, Width).
    """

    def __init__(self, pool_size, stride=None):
        self.populate_self(locals())
        super().__init__([])
        if isinstance(pool_size, int):
            self.pool_size = (pool_size, pool_size)
        else:
            self.pool_size = pool_size

        # If stride is not specified, it defaults to the pool_size
        if stride is None:
            self.stride = self.pool_size
        elif isinstance(stride, int):
            self.stride = (stride, stride)
        else:
            self.stride = stride

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """
        Applies the max pooling operation.
        """
        return _max_pool(X, self.pool_size, self.stride)


class LSTMCell(Layer):
    """
    A single cell of an LSTM. Performs the computation for one timestep.
    """

    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # The input to the gates is the concatenation of the previous hidden state
        # and the current input, so its size is hidden_size + input_size.
        concat_size = hidden_size + input_size

        # We create one large weight matrix for all 4 gates (input, forget, candidate, output)
        self.weights_all = mg.tensor(
            np.random.randn(concat_size, 4 * hidden_size) *
            np.sqrt(2. / concat_size), dtype=mg.float32)

        # We also create one large bias vector for all 4 gates.
        self.bias_all = mg.tensor(
            np.zeros((1, 4 * hidden_size)), dtype=mg.float32)
        # A common practice is to initialize the forget gate bias to 1.0 to encourage remembering.
        self.bias_all.data[:, hidden_size: 2 * hidden_size] = 1.0

        super().__init__([self.weights_all, self.bias_all])

    def forward(self, x_t: mg.Tensor, h_prev: mg.Tensor, C_prev: mg.Tensor):
        """
        Performs a forward pass for a single timestep.


        :param x_t (mg.Tensor): Input for the current timestep, shape (N, input_size).
        :param h_prev (mg.Tensor): Hidden state from the previous timestep, shape (N, hidden_size).
        :param C_prev (mg.Tensor): Cell state from the previous timestep, shape (N, hidden_size).

        :return Tuple[mg.Tensor, mg.Tensor]: The new hidden state (h_next) and cell state (C_next).
        """
        # Concatenate previous hidden state and current input
        concat_input = mg.concatenate([h_prev, x_t], axis=1)

        # Perform a single matrix multiplication for all gates
        gate_calcs = mg.matmul(concat_input, self.weights_all) + self.bias_all

        # This is the correct and idiomatic way in MyGrad.
        hs = self.hidden_size
        f_calc = gate_calcs[:, :hs]
        i_calc = gate_calcs[:, hs: 2 * hs]
        g_calc = gate_calcs[:, 2 * hs: 3 * hs]
        o_calc = gate_calcs[:, 3 * hs:]  # Slicing to the end is robust

        # Apply activation functions to each gate
        f_t = activations.sigmoid(f_calc)
        i_t = activations.sigmoid(i_calc)
        g_t = activations.tanh(g_calc)
        o_t = activations.sigmoid(o_calc)

        # Calculate the new cell state and hidden state
        C_next = (f_t * C_prev) + (i_t * g_t)
        h_next = o_t * activations.tanh(C_next)

        return h_next, C_next


class LSTMLayer(Layer):
    """
    An LSTM layer that processes a sequence of inputs by unrolling an LSTMCell
    over time.
    """

    def __init__(self, input_size: int, hidden_size: int, return_sequences: bool = True):
        self.hidden_size = hidden_size
        self.return_sequences = return_sequences

        # The LSTM layer contains a cell that holds the parameters
        self.cell = LSTMCell(input_size, hidden_size)

        # Expose the cell's parameters as the layer's parameters for the optimizer
        self.weights = self.cell.weights_all
        self.bias = self.cell.bias_all
        # LSTM layer doesn't need its own use_bias attribute, it's handled by the cell
        self.use_bias = True
        super().__init__([self.weights, self.bias])

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """
        Processes a sequence of inputs.

        :param mg.Tensor X: The input sequence, shape (N, seq_len, input_size).
        :return mg.Tensor: The sequence of hidden states, shape (N, seq_len, hidden_size),
                       or the final hidden state, shape (N, hidden_size).
        """
        batch_size, seq_len, _ = X.shape

        # Initialize hidden state and cell state with zeros
        h_prev = mg.tensor(
            np.zeros((batch_size, self.hidden_size)), dtype=mg.float32)
        C_prev = mg.tensor(
            np.zeros((batch_size, self.hidden_size)), dtype=mg.float32)

        # List to store the hidden states from each timestep
        outputs = []

        # Unroll the cell over the time dimension (seq_len)
        for t in range(seq_len):
            # Get the input for the current timestep
            x_t = X[:, t, :]

            # Run the cell
            h_next, C_next = self.cell.forward(x_t, h_prev, C_prev)

            # Store the output hidden state
            outputs.append(h_next)

            # Update states for the next iteration
            h_prev, C_prev = h_next, C_next

        if self.return_sequences:
            # Stack all hidden states to create a single output tensor
            # We need to reshape each h_next to (N, 1, hidden_size) before concatenating
            reshaped_outputs = [out.reshape(
                batch_size, 1, self.hidden_size) for out in outputs]
            return mg.concatenate(reshaped_outputs, axis=1)
        else:
            return outputs[-1]


class Embedding(Layer):
    """
    Word embedding layer

    :param int vocab_size: The size of vocabulary
    :param int dim: the number of output dimensions
    """

    def __init__(self, vocab_size, dim) -> None:
        self.vocab_size = vocab_size
        self.dim = dim

        self.weight = mg.tensor((np.random.rand(vocab_size, dim) - 0.5) / dim,
                                constant=False)

        super().__init__([self.weight])

    def forward(self, X: mg.Tensor):
        return self.weight[X]


class InputShape(Layer):
    """
    A very simple layer designed just for model designing
    where you might need in order to determine the model shapes and
    it can make sure the input shape is correct where it the shape of data is
    (X, D1, D2, D3, ... ) where it ignores the the first dimension because it is
    the number of samples.
    """

    def __init__(self, shape: Tuple[int],
                 ensure_shape: Optional[bool] = True) -> None:
        self.shape = tuple(shape)
        self.ensure_shape = ensure_shape
        super().__init__([])

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """Just returns the inputs"""
        if self.ensure_shape and self.shape != X.shape[1:]:
            raise ValueError(f"The input shape of {X.shape} doesn't match "
                             f"the desired {self.shape}")
        return X

    def output_shape(self, prev_shape: Optional[Tuple[int]] = None) -> Tuple[int]:
        """returns the input shape of layers"""
        return self.shape


class Dropout(Layer):
    """
    A dropout layer

    :param float proba: The percentage of inactive neurons
    """

    def __init__(self, proba: float) -> None:
        self.proba = proba
        super().__init__([])

    def forward(self, X):
        keep_proba = 1 - self.proba
        mask = np.random.binomial(1, keep_proba, size=X.data.shape)
        # The division scales up the active neurons to compensate for the dropped ones
        return (X * mask) / keep_proba

    def predict(self, X):
        """
        In the method :class:`helixnet.layers.Dropout.predict`
        the :class:`helixnet.layers.Dropout` won't perform the dropout and
        pass the inputs directly.
        """
        return X


class BatchNorm(Layer):
    """
    Performs batch normalization.

    :param Tuple[int] input_shape: The shape of the input of the data
    :param float momentum: The momentum of the layer
    :param float epsilon: A simple number for numerical stability
    """

    def __init__(self, input_shape: Tuple[int], momentum=0.99, epsilon=1e-7):
        self.weight = mg.tensor(np.random.randn(*input_shape))
        self.bias = mg.tensor(np.random.randn(*input_shape[1:]))
        super().__init__([self.weight, self.bias])

        self.momentum = momentum
        self.epsilon = epsilon

        self.running_mean = np.zeros(input_shape)
        self.running_var = np.ones(input_shape)
        self.populate_self(locals())

    def forward(self, X) -> mg.Tensor:
        # During training, use batch statistics
        batch_mean = mg.mean(X, axis=0)
        batch_var = mg.var(X, axis=0)

        # Update running averages
        self.running_mean = self.momentum * self.running_mean + \
            (1 - self.momentum) * batch_mean.data
        self.running_var = self.momentum * self.running_var + \
            (1 - self.momentum) * batch_var.data

        # Normalize with batch statistics
        normalized_x = (X - batch_mean) / mg.sqrt(batch_var + self.epsilon)

        return self.weight * normalized_x + self.bias

    def predict(self, X, *args, **kwargs) -> mg.Tensor:
        """
        Normalize the data without updating the running mean and variance

        :param mg.Tensor X: The input of the data
        """
        normalized_x = (X - self.running_mean) / \
            mg.sqrt(self.running_var + self.epsilon)
        return self.weight * normalized_x + self.bias


class DenseTranspose(Layer):
    """
    This layer can be used to tie the weights only of a dense layer useful in autoencoders

    This layer doesn't tie the bias and can create it's own or not

    :param Dense layer: The layer that its weights will be tied.
    :param activation: The activation function that will be used by the layer. But if it's ``none`` it
        will use the tied layer's activation function.
    :param bool use_bias: If you want the layer to created it's own bias.
    """

    def __init__(self, layer: Dense, activation=None, use_bias=None):
        self.weight = layer.weights.T
        if use_bias or (use_bias is None and layer.use_bias):
            self.bias = mg.tensor(np.zeros(self.weight.shape[1:]),
                                  constant=False)
            super().__init__([self.bias])
        else:
            self.bias = None
            super().__init__([])
        self.activation = layer.activation if not activation \
            else activation

    def forward(self, X) -> mg.Tensor:
        return self.activation(X @ self.weight + self.bias) if self.bias \
            is not None else self.activation(X @ self.weight)

    def output_shape(self, prev_shape: Optional[Tuple[int]] = ()) -> Tuple[int]:
        return self.weight.shape[1:]
    # TODO: Check a better implementation


def upsample_zero_insert(x, scale):
    h, w = x.shape
    up = np.zeros((h * scale, w * scale), dtype=x.dtype)
    up[::scale, ::scale] = x
    return up


class ConvTranspose2D(Layer):
    """
    Performs a 2D transpose convolution (deconvolution), used for upsampling.
    This implementation works by first upsampling the input with zero-insertion,
    and then performing a standard convolution.
    """

    def __init__(self, input_channels: int, output_channels: int, kernel_size,
                 stride=1, activation=None, use_bias: bool = True):

        self.populate_self(locals())
        if isinstance(kernel_size, int):
            self.kernel_size = (kernel_size, kernel_size)
        else:
            self.kernel_size = kernel_size

        # The weight shape for the underlying conv_nd MUST be (C_out, C_in, K, K)
        # We are essentially "tricking" a regular convolution into being a transpose one.
        weight_shape = (input_channels, output_channels, *self.kernel_size)
        self.weights = mg.tensor(
            np.random.randn(*weight_shape) * np.sqrt(2. / (input_channels * self.kernel_size[0] * self.kernel_size[1]))
        )

        self.stride = stride if isinstance(stride, int) else stride[0]
        self.activation = activation if activation is not None else (lambda x: x)
        self.use_bias = use_bias

        if self.use_bias:
            self.bias = mg.tensor(np.zeros(output_channels))
            super().__init__([self.weights, self.bias])
        else:
            self.bias = None
            super().__init__([self.weights])

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        """ Performs the transpose convolution using a two-step process. """
        # Step 1: Upsample the input by inserting zeros
        if self.stride > 1:
            N, C, H, W = X.shape
            # For a stride of 2, we want one zero between each element.
            H_up, W_up = (H - 1) * self.stride + 1, (W - 1) * self.stride + 1
            upsampled_data = np.zeros((N, C, H_up, W_up), dtype=X.dtype)
            upsampled_data[:, :, ::self.stride, ::self.stride] = X.data
            X_upsampled = mg.tensor(upsampled_data)
        else:
            X_upsampled = X

        # Step 2: Perform a "full" convolution on the upsampled data
        padding = self.kernel_size[0] - 1

        # We need to swap the input/output channels for the convolution's weights
        # to correctly perform the transpose operation.
        # So we transpose the first two axes of the weights.
        transposed_weights = self.weights.transpose(1, 0, 2, 3)

        conv_result = nnet.conv_nd(X_upsampled, transposed_weights, stride=1, padding=padding)

        if self.use_bias:
            conv_result += self.bias.reshape(1, -1, 1, 1)

        return self.activation(conv_result)


class Reshape(Layer):
    """Reshapes the input tensor to the specified shape.

    :param tuple[int] target_shape: The shape you want the data to be converted to."""

    def __init__(self, target_shape):
        # target_shape does not include the batch dimension (N)
        self.target_shape = target_shape
        super().__init__([])

    def forward(self, X: mg.Tensor) -> mg.Tensor:
        # The -1 in reshape is a placeholder for the batch size (N)
        return X.reshape(-1, *self.target_shape)

    def output_shape(self, prev_shape: Optional[Tuple[int]] = ()) -> Tuple[int]:
        return self.target_shape
