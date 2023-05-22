"""Optional stopping"""

import altair as alt
import pandas as pd
import streamlit as st

import secretary_problem

st.set_page_config(layout="wide")


def main():
    # hide_streamlit_style = """
    # <style>
    ##MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # </style>
    ## Set up
    logo_loc = "./media/ADAO_logo_2.png"

    ## Sidebar
    st.sidebar.image(image=logo_loc, width=300)
    st.sidebar.markdown("---")

    with st.sidebar:
        num_candidates = st.slider("Number of candidates", 1, 1000, 100)
        cost = st.slider(
            "Cost per observation (100 = - 1 rank per observation)", 0, 100, 10
        )
        cost = cost / 100.0
        num_simulations = st.slider("Number of simulations", 1, 1000, 100)
        stopping_strategy = st.slider(
            "Stop after what percentage of candidates seen", 0, 100, 37
        )
        stopping_strategy = stopping_strategy / 100.0

    st.sidebar.info(
        "This is a demo. Interested? Fill in [Contact form](https://docs.google.com/forms/d/e/1FAIpQLSeuMiVF7f0XVMQ8C-9jntlQU_lBzX0J5dymg1yLt7Y0QxUN_Q/viewform?usp=sf_link) or email us at <contact@adao.tech> "
    )

    ## Main
    st.title("Optional stopping problem")

    cost_of_simulation_lst = []
    rank_candidate_lst = []
    steps_lst = []
    history_lst = []

    for _ in range(num_simulations):
        initial_status = secretary_problem.create_initial_status()
        problem = secretary_problem.create_secretary_problem(num_candidates, cost)
        strategy = secretary_problem.create_secretary_strategy(stopping_strategy)
        history = secretary_problem.secretary_problem(
            dict(initial_status), dict(problem), dict(strategy)
        )
        cost_of_simulation_lst.append(
            secretary_problem.cost_of_simulation(history, problem)["result"]
        )
        rank_candidate_lst.append(history[-1]["rank"])
        steps_lst.append(history[-1]["step"])

    data = pd.DataFrame(
        {
            "cost_of_simulation": cost_of_simulation_lst,
            "rank_candidate": rank_candidate_lst,
            "steps": steps_lst,
        }
    )
    # making the simple histogram on Acceleration
    st.subheader("Results")
    hist_1 = alt.Chart(data).mark_bar().encode(x="cost_of_simulation", y="count()")
    st.altair_chart(hist_1, use_container_width=True)

    st.write(
        "The cost of simulation is the [cost = rank - steps * cost]. This shows that observing will incur a cost."
    )

    st.subheader("Ranks")
    hist_2 = alt.Chart(data).mark_bar().encode(x="rank_candidate", y="count()")
    st.altair_chart(hist_2, use_container_width=True)
    st.write("The rank of the candidate chosen")

    st.subheader("Steps")
    hist_3 = alt.Chart(data).mark_bar().encode(x="steps", y="count()")
    st.altair_chart(hist_3, use_container_width=True)
    st.write("The steps it took to choose the candidate")

    ## Main - Closure
    st.markdown("---")
    st.write(
        """### Contact

Contact us:

- Form: [Contact form](https://docs.google.com/forms/d/e/1FAIpQLSeuMiVF7f0XVMQ8C-9jntlQU_lBzX0J5dymg1yLt7Y0QxUN_Q/viewform?usp=sf_link)

- Email: <contact@adao.tech>

        """
    )

    st.write(
        """### Disclaimer
    This software is presented "as-is" and the user accepts this condition
    before using it.  In its current form it is a Demo and no representation is
    given as to performance nor compliance. Also, no warranties are offered as
    to the software's functionality. The software can be used for demonstration
    purposes only. 

    The software is subject to copyrights and no license is offered as part of
    the demonstration offered here. Users are solely responsible for damages of
    any kind that may ensue from using this software in any way beyond this
    demonstration."""
    )


if __name__ == "__main__":
    main()
