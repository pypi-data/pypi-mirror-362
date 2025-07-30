# -*- coding: utf-8 -*-

# This code is part of pyqcat-viper.
#
# Copyright (c) 2021-2030 Origin Quantum Computing. All Right Reserved.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# __date:         2025/05/31
# __author:       HanQing Shi

# pylint: disable=no-name-in-module.
# pylint: disable=import-error.
# pylint: disable=wildcard-import.
# pylint: disable=undefined-variable.
# pylint: disable=expression-not-assigned.
# pylint: disable=c-extension-no-member.
# pylint: disable=invalid-name.
# pylint: disable=too-many-arguments.
# pylint: disable=too-many-positional-arguments.
# pylint: disable=too-many-instance-attributes.
# We disable the pylint error because the pylint can't recognize the C++ extensions.

"""Viper optimizer: Inspired by Google's Snake."""
import json
import pathlib
from typing import Any, Dict, List, Tuple

import geatpy as ea
import numpy as np
import spdlog

from pyqcat_viper.Viper import ArbParams, Coordinate, EvaluationModel

logger = spdlog.ConsoleLogger("py")


class ViperOptimizer:
    """Viper Optimizer class.

    Args:
        algorithm_name (str): The name of the algorithm being used.
        initial_center_node (Coordinate): The initial center node coordinate for the algorithm.
        surround (int): The number of surrounding nodes to consider.
        max_gen (int): The maximum number of generations for the evolutionary process.
        iteration (int): The number of outer iterations for the algorithm.
        inner_iteration (int): The number of inner iterations within each outer iteration.
        seed (int): The random seed for reproducibility.
        save_path (pathlib.Path): The path where the results and intermediate files should be saved.
        fixed_freq_dict (Dict[str, int], optional): A dictionary of fixed frequencies for certain
                                                    nodes, defaults to None.
        save_process_chip (bool, optional): Whether to save the process chip data, defaults to
                                            False.

    Attributes:
        algorithm_name (str): The name of the algorithm. Only support 'DE' for now.
        center_node (Coordinate): The center node coordinate.
        surround (int): The number of surrounding nodes.
        max_gen (int): The maximum number of generations.
        iteration (int): The number of outer iterations.
        inner_iteration (int): The number of inner iterations.
        seed (int): The random seed.
        save_path (pathlib.Path): The path for saving results.
        fixed_freq_dict (Dict[str, int] | None): The fixed frequency dictionary.
        save_process_chip (bool): Whether to save process chip data.
        population_size (int | None): The size of the population, initialized to None.
        current_inner (int): The current inner iteration count, initialized to 0.
        epoch (None): Placeholder for epoch information, initialized to None.
        constraint_states (dict): A dictionary to store constraint states.
        tracker (dict): A dictionary to track various metrics.
        _eval_model (EvaluationModel | None): The C++ evaluation model, initialized to None.
    """

    def __init__(
        self,
        algorithm_name: str,
        initial_center_node: Coordinate,
        surround: int,
        max_gen: int,
        iteration: int,
        inner_iteration: int,
        seed: int,
        save_path: pathlib.Path,
        fixed_freq_dict: Dict[str, int] = None,
        save_process_chip: bool = False,
    ):
        self.algorithm_name = algorithm_name
        self.center_node = initial_center_node
        self.surround = surround
        self.max_gen = max_gen
        self.iteration = iteration
        self.inner_iteration = inner_iteration
        self.seed = seed
        self.save_path = save_path
        self.fixed_freq_dict = fixed_freq_dict
        self.save_process_chip = save_process_chip
        self.population_size: int | None = None

        self.current_inner = 0
        self.epoch = None
        self.constraint_states = {}
        self.tracker = {}

        # C++ evaluation model.
        self._eval_model: EvaluationModel | None = None

    @staticmethod
    def _check_file_path(f_name: str):
        """Check if the file directory path exists, create if not."""
        file_path = pathlib.Path(f_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)

    def _initialize_tracker(self):
        params = {
            "center_node": self._eval_model.get_qubit_str(self.center_node),
            "inner_iteration": self.inner_iteration,
            "popsize": self.population_size,
            "MAXGEN": self.max_gen,
            "surround": self.surround,
            "algorithm_name": self.algorithm_name,
        }
        self.tracker["params"] = params

    def _ea_eval_var_debug(self, freq_array):
        # Just for debugging.
        error_array, cv_array = self._eval_model.ea_eval_var(freq_array)
        return error_array, cv_array

    def build_evaluation_model(
        self,
        chip_type: str,
        chip_json_path: pathlib.Path,
        qubit_data_path: pathlib.Path,
        xy_crosstalk_path: pathlib.Path,
        arb_params: ArbParams,
        use_rb_spectrum: bool,
        mu_threshold: float,
        population_size: int,
        two_tq: int = 40,
        single_tq: int = 20,
        delete_unused: bool = True,
        bad_edges: List[Tuple[Coordinate, Coordinate]] | None = None,
        print_graph: bool = True,
    ):
        """
        Builds an evaluation model for quantum chip performance analysis.

        Args:
            chip_type (str): The type of quantum chip being modeled.
            chip_json_path (pathlib.Path): The path to the JSON file containing chip topology data.
            qubit_data_path (pathlib.Path): The path to the file containing qubit-specific data.
            xy_crosstalk_path (pathlib.Path): The path to the file containing XY crosstalk data.
            arb_params (ArbParams): Arbitrary waveform generator parameters.
            use_rb_spectrum (bool): Whether to use Randomized Benchmarking spectrum in the
                                    evaluation.
            mu_threshold (float): The threshold value for mu in the evaluation criteria.
            population_size (int): The size of the population used in the evaluation algorithm.
            two_tq (int, optional): The number of two-qubit gate time units, defaults to 40ns.
            single_tq (int, optional): The number of single-qubit gate time units, defaults to 20ns.
            delete_unused (bool, optional): Whether to delete unused qubits from the model, defaults
                                            to True.
            bad_edges (List[Tuple[Coordinate, Coordinate]], optional): A list of bad qubit
                                                    connections (edges), defaults to None.
            print_graph (bool, optional): Whether to print the chip graph, defaults to True.
        """
        self._eval_model = EvaluationModel(
            arb_params,
            use_rb_spectrum,
            mu_threshold,
            population_size,
            two_tq,
            single_tq,
            delete_unused,
        )
        self._eval_model.build_chip_model(
            chip_type,
            str(chip_json_path),
            str(qubit_data_path),
            str(xy_crosstalk_path),
            bad_edges,
            print_graph,
        )
        self.population_size = population_size
        self._initialize_tracker()

    def _run_de_algorithm(
        self,
        lb_bounds: np.ndarray[Any, np.dtype[np.uint32]],
        ub_bounds: np.ndarray[Any, np.dtype[np.uint32]],
    ):
        problem = ea.Problem(
            name="err_model",
            M=1,
            maxormins=[1],
            Dim=len(lb_bounds),
            varTypes=[1] * len(lb_bounds),
            lb=lb_bounds,
            ub=ub_bounds,
            # If you want to debug, uncomment the following line
            # and comment the line below.
            # evalVars=self._ea_eval_var_debug,
            evalVars=self._eval_model.ea_eval_var,
        )
        best_solution = None
        best_fitness = float("inf")

        for idx in range(self.inner_iteration):
            self.current_inner = idx
            population = ea.Population(Encoding="RI", NIND=self.population_size)

            algorithm = ea.soea_DE_best_1_bin_templet(
                problem=problem,
                population=population,
                MAXGEN=self.max_gen,
                logTras=50,
                maxTrappedCount=150,
                outFunc=self._states_func,
            )
            algorithm.mutOper.F = 0.95
            algorithm.recOper.XOVR = 0.7

            path_name = str(self.save_path / f"epoch={self.epoch}-{idx} soea_DE result")
            self._check_file_path(path_name)

            res = ea.optimize(
                algorithm=algorithm,
                seed=self.seed,
                prophet=best_solution,
                verbose=True,
                drawing=0,
                outputMsg=True,
                drawLog=False,
                saveFlag=True,
                dirName=path_name,
            )

            current_solution = res["Vars"][0]
            current_fitness = res["ObjV"][0][0]

            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_solution = current_solution

            # if self.save_process_chip:
            #     # Update the optimization tracker.
            #     self._update_optimization_tracker(current_fitness, res["executeTime"])

            self.constraint_states = {}

        return best_solution

    def _update_optimization_tracker(self, avg_error, exec_time):
        epoch = self.epoch
        inner_iter = self.current_inner

        # Create epoch entry if it doesn't exist
        if f"epoch {epoch}" not in self.tracker:
            self.tracker[f"epoch {epoch}"] = {}

        # low efficiency. do not use this in production.
        self._eval_model.sync_error_states()
        error_dict = self._eval_model.get_optimization_result()
        qubits_error_dict = error_dict["qubits_error_map"]
        couplers_error_dict = error_dict["couplers_error_map"]

        # Create inner iteration entry
        self.tracker[f"epoch {epoch}"][f"inner iter {inner_iter}"] = {
            "node error": qubits_error_dict,
            "edge error": couplers_error_dict,
            "ave error": avg_error,
            "executeTime": f"{exec_time:.2f}s",
            "constraint states": self.constraint_states or {},
        }

    def _update_optimize_result_to_tracker(self):
        epoch = self.epoch
        # Create epoch entry if it doesn't exist
        if f"epoch {epoch}" not in self.tracker:
            self.tracker[f"epoch {epoch}"] = {}

        # TODO Only get the target qubits and couplers, not always all.
        error_dict = self._eval_model.get_optimization_result()
        qubits_error_dict = error_dict["qubits_error_map"]
        couplers_error_dict = error_dict["couplers_error_map"]

        # Create inner iteration entry
        self.tracker[f"epoch {epoch}"] = {
            "node error": qubits_error_dict,
            "edge error": couplers_error_dict,
        }

    def _run_optimization_algorithm(
        self,
        lb_bounds: np.ndarray[Any, np.dtype[np.uint32]],
        ub_bounds: np.ndarray[Any, np.dtype[np.uint32]],
    ):
        if self.algorithm_name == "DE":
            return self._run_de_algorithm(lb_bounds, ub_bounds)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm_name}")

    def _run_optimization_iteration(self):
        freq_lb_bounds, freq_ub_bounds = self._eval_model.get_frequency_bounds(
            self.fixed_freq_dict
        )
        best_frequencies = self._run_optimization_algorithm(
            freq_lb_bounds, freq_ub_bounds
        )
        return best_frequencies

    def _states_func(self, algorithm, pop):
        current_gen = algorithm.currentGen
        CV = pop.CV
        if CV is not None:
            satisfied_count = np.sum(np.all(CV <= 0, axis=1))
            total = pop.sizes
            ratio = satisfied_count / total if total > 0 else 0
            self.constraint_states[current_gen] = ratio

    def _save_epoch_results(self):
        save_path = self.save_path / "allocator_tracker.json"
        with open(save_path, "w") as f:
            json.dump(self.tracker, f, indent=4)

    def run(self):
        """Run the optimizer."""
        logger.info(f"Start optimization process at center {self.center_node}.")
        for epoch in range(1, self.iteration + 1):
            self.epoch = epoch
            self._eval_model.select_nodes_to_optimize(self.center_node, self.surround)
            self._eval_model.select_edges_to_optimize(self.center_node, self.surround)
            self._eval_model.log_optimization_state(epoch)

            best_frequencies = self._run_optimization_iteration()

            self._eval_model.apply_optimization_result(best_frequencies)
            logger.info(f"Epoch {epoch} completed, apply the best frequencies to chip.")

            if self.save_process_chip:
                self._update_optimize_result_to_tracker()

            if self._eval_model.check_termination_condition(self.center_node):
                break

            logger.info(f"Change center node to {self.center_node}.")

        if self.save_process_chip:
            self._save_epoch_results()

        logger.info("Optimization completed.")
