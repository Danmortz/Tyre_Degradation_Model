import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ----------------------------------------
# Simple F1 Race Pace Prediction Model
# ----------------------------------------
# We generate synthetic lap data for:
# Soft, Medium, Hard tyres
# Features -> lap number, tyre age, compound code
# Target -> lap time (seconds)
#
# Then we train a Linear Regression model to
# predict lap time from these features.


COMPOUNDS = {
    "Soft": {"base": 90.0, "deg": 0.20, "code": 0},
    "Medium": {"base": 91.0, "deg": 0.14, "code": 1},
    "Hard": {"base": 92.0, "deg": 0.10, "code": 2},
}

LAPS_PER_STINT = 20   # laps per compound


def generate_data():
    X = []  # features: [lap_number, tyre_age, compound_code]
    y = []  # lap time in seconds

    for compound_name, params in COMPOUNDS.items():
        base = params["base"]
        deg = params["deg"]
        code = params["code"]

        for lap in range(1, LAPS_PER_STINT + 1):
            tyre_age = lap - 1

            # Fuel effect: early laps are slower (heavy car)
            fuel_effect = (LAPS_PER_STINT - lap) * 0.03  # 0.03s per lap of fuel burn

            ideal_time = base + deg * tyre_age - fuel_effect

            # Some random noise to make it realistic
            noise = random.uniform(-0.08, 0.08)

            lap_time = ideal_time + noise

            X.append([lap, tyre_age, code])
            y.append(lap_time)

    return X, y


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    print("Model R² score on test set:", round(score, 4))
    print("Coefficients (lap, tyre_age, compound_code):", model.coef_)
    print("Intercept:", model.intercept_)

    # Predict on test set for plotting
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred


def plot_results(y_test, y_pred):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred)

    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")

    plt.xlabel("Actual Lap Time (s)")
    plt.ylabel("Predicted Lap Time (s)")
    plt.title("F1 Race Pace Prediction – Actual vs Predicted")

    plt.savefig("race_pace_prediction_plot.png", dpi=300)
    plt.show()


def main():
    X, y = generate_data()
    model, X_test, y_test, y_pred = train_model(X, y)

    # Show a few example predictions
    print("\nSample predictions (first 5):")
    for i in range(5):
        features = X_test[i]
        actual = y_test[i]
        predicted = y_pred[i]
        print(
            f"Features {features} -> Actual: {round(actual,3)} s, "
            f"Predicted: {round(predicted,3)} s"
        )

    plot_results(y_test, y_pred)


if __name__ == "__main__":
    main()
