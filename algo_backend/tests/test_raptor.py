import pytest
from algo_backend.raptor import RAPTOR   # <-- adjust to your module
from algo_backend.mock_dataset import build_mock_data  # <-- adjust path


@pytest.fixture
def dataset():
    return build_mock_data()


def run_raptor(dataset, source_id, target_id, departure_time, max_rounds=6):
    stops = dataset["stop_list"]
    routes = dataset["route_list"]

    source = next(s for s in stops if s.id == source_id)
    target = next(s for s in stops if s.id == target_id)

    r = RAPTOR(
        source_stop=source,
        target_stop=target,
        departure_time=departure_time,
        stop_list=stops,
        route_list=routes,
        max_rounds=max_rounds
    )
    return r


# -------------------------------------------------------------------------
# 1. BASIC REACHABILITY: S0 → S3 via Route R1 (direct)
# -------------------------------------------------------------------------

def test_direct_reachable(dataset):
    r = run_raptor(dataset, "S0", "S3", departure_time=480)
    tau = r  # RAPTOR returns tau matrix
    
    S3_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S3")

    # Earliest arrival should match R1_T2 (faster trip)
    # R1_T2 arrives S3 at 497
    assert min(tau[S3_index]) == 497


# -------------------------------------------------------------------------
# 2. BEST CHOICE BETWEEN TWO POSSIBLE JOURNEYS:
# R1_T2 connects to R5_T2 earlier than R1_T1→R5_T1
# -------------------------------------------------------------------------

def test_best_transfer_path(dataset):
    r = run_raptor(dataset, "S0", "S11", departure_time=480)
    tau = r

    S11_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S11")

    # Expected:
    #   R1_T2 reaches S3 at 497
    #   Transfer (S3 min_transfer=1) → ready at 498
    #   R5_T2 departs S3 at 498 → arrives S11 at 518
    assert min(tau[S11_index]) == 518


# -------------------------------------------------------------------------
# 3. TRANSFER AT S2: S0 → S4 (through R1 then R2)
# -------------------------------------------------------------------------

def test_transfer_at_s2(dataset):
    r = run_raptor(dataset, "S0", "S4", departure_time=480)
    tau = r

    S4_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S4")

    # Expected:
    #   R1_T2 arrives S2 at 492
    #   min_transfer (3 min) → 495
    #   R2_T1 departs S2 at 492 → too early
    #   Must take R2_T2 (08:40 = 520)
    #   Arrival at S4 = 526
    assert min(tau[S4_index]) == 526


# -------------------------------------------------------------------------
# 4. UNREACHABLE REGION: S0 → S9 (isolated route R4)
# -------------------------------------------------------------------------

def test_unreachable_stop(dataset):
    r = run_raptor(dataset, "S0", "S9", departure_time=480)
    tau = r

    S9_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S9")

    assert all(t == float("inf") for t in tau[S9_index])


# -------------------------------------------------------------------------
# 5. OVERTAKING: R1_T2 arrives earlier than R1_T1
# -------------------------------------------------------------------------

def test_overtaking_trip(dataset):
    r = run_raptor(dataset, "S1", "S3", departure_time=480)
    tau = r

    S3_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S3")

    # R1_T2 arrives earlier (497 vs 500)
    assert min(tau[S3_index]) == 497


# -------------------------------------------------------------------------
# 6. ALTERNATE BRANCH ROUTE: S1 → S7 via R3
# -------------------------------------------------------------------------

def test_branch_network(dataset):
    r = run_raptor(dataset, "S1", "S7", departure_time=480)
    tau = r

    S7_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S7")

    # R3_T1: S1@486 → S7@500
    assert min(tau[S7_index]) == 500


# -------------------------------------------------------------------------
# 7. START TIME TOO LATE: missing early trip (S0 → S3 at 08:18)
# -------------------------------------------------------------------------

def test_start_after_first_trip(dataset):
    r = run_raptor(dataset, "S0", "S3", departure_time=495)  # 08:15
    tau = r

    S3_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S3")

    # Only R1_T2 is reachable (T1 left at 480)
    assert min(tau[S3_index]) == 497


# -------------------------------------------------------------------------
# 8. NO POSSIBLE TRANSFER: S6 → S3 (branch does not connect backward)
# -------------------------------------------------------------------------

def test_no_transfer_backward(dataset):
    r = run_raptor(dataset, "S6", "S3", departure_time=480)
    tau = r

    S3_index = next(s.index_in_list for s in dataset["stop_list"] if s.id == "S3")

    assert all(t == float("inf") for t in tau[S3_index])
