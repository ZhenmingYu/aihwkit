# IBM Analog Hardware Acceleration Kit

[![Documentation Status](https://readthedocs.org/projects/aihwkit/badge/?version=latest)](https://aihwkit.readthedocs.io/en/latest/?badge=latest)

## Description

_IBM Analog Hardware Acceleration Kit_ is an open source Python toolkit for
exploring and using the capabilities of in-memory computing devices in the
context of artificial intelligence.

> :warning: This library is currently in beta and under active development.
> Please be mindful of potential issues and keep an eye for improvements,
> new features and bug fixes in upcoming versions.

The toolkit consists of two main components:

### Pytorch integration

A series of primitives and features that allow using the toolkit within
[`Pytorch`]:

* Analog neural network modules (fully connected layer, convolution layer).
* Analog optimizers (SGD).

### Analog devices simulator

A high-performant (CUDA-capable) C++ simulator that allows for
simulating a wide range of analog devices and crossbar configurations
by using abstract functional models of material characteristics with
adjustable parameters. Feature include:

* Forward pass output-referred noise and device fluctuations, as well
  as adjustable ADC and DAC discretization and bounds
* Stochastic update pulse trains for rows and columns with finite
  weight update size per pulse coincidence 
* Device-to-device systematic variations, cycle-to-cycle noise and 
  adjustable asymmetry during analog update 
* Adjustable device behavior for exploration of material specifications for
  training and inference
* State-of-the-art dynamic input scaling, bound management, and update
  management schemes

## Example

### Training example

```python
from torch import Tensor
from torch.nn.functional import mse_loss

# Import the aihwkit constructs.
from aihwkit.nn import AnalogLinear
from aihwkit.optim.analog_sgd import AnalogSGD

x = Tensor([[0.1, 0.2, 0.4, 0.3], [0.2, 0.1, 0.1, 0.3]])
y = Tensor([[1.0, 0.5], [0.7, 0.3]])

# Define a network using a single Analog layer.
model = AnalogLinear(4, 2)

# Use the analog-aware stochastic gradient descent optimizer.
opt = AnalogSGD(model.parameters(), lr=0.1)
opt.regroup_param_groups(model)

# Train the network.
for epoch in range(10):
    pred = model(x)
    loss = mse_loss(pred, y)
    loss.backward()

    opt.step()
    print('Loss error: {:.16f}'.format(loss))
```

You can find more examples in the [`examples/`] folder of the project, and
more information about the library in the [documentation].

## What is Analog AI?

In traditional hardware architecture, computation and memory are siloed in
different locations. Information is moved back and forth between computation
and memory units every time an operation is performed, creating a limitation
called the [von Neumann bottleneck].

Analog AI delivers radical performance improvements by combining compute and
memory in a single device, eliminating the von Neumann bottleneck. By leveraging
the physical properties of memory devices, computation happens at the same place
where the data is stored. Such in-memory computing hardware increases the speed 
and energy-efficiency needed for the next generation of AI. 

## What is an in-memory computing chip?

An in-memory computing chip typically consists of multiple arrays of memory
devices that communicate with each other. Many types of memory devices such as
[phase-change memory] (PCM), [resistive random-access memory] (RRAM), and
[Flash memory] can be used for in-memory computing. 

Memory devices have the ability to store synaptic weights in their analog
charge (Flash) or conductance (PCM, RRAM) state. When these devices are arranged
in a crossbar configuration, it allows to perform an analog matrix-vector
multiplication in a single time step, exploiting the advantages of analog
storage capability and [Kirchhoff’s circuits laws]. You can learn more about
it in our [online demo].
 
In deep learning, data propagation through multiple layers of a neural network
involves a sequence of matrix multiplications, as each layer can be represented
as a matrix of synaptic weights. The devices are arranged in multiple crossbar
arrays, creating an artificial neural network where all matrix multiplications
are performed in-place in an analog manner. This structure allows to run deep
learning models at reduced energy consumption. 

## Installation

### Installing from PyPI

The preferred way to install this package is by using the
[Python package index]:

```bash
$ pip install aihwkit
```

The packages require the following runtime libraries to be installed in your
system:

| Dependency  | Version | Notes |
| --- | --- | --- |
| [`OpenBLAS`] | 0.3.3+ | |
| [`CUDA Toolkit`] | 9.0+ | For GPU-enabled simulator |

Note that we provide pre-built packages for specific combinations of
architectures and versions, and in some cases a pre-built package might still
not be available. Please check the following section for more information on
how to build your own package.

### Installing from source

The following commands will download the latest sources and install the
package from source:

```bash
$ git clone https://github.com/IBM/aihwkit.git
$ cd aihwkit
$ python setup.py install
```

Note that additional libraries and tools are required, as compilation of the
sources is involved. The build system is based on `cmake` and has a number of
options. Please check the [developer guide] for more information.

## Authors

IBM Analog Hardware Acceleration Kit has been developed by IBM Research,
with Tayfun Gokmen, Manuel Le Gallo-Bourdeau, Malte Rasch and Diego Moreda
as the initial core authors, along with many [contributors].

You can contact us by opening a new issue in the repository, or alternatively
at the ``aihwkit@us.ibm.com`` email.

## License

This project is licensed under [Apache License 2.0].

[Apache License 2.0]: LICENSE.txt
[`CUDA Toolkit`]: https://developer.nvidia.com/accelerated-computing-toolkit
[developer guide]: docs/source/developer_guide.rst
[`OpenBLAS`]: https://www.openblas.net/
[Python package index]: https://pypi.org/project/aihwkit
[`Pytorch`]: https://pytorch.org/

[`examples/`]: examples/
[documentation]: https://aihwkit.readthedocs.io/
[contributors]: https://github.com/IBM/aihwkit/graphs/contributors

[von Neumann bottleneck]: https://en.wikipedia.org/wiki/Von_Neumann_architecture#Von_Neumann_bottleneck
[phase-change memory]: https://en.wikipedia.org/wiki/Phase-change_memory
[resistive random-access memory]: https://en.wikipedia.org/wiki/Resistive_random-access_memory
[Flash memory]: https://en.wikipedia.org/wiki/Flash_memory
[Kirchhoff’s circuits laws]: https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws
[online demo]: https://analog-ai-demo.mybluemix.net/
