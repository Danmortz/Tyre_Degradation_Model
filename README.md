# 🛞 F1 Tyre Degradation Model

## 📌 Summary
This project simulates basic tyre degradation for three F1 compounds: Soft, Medium, and Hard.  
Each compound starts from a base lap time and gets slightly slower every lap, with a small random variation to mimic real-world behaviour.

The goal is to demonstrate how tyre degradation affects lap times and to generate data that can be analysed in Excel or Power BI.

---

## ⚙️ How the Model Works

For each compound:

- `base_lap`: starting lap time in seconds  
- `deg_per_lap`: how much slower the tyre gets each lap  
- Random noise is added to each lap to make the data less predictable

Output:
- A file named **`tyre_degradation_results.csv`**
- Columns: `Lap, Soft, Medium, Hard`
- 20 laps simulated by default

---

## ▶️ How to Run

1. Download or clone this repository  
2. Open Terminal in this folder  
3. Run:

```bash
python3 tyre_degradation.py
