import random
import csv

# -----------------------------
# Simple F1 Tyre Degradation Model
# -----------------------------
# We simulate lap times for 3 compounds:
# Soft, Medium, Hard
# Soft: fastest, degrades quickly
# Medium: balanced
# Hard: slowest, degrades slowly

COMPOUNDS = {
    "Soft": {
        "base_lap": 90.0,    # seconds
        "deg_per_lap": 0.18  # how much slower per lap
    },
    "Medium": {
        "base_lap": 91.0,
        "deg_per_lap": 0.12
    },
    "Hard": {
        "base_lap": 92.0,
        "deg_per_lap": 0.08
    }
}

def simulate_stint(compound_name: str, laps: int = 20, random_variation: float = 0.08):
    """
    Simulate a stint for one compound.
    Returns a list of lap times in seconds.
    """
    compound = COMPOUNDS[compound_name]
    base = compound["base_lap"]
    deg = compound["deg_per_lap"]

    lap_times = []

    for lap in range(1, laps + 1):
        # Linear degradation: each lap gets slightly slower
        ideal_time = base + deg * (lap - 1)

        # Add some randomness to simulate driver / wind / track changes
        noise = random.uniform(-random_variation, random_variation)

        lap_time = ideal_time + noise
        lap_times.append(round(lap_time, 3))

    return lap_times


def save_to_csv(filename: str, laps: int, data: dict):
    """
    Save lap times to a CSV file.
    data = {
        "Soft": [...],
        "Medium": [...],
        "Hard": [...]
    }
    """
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Header
        header = ["Lap"] + list(data.keys())
        writer.writerow(header)

        for lap in range(laps):
            row = [lap + 1]
            for compound in data.keys():
                row.append(data[compound][lap])
            writer.writerow(row)

    print(f"Saved results to {filename}")


def main():
    laps = 20  # length of stint

    results = {}
    for compound in COMPOUNDS.keys():
        results[compound] = simulate_stint(compound, laps=laps)

    # Print a small sample to console
    print("Sample lap times (first 5 laps):")
    for compound, times in results.items():
        print(f"{compound}: {times[:5]}")

    # Save for further analysis (Excel / Power BI)
    save_to_csv("tyre_degradation_results.csv", laps, results)


if __name__ == "__main__":
    main()
