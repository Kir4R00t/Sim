from arrival_generator import run_simulation
import pandas as pd

# Cały ten plik raczej nie wymaga komentarzy :v

def run_all_scenarios(n_runs):
    scenarios = {
        "base": dict(n_doctors=3, n_nurses=5, n_rooms=2),
        "extra_staff": dict(n_doctors=4, n_nurses=7, n_rooms=2),
        "dynamic_allocation": dict(n_doctors=3, n_nurses=5, n_rooms=2, dynamic_allocation=True),
        "fast_track": dict(n_doctors=3, n_nurses=5, n_rooms=2, fast_track=True),
    }

    results = []

    for name, config in scenarios.items():
        for run in range(n_runs):
            stats, utilization, duration = run_simulation(**config)
            for p in stats:
                results.append({
                    "scenario": name,
                    "run": run,
                    "priority": p.priority,
                    "wait_time": (p.triage_time - p.arrival_time) if p.triage_time else None,
                    "doctor_wait": (p.seen_by_doctor_time - p.triage_time) if p.seen_by_doctor_time else None,
                    "total_time": (p.departure_time - p.arrival_time) if p.departure_time else None
                })

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = run_all_scenarios(n_runs=100)
    df.to_csv("sor_results.csv", index=False)
