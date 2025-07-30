"""
@file python/dandeliion/client/solution.py

Module containing class for handling access to solutions
"""

#
# Copyright (C) 2024-2025 Dandeliion Team
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3.0 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

# built-in modules
import logging
import copy
import json
from typing import Protocol, Optional, Union
from pathlib import Path
from collections.abc import Mapping

# custom modules
from .exceptions import DandeliionAPIException

# third-party modules
import numpy as np
import numpy.typing


logger = logging.getLogger(__name__)


class Simulator(Protocol):
    """ Simulator Protocol """
    def update_results(self, prefetched_data: dict, keys: list = None, inline: bool = False) -> Optional[dict]: ...
    def get_status(self, prefetched_data: dict) -> str: ...
    def get_log(self, prefetched_data: dict) -> str: ...


class InterpolatedArray(np.ndarray):
    """
    Subclass of ndarray providing function call for linear interpolation
    """
    def __new__(cls, t: np.typing.ArrayLike, y: np.typing.ArrayLike, **kwargs):
        instance = np.asarray(y, **kwargs).view(cls)
        instance.t = np.array(t)
        return instance

    def __call__(self, t):
        """
        function call to return interpolated value
        """
        # check that 1-d array
        if not (len(self.t.shape) == len(self.shape) == 1):
            raise ValueError('x and y must be 1-d array-like objects')
        # check that array of same length
        if self.t.shape != self.shape:
            raise ValueError('x and y must be of same length')
        return np.interp(t, self.t, self)


class Solution(Mapping):
    """
    Dictionary-style class for the solutions of a simulation run
    returned by :meth:`solve`
    """

    _data: dict = None
    _sim: Simulator = None

    def __init__(self, sim: Simulator, prefetched_data: Union[dict, str, Path], time_column: str = None):
        """
        Constructor

        Args:
            sim (Simulator): simulator instance for fetching data from server
            prefetched_data (dict | str | Path): existing (meta) data either as dictionary or stored in json file
            time_column (str): label of time column (used for interpolation)
        """
        self._sim = sim
        # if prefetched_data is not dict i.e. path to json file instead, load file
        if not isinstance(prefetched_data, dict):
            with open(prefetched_data, 'r') as f:
                prefetched_data = json.load(f)
        self._data = prefetched_data
        self._time_column = time_column

    def _init_solution(self):
        """
        Initialises prefetched solution from simulator if necessary
        """
        logger.debug('Initialising solutions')
        self._sim.update_results(self._data, inline=True)
        # if solution still not initialised (e.g. because simulation
        # failed or has not finished yet), raise Exception
        if self._data['Solution'] is None:
            raise DandeliionAPIException(
                'Solution not ready (yet). Check status for details.'
            )

    def __getitem__(self, key: str):
        """
        Returns the results requested by the key.

        Args:
            key (str): key for results to be returned.

        Returns:
            object: data as requested by provided key
        """

        # if solution not initialised yet, try to fetch from server
        if self._data.get('Solution', None) is None:
            self._init_solution()

        if key not in self._data['Solution']:
            raise KeyError(
                f'Column for {key} does not exist in solution.'
            )
        # fetch data if necessary (time column and requested column)
        keys = []
        if self._time_column is not None and self._data['Solution'][self._time_column] is None:
            logger.info(f"Fetching '{self._time_column}' column from simulator")
            keys.append(self._time_column)
        if self._data['Solution'][key] is None and (self._time_column is None or key != self._time_column):
            logger.info(f"Fetching '{key}' column from simulator")
            keys.append(key)
        if keys:
            self._sim.update_results(self._data, keys=keys, inline=True)
        # now return either an InterpolatedArray (if time column defined) or just a numpy array with a copy
        # of the requested column
        if self._time_column is not None:
            return InterpolatedArray(t=self._data['Solution'][self._time_column], y=self._data['Solution'][key])
        else:
            return np.array(copy.deepcopy(self._data['Solution'][key]))

    def __len__(self):
        """
        Returns the number of fields in the solutions.

        Returns:
            int: number of fields
        """
        if self._data.get('Solution', None) is None:
            self._init_solution()
        return len(self._data['Solution'])

    def __iter__(self):
        """
        Returns an iterator on the solutions fields.

        Returns:
            iterator
        """
        if self._data.get('Solution', None) is None:
            self._init_solution()
        yield from self._data['Solution']

    @property
    def status(self):
        """
        Returns the status of the simulation run linked to this solutions

        Returns:
            str: current status of simulation run ('queued', 'running', 'failed', 'success')
        """
        return self._sim.get_status(self._data)

    @property
    def log(self):
        """
        Returns the log file produced by the backend

        Returns:
            str: contents of log file (runtime_log.txt)
        """
        return self._sim.get_log(self._data)

    def dump(self, filepath: Union[str, Path]):
        """
        Fetches all data and stores it into file.

        Args:
           filepath (str | Path): path to file were data should be stored
        """
        # fetch all (meta)data
        self._sim.get_status(self._data)
        try:
            self._sim.update_results(self._data, keys=list(self.keys()), inline=True)
        except DandeliionAPIException:  # if simulation not done yet
            pass
        self._sim.get_log(self._data)

        # now dump into file
        with open(filepath, 'w') as f:
            json.dump(self._data, f)

    def join(self):
        """
        Blocks until solution is available (i.e. simulation is done)
        """
        self._sim._join(self._data)
