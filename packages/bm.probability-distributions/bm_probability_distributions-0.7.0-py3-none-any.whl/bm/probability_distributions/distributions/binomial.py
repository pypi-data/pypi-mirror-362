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

"""
Binomial Distribution
---------------------

A binomial distribution class, derived from a Udacity
exercise template.

"""

from __future__ import annotations

from typing import Callable, Never
from math import comb, sqrt
import matplotlib.pyplot as plt
from ..datasets import DataSet
from ..distribution import DiscreteDist

__all__ = ['Binomial']


class Binomial(DiscreteDist):
    """Class for visualizing data as Binomial distributions.

    The binomial distribution represents the number of events with
    probability ``p`` happening in ``n`` numbers of trials.

    Attributes (some inherited):

    - ``mean`` (float) representing the mean value of the distribution
    - ``stdev`` (float) representing the standard deviation of the distribution
    - ``data``  extracted from a data file (taken to be a population)
    - ``p`` (float) representing the probability of an event occurring
    - ``n`` (int) the total number of trials

    """

    def __init__(self, p: float = 0.5, n: int = 20):
        if not (0.0 <= p <= 1.0) or n < 1:
            msg1 = 'For a binomial distribution, '
            msg2 = msg3 = ''
            if not (0.0 <= p <= 1.0):
                msg2 = '0 <= p <= 1'
            if n < 0:
                msg3 = 'the number of trials n must be non-negative'
            if msg2 and msg3:
                msg = msg1 + msg2 + ' and ' + msg3 + '.'
            else:
                msg = msg1 + msg2 + msg3 + '.'
            raise ValueError(msg)

        self.p: float = p
        self.n: int = n

        super().__init__()

    def pdf(self, kf: float) -> float:
        """Binomial probability distribution function."""
        k = int(kf)
        n = self.n
        p = self.p
        return comb(n, k) * (p**k) * (1 - p) ** (n - k)

    def cdf(self, kf: float) -> float:
        """Binomial cumulative probability distribution function."""
        return sum((self.pdf(ii) for ii in range(int(kf))))

    def calculate_mean(self) -> float:
        """Calculate the mean from p and n"""
        n = self.n
        p = self.p
        self.mean = mean = n * p
        return mean

    def calculate_stdev(self) -> float:
        """Calculate the standard deviation using p and n"""
        n = self.n
        p = self.p
        self.stdev = stdev = sqrt(n * p * (1 - p))
        return stdev

    def replace_stats_from_dataset(self, dset: DataSet) -> tuple[float, int]:
        """Function to calculate p and n from a data set.

        Where the read in data set is taken as the population.
        """
        if dset:
            self.n = n = dset._size
            self.p = p = sum(dset._data) / n
            self.mean = n * p
            self.stdev = sqrt(n * p * (1 - p))
        return self.p, self.n

    def plot_bar_data(self) -> None:
        """Produce a bar-graph of the data using the matplotlib pyplot library."""
        n = self.n
        p = self.p

        fig, axis = plt.subplots()
        axis.bar(('0', '1'), (n * (1 - p), n * p), color='maroon', width=0.6)
        axis.set_title('Failures and Successes for a sample of {}'.format(n))
        axis.set_xlabel('prob = {}, n = {}'.format(p, n))
        axis.set_ylabel('Sample Count')
        plt.show()

    def plot_bar_pdf(self) -> tuple[list[int], list[float]]:
        """Function to plot the pdf of the binomial distribution.

        :return:
            A tuple containing

            - list[int]: x values used for the pdf plot
            - list[float]: y values used for the pdf plot

        """

        def pdf(ii: int) -> float:
            return self.pdf(float(ii))

        xs: list[int] = list(range(self.n + 1))
        ys: list[float] = list(map(pdf, range(self.n + 1)))

        plt.bar(list(str(x) for x in xs), ys, color='maroon', width=0.4)
        plt.title('Probability Density of Success')
        plt.xlabel('Successes for {} trials'.format(self.n))
        plt.ylabel('Probability')
        plt.show()

        return xs, ys

    def __add__(self, other: Binomial) -> Binomial | Never:
        """Add together two Binomial distributions with equal p."""
        if type(other) is not Binomial:
            msg = 'A binomial distribution cannot be added to a {}'
            msg = msg.format(type(other))
            raise TypeError(msg)
        if self.p != other.p:
            msg = 'p values are not equal'
            raise ValueError(msg)

        return Binomial(self.p, self.n + other.n)

    def __repr__(self) -> str:
        repr_str = 'Binomial({}, {})'
        return repr_str.format(self.p, self.n)

    def __str__(self) -> str:
        user_str = 'mean {}, standard deviation {}, p {}, n {}'
        return user_str.format(self.mean, self.stdev, self.p, self.n)
