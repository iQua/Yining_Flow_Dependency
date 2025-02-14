import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator

# Reading data from the CSV file, skipping extraneous headers
file_name = "results/experiment1_time_cost"
csv_file_path = "./" + file_name + ".csv"
data = pd.read_csv(
    csv_file_path  # , skiprows=1
)  # Adjust 'skiprows' as necessary based on the header structure

methods = ["DataAware  ", "Barrier  ", "Optimal"]
n_collectives = ["2-RAR", "4-RAR", "6-RAR", "8-RAR"]
# Plotting the data
figure_size = 5, 4
fig, axis = plt.subplots(figsize=figure_size)
plt.subplots_adjust(
    left=0.133, bottom=0.13, right=0.952, top=0.96, hspace=0.2, wspace=0.2
)
axis.xaxis.set_major_locator(MaxNLocator(integer=True))

handles, labels = plt.gca().get_legend_handles_labels()

print(data)

plt.plot(
    n_collectives,
    data["Data Aware"],
    label="DataAware",
    marker=".",
    color="#B3B3B3",
    linewidth=1,
)
plt.plot(
    n_collectives,
    data["Barrier"],
    label="Barrier",
    marker="o",
    color="#6C8EBF",
    linewidth=2,
)
plt.plot(
    n_collectives,
    data["Stellar OP"] + data["Stellar OR"],
    label="Optimal",
    marker="*",
    color="#B85450",
    linewidth=3,
)

# change font and size
label_font = FontProperties()
label_font.set_family("Source Sans Pro")
label_font.set_weight("semibold")
label_font.set_size("12")

# plt.xlabel("Number of Collectives (Broadcasts)", fontproperties=label_font)
plt.ylabel("Problem Solving Time (s)", fontproperties=label_font)
plt.tick_params(labelsize=12)
plt.grid(True)
plt.legend(prop=label_font, loc="best")
plt.show()
figure_filename = "experiment21-results.pdf"
fig.savefig(figure_filename)
