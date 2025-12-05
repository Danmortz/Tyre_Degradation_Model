import matplotlib.pyplot as plt

# -----------------------------
# Simple F1 Undercut vs Overcut Simulator
# -----------------------------
# Car A = pits later (overcut)
# Car B = pits earlier (undercut)
#
# Both start on Soft, then switch to Medium.
# We simulate a 25-lap race and check if the
# earlier stop (undercut) makes Car B come out ahead.

# Tyre models (same logic style as your degradation script)
SOFT_BASE = 90.0
SOFT_DEG = 0.18

MEDIUM_BASE = 91.0
MEDIUM_DEG = 0.12

PIT_LOSS = 22.0     # seconds lost during pit stop (pit lane time)
TOTAL_LAPS = 25     # race length

def lap_time(compound: str, tyre_age: int) -> float:
    """Return lap time in seconds for a given compound and tyre age (laps used)."""
    if compound == "Soft":
        return SOFT_BASE + SOFT_DEG * tyre_age
    elif compound == "Medium":
        return MEDIUM_BASE + MEDIUM_DEG * tyre_age
    else:
        raise ValueError("Unknown compound")


def simulate_car(pit_lap: int, first_compound="Soft", second_compound="Medium"):
    """
    Simulate one car that starts on first_compound,
    pits on pit_lap and switches to second_compound.
    Returns list of lap times (length TOTAL_LAPS).
    """
    times = []
    tyre_compound = first_compound
    tyre_age = 0  # laps used on current tyre

    for lap in range(1, TOTAL_LAPS + 1):
        if lap == pit_lap:
            # Do the pit stop on this lap
            # Lap time = normal lap + pit loss
            base_time = lap_time(tyre_compound, tyre_age)
            times.append(base_time + PIT_LOSS)

            # Switch tyre for next lap
            tyre_compound = second_compound
            tyre_age = 0
        else:
            t = lap_time(tyre_compound, tyre_age)
            times.append(t)
            tyre_age += 1

    return times


def cumulative(times):
    """Convert lap times to cumulative race time."""
    total = 0.0
    out = []
    for t in times:
        total += t
        out.append(total)
    return out


def main():
    # Car B (undercut) pits earlier, e.g. lap 10
    pit_lap_B = 10
    # Car A (overcut) pits later, e.g. 3 laps after B
    pit_lap_A = pit_lap_B + 3

    times_A = simulate_car(pit_lap_A)
    times_B = simulate_car(pit_lap_B)

    cum_A = cumulative(times_A)
    cum_B = cumulative(times_B)

    laps = list(range(1, TOTAL_LAPS + 1))
    gap = [cum_B[i] - cum_A[i] for i in range(TOTAL_LAPS)]  # B - A (negative = B ahead)

    # Find first lap where undercut works (Car B ahead)
    undercut_lap = None
    for i, g in enumerate(gap):
        if g < 0:
            undercut_lap = laps[i]
            break

    print(f"Car B (undercut) pits on lap {pit_lap_B}")
    print(f"Car A (overcut) pits on lap {pit_lap_A}")
    if undercut_lap is not None:
        print(f"➡ Undercut successful: Car B becomes ahead on lap {undercut_lap}")
        print(f"   Gap on that lap: {gap[undercut_lap-1]:.3f} seconds (negative = B ahead)")
    else:
        print("❌ Undercut did NOT work: Car B never gets ahead of Car A in this stint.")

    # Plot gap vs lap
    plt.figure(figsize=(10, 6))
    plt.axhline(0, linestyle="--")  # zero line
    plt.plot(laps, gap)
    plt.xlabel("Lap Number")
    plt.ylabel("Gap (Car B - Car A) [s]")
    plt.title("Undercut vs Overcut – Time Gap vs Lap\n(Negative gap = Undercut car ahead)")
    plt.savefig("undercut_gap_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
