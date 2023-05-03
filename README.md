# JART v1b physically derived memristive model with IBM aihwkit
This repository contains the original code described in the paper ["Integration of Physics-Derived Memristor Models with Machine Learning Frameworks"](https://ieeexplore.ieee.org/document/10052010) by Z. Yu, S. Menzel, J. P. Strachan, and E. Neftci, published at the 2022 56th Asilomar Conference on Signals, Systems, and Computers, and will produce the same results published in the paper.

The code is built on IBM aihwkit version 0.6.0 and we are currently working on upstreaming it with offitial IBM aihwkit branch, which can be tracked in the following link: https://github.com/IBM/aihwkit/pull/501.


## Issues
The current code version has some issues with CUDA compatibility.
1. The results calculated to CUDA are having problems transfering back into PyTorch. Adding a [slight delay](https://github.com/ZhenmingYu/aihwkit/blob/JART_v1b_device/src/rpucuda/cuda/rpucuda_JART_v1b_device.cu#L271-L272) can solve this issue, but siginificantly damaged the proformance.
2. The CUDA currently doesn't support cycle to cycle veribility, as this requires more device-specific parameters than aihwkit framework can support.

## Running the experiments
To run and plot the experiments, as well as to access the configuration files, please refer to the [JART_v1b_tests](https://github.com/ZhenmingYu/aihwkit/tree/JART_v1b_device/JART_v1b_tests) directory. 