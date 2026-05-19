import pm4py
import pandas as pd
from typing import Optional


def discover_dfg(event_log: pd.DataFrame) -> tuple:
    dfg, start_activities, end_activities = pm4py.discover_dfg(
        event_log,
        activity_key="activity",
        timestamp_key="timestamp",
        case_id_key="case_id",
    )
    return dfg, start_activities, end_activities


def discover_inductive_model(event_log: pd.DataFrame):
    process_tree = pm4py.discover_process_tree_inductive(event_log)
    return process_tree


def check_conformance(event_log: pd.DataFrame, model_type: str = "inductive") -> dict:
    if model_type == "inductive":
        process_tree = discover_inductive_model(event_log)
        net, im, fm = pm4py.convert_to_petri_net(process_tree)
    else:
        dfg, start_activities, end_activities = discover_dfg(event_log)
        net, im, fm = pm4py.convert_to_petri_net_dfg(dfg, start_activities, end_activities)

    aligned_traces = pm4py.conformance_diagnostics_alignments(event_log, net, im, fm)
    fitness = pm4py.fitness_alignments(aligned_traces)
    return {
        "fitness": fitness,
        "num_traces": len(event_log["case_id"].unique()),
        "num_events": len(event_log),
    }
