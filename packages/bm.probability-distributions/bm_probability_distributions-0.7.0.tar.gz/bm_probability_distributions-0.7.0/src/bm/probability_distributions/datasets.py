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

"""Module for - managing sample/population data

- *class* DataSet: contains sample or population data
- *class* DataSets: base class for managing data sets

"""

from __future__ import annotations

import math
from collections.abc import Iterator
from typing import Never
from pythonic_fp.containers.maybe import MayBe

__all__ = ['DataSet', 'DataSets']


class DataSet:
    """Class containing sample or population data.

    - all data internally stored as floats (even integer data)
    - data sorted smallest to largest
    - methods provided to

      - read in data from a file
      - computing data statistics
      - add or remove data

    """

    @staticmethod
    def read_data_from_file(file_name: str, sample: bool = False) -> MayBe[DataSet]:
        """Read in data from a text file, return a DataSet object.

        The text file should

        - have one number (float) per line and calculate statistics

          - if sample is true (default), calculate sample stats
          - if sample is false, calculate population stats

        - blank lines and lines beginning with '#' are ignored

        """
        data: list[float] = []
        try:
            with open(file_name) as file:
                line = file.readline()
                while line:
                    if line[0] != '#' and line[0] != chr(ord('\n')):
                        data.append(float(line))
                        line = file.readline()
                    else:
                        line = file.readline()
        except ValueError as esc:
            raise RuntimeError('Error parsing "{}"'.format(file_name)) from esc
        except FileNotFoundError as esc:
            raise RuntimeError(
                'Can\'t find file data file "{}"'.format(file_name)
            ) from esc
        except PermissionError as esc:
            raise RuntimeError(
                'No read permissiona for data file "{}"'.format(file_name)
            ) from esc
        else:
            return MayBe(DataSet(*data, sample=sample))

    def __init__(self, *data: int | float, sample: bool = False) -> None:
        self._sample: bool = sample
        self._data = list(map(lambda d: float(d), data))
        self._size = len(self._data)
        self._data.sort()
        self._calculate_stats()

    def _calculate_stats(self) -> None:
        """Calculate data statistics"""
        self._mean = self._calculate_mean()
        self._stdev = self._calculate_stdev()
        self._quartiles = self._calculate_quartiles()
        self._median = self._quartiles.map(lambda t: t[1])

    def _calculate_mean(self) -> MayBe[float]:
        """Calculate the mean of the data set, if it exists."""
        if self:
            return MayBe(sum(self._data) / self._size)
        else:
            return MayBe()

    def _calculate_stdev(self) -> MayBe[float]:
        """From the data set, calculate & return the stdev if it exists.

        - If sample is True, calculate a sample standard deviation
        - If sample is False, calculate a population standard deviation

        """
        data = self._data
        n = self._size
        if self._mean:
            mean = self._mean.get()
            if self._sample:
                if n > 1:
                    return MayBe(math.sqrt(sum(((x - mean) ** 2 for x in data)) / (n - 1)))
            else:
                if n > 0:
                    return MayBe(math.sqrt(sum(((x - mean) ** 2 for x in data)) / n))
        return MayBe()

    def _calculate_quartiles(self) -> MayBe[tuple[float, float, float]]:
        """Calculate first, second (median), and third quartiles

        Using the "trimmed mid-range" of the data.

        """
        n = self._size
        data = self._data
        if data:
            q = n // 2
            r = q // 2

            if n % 2 == 0:
                second = (data[q - 1] + data[q]) / 2.0
                lower_half = data[:q]
                upper_half = data[q:]
                if q % 2 == 0:
                    first = (lower_half[r - 1] + lower_half[r]) / 2.0
                    third = (upper_half[r - 1] + upper_half[r]) / 2.0
                else:
                    first = lower_half[(r)]
                    third = upper_half[(r)]
            else:
                second = data[q]
                lower_half = data[:q]
                upper_half = data[q:]
                if q % 2 == 0:
                    first = (lower_half[r - 1] + lower_half[r]) / 2.0
                    third = (upper_half[r - 1] + upper_half[r]) / 2.0
                else:
                    first = lower_half[(r)]
                    third = upper_half[(r)]

            return MayBe((first, second, third))
        else:
            return MayBe()

    def __bool__(self) -> bool:
        return self._size > 0

    def __iter__(self) -> Iterator[float]:
        return iter(self._data)

    def is_sample(self) -> bool:
        return self._sample

    def is_population(self) -> bool:
        return not self._sample

    def has_mean(self) -> bool:
        return bool(self._mean)

    def has_median(self) -> bool:
        return bool(self._median)

    def has_stdev(self) -> bool:
        return bool(self._stdev)

    def has_quartiles(self) -> bool:
        return bool(self._quartiles)

    @property
    def mean(self) -> float | Never:
        return self._mean.get()

    @property
    def median(self) -> float | Never:
        return self._median.get()

    @property
    def stdev(self) -> float | Never:
        return self._stdev.get()

    @property
    def quartiles(self) -> tuple[float, float, float] | Never:
        return self._quartiles.get()


class DataSets:
    """Base class for managing data sets.

    - data sets can be samples or populations
    - methods provided to

      - add or remove data sets
      - plot data sets

    - how they are related to each other is up to the user of the class

    """

    def __init__(self) -> None:
        self.data_sets: list[DataSet] = []
