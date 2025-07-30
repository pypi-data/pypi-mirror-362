#!/usr/bin/env python
# ******************************************************************************
# Copyright 2025 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ['export_to_onnx']

import torch
import warnings


def export_to_onnx(model, input_shape, out_path='model.onnx'):
    """ Exports a PyTorch model to ONNX format, and saves the optimized ONNX model
    to a specified file.

    Args:
        model (torch.nn.Module): The input PyTorch model to be converted.
        input_shape (tuple): The shape of the input tensor for the model.
        out_path (str, optional): The output file path for the ONNX model. Defaults to 'model.onnx'.

    """
    # if the batch_size = 1, the exported model will have a static batch_size
    # due to a bug in torch.onnx.export, else the batch_size will be dynamic.
    if input_shape[0] == 1:
        warnings.warn('Exported model with batch_size = 1 will have a static batch_size.')

    inputs = torch.rand(size=input_shape, dtype=torch.float32).to("cpu")

    with torch.inference_mode():
        torch.onnx.export(model, inputs, out_path,
                          input_names=["input"], opset_version=15,
                          dynamo=True, external_data=False, optimize=True,
                          dynamic_shapes={
                              "input": {0: torch.export.Dim("batch_size")}
                          })
        print(f'Model exported to {out_path}.')
