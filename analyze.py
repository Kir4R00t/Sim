import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")
df = pd.read_csv("sor_results.csv")

# Mapa priorytetów
priority_map = {0: "Wysoki", 1: "Średni", 2: "Niski"}
df["priority_label"] = df["priority"].map(priority_map)

# Średni czas oczekiwania wg scenariusza i priorytetu
grouped = df.groupby(["scenario", "priority_label"]).agg({
    "wait_time": "mean",
    "doctor_wait": "mean",
    "total_time": "mean"
}).reset_index()

# --- WYKRESY ---
def plot_metric(metric, title, ylabel):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=grouped, x="scenario", y=metric, hue="priority_label")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Scenariusz")
    plt.legend(title="Priorytet")
    plt.tight_layout()
    plt.show()

plot_metric("wait_time", "Średni czas oczekiwania na triage", "Czas (minuty)")
plot_metric("doctor_wait", "Średni czas oczekiwania na lekarza", "Czas (minuty)")
plot_metric("total_time", "Średni łączny czas pobytu pacjenta", "Czas (minuty)")
