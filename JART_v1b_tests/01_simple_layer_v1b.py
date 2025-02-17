# -*- coding: utf-8 -*-

# (C) Copyright 2020, 2021, 2022 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""aihwkit example 1: simple network with one layer.

Simple network that consist of one analog layer. The network aims to learn
to sum all the elements from one array.
"""
# pylint: disable=invalid-name

# Imports from PyTorch.
import torch
from torch import Tensor
from torch.nn.functional import mse_loss

# Imports from aihwkit.
from aihwkit.nn import AnalogLinear
from aihwkit.optim import AnalogSGD
from aihwkit.simulator.configs import SingleRPUConfig
from aihwkit.simulator.configs.devices import JARTv1bDevice
from aihwkit.simulator.rpu_base import cuda

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="YAML Configuration File")
args = parser.parse_args()

if args.config:
    config_file = args.config
else:
    config_file = "noise_free.yml"

split = config_file.split(".")
if len(split) == 2:
    job_type = split[0]
else:
    job_type = config_file

import yaml
stream = open(config_file, "r")
config_dictionary = yaml.safe_load(stream)

project_name = config_dictionary["project_name"]
CUDA_Enabled = config_dictionary["USE_CUDA"]
USE_wandb = config_dictionary["USE_wandb"]
USE_0_initialization= config_dictionary["USE_0_initialization"]
USE_bias= config_dictionary["USE_bias"]
del config_dictionary["USE_0_initialization"]
del config_dictionary["project_name"]
del config_dictionary["USE_wandb"]

if "Repeat_Times" in config_dictionary:
    Repeat_Times = config_dictionary["Repeat_Times"]
    del config_dictionary["Repeat_Times"]
else:
    Repeat_Times = 1

for repeat in range(Repeat_Times):
    if USE_wandb:
        import wandb
        wandb.init(project=project_name, group="Single Layer Perceptron", job_type=job_type)
        wandb.config.update(config_dictionary)

    # Prepare the datasets (input and expected output).
    x = Tensor([[0.1, 0.2, 0.4, 0.3], [0.2, 0.1, 0.1, 0.3]])
    y = Tensor([[1.0, 0.5], [0.7, 0.3]])

    # Define a single-layer network.
    rpu_config = SingleRPUConfig(device=JARTv1bDevice(w_max=config_dictionary["w_max"],
                                                      w_min=config_dictionary["w_min"],

                                                      read_voltage=config_dictionary["pulse_related"]["read_voltage"],
                                                      pulse_voltage_SET=config_dictionary["pulse_related"]["pulse_voltage_SET"],
                                                      pulse_voltage_RESET=config_dictionary["pulse_related"]["pulse_voltage_RESET"],
                                                      pulse_length=config_dictionary["pulse_related"]["pulse_length"],
                                                      base_time_step=config_dictionary["pulse_related"]["base_time_step"],

                                                      enable_w_max_w_min_bounds=config_dictionary["noise"]["enable_w_max_w_min_bounds"],
                                                      w_max_dtod=config_dictionary["noise"]["w_max"]["device_to_device"],
                                                      w_max_dtod_upper_bound=config_dictionary["noise"]["w_max"]["dtod_upper_bound"],
                                                      w_max_dtod_lower_bound=config_dictionary["noise"]["w_max"]["dtod_lower_bound"],
                                                      w_min_dtod=config_dictionary["noise"]["w_min"]["device_to_device"],
                                                      w_min_dtod_upper_bound=config_dictionary["noise"]["w_min"]["dtod_upper_bound"],
                                                      w_min_dtod_lower_bound=config_dictionary["noise"]["w_min"]["dtod_lower_bound"],

                                                      Ndiscmax_dtod=config_dictionary["noise"]["Ndiscmax"]["device_to_device"],
                                                      Ndiscmax_dtod_upper_bound=config_dictionary["noise"]["Ndiscmax"]["dtod_upper_bound"],
                                                      Ndiscmax_dtod_lower_bound=config_dictionary["noise"]["Ndiscmax"]["dtod_lower_bound"],
                                                      Ndiscmax_std=config_dictionary["noise"]["Ndiscmax"]["cycle_to_cycle_direct"],
                                                      Ndiscmax_ctoc_upper_bound=config_dictionary["noise"]["Ndiscmax"]["ctoc_upper_bound"],
                                                      Ndiscmax_ctoc_lower_bound=config_dictionary["noise"]["Ndiscmax"]["ctoc_lower_bound"],

                                                      Ndiscmin_dtod=config_dictionary["noise"]["Ndiscmin"]["device_to_device"],
                                                      Ndiscmin_dtod_upper_bound=config_dictionary["noise"]["Ndiscmin"]["dtod_upper_bound"],
                                                      Ndiscmin_dtod_lower_bound=config_dictionary["noise"]["Ndiscmin"]["dtod_lower_bound"],
                                                      Ndiscmin_std=config_dictionary["noise"]["Ndiscmin"]["cycle_to_cycle_direct"],
                                                      Ndiscmin_ctoc_upper_bound=config_dictionary["noise"]["Ndiscmin"]["ctoc_upper_bound"],
                                                      Ndiscmin_ctoc_lower_bound=config_dictionary["noise"]["Ndiscmin"]["ctoc_lower_bound"],

                                                      ldisc_dtod=config_dictionary["noise"]["ldisc"]["device_to_device"],
                                                      ldisc_dtod_upper_bound=config_dictionary["noise"]["ldisc"]["dtod_upper_bound"],
                                                      ldisc_dtod_lower_bound=config_dictionary["noise"]["ldisc"]["dtod_lower_bound"],
                                                      ldisc_std=config_dictionary["noise"]["ldisc"]["cycle_to_cycle_direct"],
                                                      ldisc_std_slope=config_dictionary["noise"]["ldisc"]["cycle_to_cycle_slope"],
                                                      ldisc_ctoc_upper_bound=config_dictionary["noise"]["ldisc"]["ctoc_upper_bound"],
                                                      ldisc_ctoc_lower_bound=config_dictionary["noise"]["ldisc"]["ctoc_lower_bound"],

                                                      rdisc_dtod=config_dictionary["noise"]["rdisc"]["device_to_device"],
                                                      rdisc_dtod_upper_bound=config_dictionary["noise"]["rdisc"]["dtod_upper_bound"],
                                                      rdisc_dtod_lower_bound=config_dictionary["noise"]["rdisc"]["dtod_lower_bound"],
                                                      rdisc_std=config_dictionary["noise"]["rdisc"]["cycle_to_cycle_direct"],
                                                      rdisc_std_slope=config_dictionary["noise"]["rdisc"]["cycle_to_cycle_slope"],
                                                      rdisc_ctoc_upper_bound=config_dictionary["noise"]["rdisc"]["ctoc_upper_bound"],
                                                      rdisc_ctoc_lower_bound=config_dictionary["noise"]["rdisc"]["ctoc_lower_bound"]))
    model = AnalogLinear(4, 2, bias=True,
                        rpu_config=rpu_config)

    if USE_0_initialization:
        weights, bias = model.get_weights()
        if USE_bias:
            model.set_weights(torch.zeros_like(weights), torch.zeros_like(bias))
        else:
            model.set_weights(torch.zeros_like(weights))

    # Move the model and tensors to cuda if it is available.
    if cuda.is_compiled() & CUDA_Enabled:
        x = x.cuda()
        y = y.cuda()
        model.cuda()

    # Define an analog-aware optimizer, preparing it for using the layers.
    opt = AnalogSGD(model.parameters(), lr=config_dictionary["learning_rate"])
    opt.regroup_param_groups(model)

    for epoch in range(config_dictionary["epochs"]):
        # Add the training Tensor to the model (input).
        pred = model(x)
        # Add the expected output Tensor.
        loss = mse_loss(pred, y)
        if USE_wandb:
            wandb.log({"Loss": loss, "epoch": (epoch+1)})
        else:
            print('Epoch {} - Loss: {:.16f}'.format(
                (epoch+1), loss))
        # Run training (backward propagation).
        loss.backward()

        opt.step()

    if USE_wandb:
        wandb.finish()