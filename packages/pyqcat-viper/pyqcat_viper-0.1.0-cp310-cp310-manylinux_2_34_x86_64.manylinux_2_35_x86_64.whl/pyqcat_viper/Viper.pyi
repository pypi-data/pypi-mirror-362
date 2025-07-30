# This code is part of pyqcat.
#
# Copyright (c) Origin Quantum Computing 2024.
#
# All Right Reserved.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# __date:         2025/05/30

# pylint: disable=unused-private-member
# pylint: disable=super-init-not-called
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
# pylint: disable=invalid-name

"""Viper python API."""
from typing import Any, List, Optional, Tuple, Dict
import numpy as np

class Coordinate:
    x: float
    y: float
    def __init__(self, x: float, y: float) -> None: ...
    def __lt__(self, other: "Coordinate") -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def to_string(self) -> str: ...

class ArbParams:
    T1: float
    T2: float
    xtalk: float
    residual_nn: List[float]
    residual_nnn: List[float]
    distortion: float
    spectator_1q: List[float]
    spectator_2q: List[float]
    tls: float
    freq_abs: float
    def __init__(
        self,
        T1: float = ...,
        T2: float = ...,
        xtalk: float = ...,
        residual_nn: List[float] = ...,
        residual_nnn: List[float] = ...,
        distortion: float = ...,
        spectator_1q: List[float] = ...,
        spectator_2q: List[float] = ...,
        tls: float = ...,
        freq_abs: float = ...,
    ) -> None: ...

class EvaluationModel:
    def __init__(
        self,
        arb_params: ArbParams,
        use_rb_spectrum: bool,
        mu_threshold: float,
        population_size: int,
        two_tq: int = ...,
        single_tq: int = ...,
        delete_unused: bool = ...,
    ) -> None: ...
    def build_chip_model(
        self,
        chip_type: str,
        chip_topology_filename: str,
        qubit_data_filename: str,
        xy_crosstalk_sim_filename: str,
        bad_edges: Optional[List[Tuple[Coordinate, Coordinate]]] = ...,
        print_chip: bool = ...,
    ) -> None: ...
    def select_nodes_to_optimize(
        self, center_node: Coordinate, surround: int
    ) -> None: ...
    def select_edges_to_optimize(
        self, center_node: Coordinate, surround: int
    ) -> None: ...
    def check_termination_condition(self, center_node: Coordinate) -> bool: ...
    def apply_optimization_result(
        self, freq_array: np.ndarray[Any, np.dtype[np.uint32]]
    ) -> None: ...
    def ea_eval_var(
        self, freq_array: np.ndarray[Any, np.dtype[np.uint32]]
    ) -> Tuple[
        np.ndarray[Any, np.dtype[np.float64]], np.ndarray[Any, np.dtype[np.float64]]
    ]: ...
    def get_optimization_result(self) -> Dict: ...
    def get_frequency_bounds(
        self, fixed_freq_dict: Dict = None
    ) -> Tuple[
        np.ndarray[Any, np.dtype[np.uint32]], np.ndarray[Any, np.dtype[np.uint32]]
    ]: ...
    def log_optimization_state(self, epoch: int) -> None: ...
    def get_qubit_str(self, coord: Coordinate) -> str: ...
    def get_coupler_str(self, edge: Tuple[Coordinate, Coordinate]) -> str: ...
    def sync_error_states(self) -> None: ...

def start_profiling(filename="profile.prof"): ...
def stop_profiling() -> int: ...
