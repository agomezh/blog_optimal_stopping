import random

import numpy as np
import pandas as pd
import streamlit as st

# Definitions of problem


# Initial Problem, strategy and status
def create_secretary_problem(num_candidates, cost_per_step=0.5):
    candidates_lst = list(range(num_candidates))
    candidates_rank = random.sample(candidates_lst, num_candidates)

    problem = {
        "candidates_idx": candidates_lst,
        "candidates_rank": candidates_rank,
        "cost_per_step": cost_per_step,
    }

    return problem


def create_secretary_strategy(percent_population: float):
    """percent_population is a float between 0 and 1 indicating proportion of the population to see"""

    strategy = {
        "observations": percent_population,
    }
    return strategy


def create_initial_status():

    initial_status = {
        "step": -1,
        "choice": -1,
        "rank": -1,
        "strategy_ended": False,
        "strategy_in_observation_period": True,
    }

    return initial_status


def secretary_problem(initial_status, problem, strategy):
    history = []
    current_status = dict(initial_status)
    while not current_status["strategy_ended"]:
        history.append(dict(current_status))
        current_status = next_step(history[-1], problem, strategy)

    return history


def next_step(status: dict, problem, strategy):
    """Makes the next step in the secretary problem (i.e next canddiate)"""
    current_step = status["step"] + 1
    status["step"] = current_step
    num_candidates = len(problem["candidates_idx"])

    status["strategy_in_observation_period"] = current_step <= (
        strategy["observations"] * num_candidates
    )

    are_enough_candidates = current_step < num_candidates
    if are_enough_candidates:
        seen_candidates_rank = problem["candidates_rank"][0 : current_step + 1]
        new_candidate_rank = seen_candidates_rank[-1]

        if new_candidate_rank > status["rank"]:
            status["rank"] = new_candidate_rank
            status["choice"] = current_step

            if not status["strategy_in_observation_period"]:
                status["strategy_ended"] = True

    else:
        seen_candidates_rank = problem["candidates_rank"][0 : current_step + 1]
        new_candidate_rank = seen_candidates_rank[-1]
        status["rank"] = new_candidate_rank
        status["choice"] = current_step

        status["strategy_ended"] = True

    return dict(status)


def cost_of_simulation(history, problem):
    results = dict()
    results["steps"] = history[-1]["step"]
    results["rank"] = history[-1]["rank"]
    results["result"] = results["rank"] - (results["steps"] * problem["cost_per_step"])
    return results


if __name__ == "__main__":
    num_sim = 1000
    for sim in range(num_sim):
        problem = create_secretary_problem(num_sim)
        strategy = create_secretary_strategy(percent_population=0.3)
        initial_status = create_initial_status()
        history = secretary_problem(dict(initial_status), dict(problem), dict(strategy))
        print(f"{cost_of_simulation(history, problem) = }")
