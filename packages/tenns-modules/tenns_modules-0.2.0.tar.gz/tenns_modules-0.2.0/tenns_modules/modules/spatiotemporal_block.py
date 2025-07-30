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

__all__ = ['SpatialBlock', 'TemporalBlock', 'SpatioTemporalBlock', 'PleiadesLayer']

import torch
import numpy as np
from torch import nn
from torch.nn import functional as F
from scipy.special import jacobi


def _set_attributes(obj, local_vars):
    # Automatically set attributes in obj with local_vars names
    for name, value in local_vars.items():
        if name != 'self':
            setattr(obj, name, value)


class SpatialBlock(nn.Module):
    """ A spatial (potentially separable) convolution.

    BatchNormalization and ReLU activation are included in this block.

    Args:
        in_channels (int): number of channels in the input
        out_channels (int): number of channels produced by the block
        kernel_size (int): size of the kernel
        stride (int, optional): stride of the convolution. Defaults to 1.
        bias (bool, optional): if True, adds a learnable bias to the output. Defaults to True.
        depthwise (bool, optional): if True, the block will be separable. Defaults to False.
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, bias=True,
                 depthwise=False):
        super().__init__()
        _set_attributes(self, locals())

        if stride not in [1, 2]:
            raise ValueError(
                f"Invalid stride: {stride} for SpatialBlock. Only 1 or 2 are allowed.")
        valid_kernel_size = [3, 5, 7]
        if not depthwise:
            valid_kernel_size += [1]
        if kernel_size not in valid_kernel_size:
            raise ValueError(
                f"Invalid kernel_size: {kernel_size} for SpatialBlock. "
                f"Must be in {valid_kernel_size}.")
        if stride == 2 and kernel_size != 3:
            raise ValueError(
                f"When stride is 2, kernel_size must be 3 in SpatialBlock "
                f"(got {kernel_size}).")

        kernel = (1, self.kernel_size, self.kernel_size)
        strides = (1, self.stride, self.stride)
        if stride == 2:
            padding_layer = nn.ZeroPad3d(padding=(0, 1, 0, 1, 0, 0))
        else:
            padding_layer = nn.ZeroPad3d(padding=(self.kernel_size // 2, self.kernel_size // 2,
                                                  self.kernel_size // 2, self.kernel_size // 2,
                                                  0, 0))
        if not depthwise:
            self.block = nn.Sequential(
                padding_layer,
                nn.Conv3d(in_channels, out_channels, kernel, strides, bias=bias),
                nn.BatchNorm3d(out_channels),
                nn.ReLU())
        else:
            self.block = nn.Sequential(
                padding_layer,
                nn.Conv3d(in_channels, in_channels, kernel, strides,
                          groups=in_channels, bias=False),
                nn.BatchNorm3d(in_channels),
                nn.ReLU(),
                nn.Conv3d(in_channels, out_channels, 1, bias=bias),
                nn.BatchNorm3d(out_channels),
                nn.ReLU()
            )

    def forward(self, input):
        # This is expecting 5D inputs with shape (B, C, T, H, W)
        return self.block(input)


def get_ortho_polynomials(length, degrees=4, alpha=-0.25, beta=-0.25):
    """ Generate the set of Jacobi orthogonal polynomials with shape (degrees + 1, length)

    Args:
        length (int): The length of the discretized temporal kernel,
            assuming the range [0, 1] for the polynomials.
        degrees (int, optional): The maximum polynomial degree. Defaults to 4.
            Note that degrees + 1 polynomials will be generated (counting the constant)
        alpha (int, optional): The alpha Jacobi parameter. Defaults to -0.25
        beta (int, optional): The beta Jacobi parameter. Defaults to -0.25

    Returns:
        np.ndarray: shaped (degrees + 1, length)
    """
    coeffs = np.vstack([np.pad(np.flip(jacobi(degree, alpha, beta).coeffs), (0, degrees - degree))
                        for degree in range(degrees + 1)]).astype(np.float32)
    steps = np.linspace(0, 1, length + 1)
    X = np.stack([steps ** (i + 1) / (i + 1) for i in range(degrees + 1)])
    polynomials_integrated = coeffs @ X
    transform = np.diff(polynomials_integrated, 1, -1) * length
    return transform


class PleiadesLayer(nn.Conv3d):
    """ A 3D convolutional layer utilizing orthogonal polynomials for kernel transformation.

    Args:
        *args: Positional arguments passed to `torch.nn.Conv3d`.
        degrees (int, optional): Degree of the orthogonal polynomials. Defaults to 4.
        alpha (float, optional): Alpha parameter for the orthogonal polynomials. Defaults to -0.25.
        beta (float, optional): Beta parameter for the orthogonal polynomials. Defaults to -0.25.
        **kwargs: Keyword arguments passed to `torch.nn.Conv3d`.
    """

    def __init__(self, *args, degrees=4, alpha=-0.25, beta=-0.25, **kwargs):
        super().__init__(*args, **kwargs)
        transform = get_ortho_polynomials(self.kernel_size[0], degrees=degrees, alpha=alpha,
                                          beta=beta)
        transform = torch.tensor(transform).float()
        scale = (self.weight.shape[1] ** 0.5) * (self.kernel_size[0] ** 0.5)
        transform = transform / scale

        self.transform = nn.Parameter(transform, requires_grad=False)
        self.weight = nn.Parameter(torch.rand(self.out_channels, self.weight.shape[1],
                                              *self.kernel_size[1:], degrees + 1))

    def forward(self, input):
        # Perform matrix multiplication between the weight tensor and the transform matrix.
        # Shapes:
        # self.weight: (out_channels, in_channels, kernel_height, kernel_width, degrees + 1)
        # self.transform: (degrees + 1, kernel_depth)
        # Resulting kernel shape after multiplication: (out_channels, in_channels, kernel_height,
        #                                               kernel_width, kernel_depth)
        kernel = torch.matmul(self.weight, self.transform)
        # Transpose the kernel tensor to match the expected input shape for F.conv3d.
        # Resulting kernel shape after transpose: (out_channels, in_channels, kernel_depth,
        #                                          kernel_height, kernel_width)
        kernel = torch.permute(kernel, (0, 1, 4, 2, 3))
        return F.conv3d(input, kernel,
                        bias=self.bias, groups=self.groups,
                        stride=self.stride, padding=self.padding,
                        dilation=self.dilation)


class TemporalBlock(nn.Module):
    """ A temporal (potentially separable) convolution.

    BatchNormalization and ReLU activation are included in this block.

    Args:
        in_channels (int): number of channels in the input
        out_channels (int): number of channels produced by the block
        kernel_size (int): size of the kernel
        bias (bool, optional): if True, adds a learnable bias to the output. Defaults to True.
        depthwise (bool, optional): if True, the block will be separable. Defaults to False.
        use_pleiades (bool, optional): if True, the first conv3d is a PleiadesLayer. Defaults to
            False.

    """

    def __init__(self, in_channels, out_channels, kernel_size, bias=True, depthwise=False,
                 use_pleiades=False):
        super().__init__()
        _set_attributes(self, locals())

        if kernel_size not in range(2, 11):
            raise ValueError(f"Invalid kernel_size: {kernel_size} for TemporalBlock. "
                             "Must be in [2:10].")

        kernel = (self.kernel_size, 1, 1)

        if use_pleiades:
            layer_constructor = PleiadesLayer
        else:
            layer_constructor = nn.Conv3d

        if not depthwise:
            self.block = nn.Sequential(
                layer_constructor(in_channels, out_channels, kernel, bias=bias),
                nn.BatchNorm3d(out_channels),
                nn.ReLU()
            )
        else:
            self.block = nn.Sequential(
                layer_constructor(in_channels, in_channels, kernel, groups=in_channels, bias=False),
                nn.BatchNorm3d(in_channels),
                nn.ReLU(),
                nn.Conv3d(in_channels, out_channels, 1, bias=bias),
                nn.BatchNorm3d(out_channels),
                nn.ReLU()
            )

    def forward(self, input):
        # This is expecting 5D inputs with shape (B, C, T, H, W)
        input = F.pad(input, (0, 0, 0, 0, self.kernel_size - 1, 0))
        return self.block(input)


class SpatioTemporalBlock(nn.Module):
    """ A combination of temporal and spatial convolutions.

    This first applies a temporal convolution (potentially separable) to process the input over the
    temporal dimension, followed by a spatial convolution (potentially separable) to process the
    output over the spatial dimension.

    Args:
        in_channels (int): input channels
        med_channels (int): intermediate channels between blocks
        out_channels (int): output channels
        t_kernel_size (int): size of the TemporalBlock kernel
        s_kernel_size (int): size of the SpatialBlock kernel
        s_stride (int, optional): stride of the SpatialBlock convolution. Defaults to 1.
        bias (bool, optional): if True, adds a learnable bias to the output. Defaults to True.
        t_depthwise (bool, optional): if True, the TemporalBlock will be separable. Defaults to
            False.
        s_depthwise (bool, optional): if True, the SpatialBlock will be separable. Defaults to
            False.
        temporal_first (bool, optional): if True, the first block is a temporal block.
            Defaults to True.
        use_pleiades (bool, optional): if True, the first conv3d of the TemporalBlock
            is a PleiadesLayer. Defaults to False.
    """

    def __init__(self, in_channels, med_channels, out_channels, t_kernel_size, s_kernel_size,
                 s_stride=1, bias=True, t_depthwise=False, s_depthwise=False,
                 temporal_first=True, use_pleiades=False):
        super().__init__()
        _set_attributes(self, locals())

        if temporal_first:
            self.block = nn.Sequential(
                TemporalBlock(in_channels, med_channels, t_kernel_size, bias, t_depthwise,
                              use_pleiades),
                SpatialBlock(med_channels, out_channels, s_kernel_size, s_stride, bias,
                             s_depthwise),
            )
        else:
            self.block = nn.Sequential(
                SpatialBlock(in_channels, med_channels, s_kernel_size, s_stride, bias,
                             s_depthwise),
                TemporalBlock(med_channels, out_channels, t_kernel_size, bias, t_depthwise,
                              use_pleiades),
            )

    def forward(self, input):
        # This is expecting 5D inputs with shape (B, C, T, H, W)
        return self.block(input)
