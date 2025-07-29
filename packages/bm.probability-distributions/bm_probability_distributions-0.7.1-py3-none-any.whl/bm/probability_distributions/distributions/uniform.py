# Copyright 2024-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This module contains software derived from Udacity® exercises.
# Udacity® (https://www.udacity.com/)
#

from __future__ import annotations

from typing import Never
from math import sqrt
import matplotlib.pyplot as plt
from ..datasets import DataSet
from ..distribution import ContDist

__all__ = ['Uniform']


class Uniform(ContDist):
    """Class for visualizing Normal distributions.

    .. note::
        The Uniform distribution is a continuous probability
        distribution with probability density function

           f(x) = 1/(b-a)  for a < x < b
           f(x) = 0        otherwise
        where
          μ = mu = (a+b)/2 = mean value
          σ = sigma = (b-a)/2√3 = standard deviation

    """

    def __init__(self, a: float = 0.0, b: float = 1.0):
        if b <= a:
            msg = 'For a Uniorm distribution, b > a'
            raise ValueError(msg)

        self.mu = (a + b) / 2
        self.sigma = (b - a) / (2 * sqrt(3))
        self.a = a
        self.b = b

        super().__init__()

    def __repr__(self) -> str:
        repr_str = 'mean {}, standard deviation {}'
        return repr_str.format(self.mu, self.sigma)

    def pdf(self, x: float) -> float:
        """Uniform probability distribution function."""
        a = self.a
        b = self.b
        c = 1.0 / (b - a)
        if a < x < b:
            return c
        else:
            return 0

    def cdf(self, x: float) -> float:
        """Uniform cumulative probability distribution function."""
        a = self.a
        b = self.b
        c = 1.0 / (b - a)
        if x <= a:
            return 0
        elif x < b:
            return c * (x - a)
        else:
            return 1

    def __add__(self, other: Uniform) -> Uniform | Never:
        """Add together two compatible Uniform distributions."""
        if type(other) is not Uniform:
            msg = 'A Uniform distribution cannot be added to a {}'
            msg = msg.format(type(other))
            raise TypeError(msg)

        if other.a <= self.a <= other.b:
            a = other.a
            b = max(self.b, other.b)
        elif self.a <= other.a <= self.b:
            a = self.a
            b = max(self.b, other.b)
        else:
            msg = 'Intervals of Uniform distributions must overlap'
            raise ValueError(msg)

        return Uniform(b, a)
