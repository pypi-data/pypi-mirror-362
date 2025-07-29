# Copyright 2024 Geoffrey R. Scheller
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

"""Module bm.probability_distributions.distribution

Providing base classes to visualize probability distributions.

- *class* ContDist: base class to visualize continuous pd
- *class* DiscreteDist: base class to visualize discrete pd

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, Never
import matplotlib.pyplot as plt
from .datasets import DataSet
from pythonic_fp.containers.maybe import MayBe

__all__ = ['ContDist', 'DiscreteDist']


class ContDist(ABC):
    """Base class to visualize continuous probability distributions."""

    def __init__(self) -> None:
        self.population: MayBe[DataSet] = MayBe()
        self.samples: list[DataSet] = []

    @abstractmethod
    def pdf(self, kf: float) -> float:
        """Probability distribution function."""
        ...

    @abstractmethod
    def cdf(self, kf: float) -> float:
        """Cumulative distribution function."""
        ...

    @abstractmethod
    def __add__(self, other: Self) -> Self | Never:
        """Add together two compatible distributions."""
        ...


#    def plot_bar_data(self) -> None: ...

#    def barplot_pdf(self) -> tuple[list[int], List[float]]:
#        """Function to plot the pdf of the binomial distribution.
#
#        Returns:
#            list: x values used for the pdf plot
#            list: y values used for the pdf plot
#        """
#        pdf: Callable[[int], float] = lambda ii: self.pdf(float(ii))
#
#        xs: list[int] = list(range(self.n + 1))
#        ys: list[float] = list(map(pdf, range(self.n + 1)))
#
#        plt.bar(list(str(x) for x in xs), ys, color ='maroon', width = 0.4)
#        plt.title('Probability Density of Success')
#        plt.xlabel('Successes for {} trials'.format(self.n))
#        plt.ylabel('Probability')
#        plt.show()
#
#        return xs, ys


class DiscreteDist(ABC):
    """Base class to visualize discrete probability distributions."""

    def __init__(self) -> None:
        self.population: MayBe[DataSet] = MayBe()
        self.samples: list[DataSet] = []

    @abstractmethod
    def pdf(self, kf: float) -> float:
        """Probability distribution function."""
        ...

    @abstractmethod
    def cdf(self, kf: float) -> float:
        """Cumulative distribution function."""
        ...

    @abstractmethod
    def __add__(self, other: Self) -> Self | Never:
        """Add together two compatible distributions."""
        ...
