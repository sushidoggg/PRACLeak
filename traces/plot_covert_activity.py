import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def prefix_sum(lst):
    for i in range(1, len(lst)):
        lst[i] += lst[i - 1]
    return lst

def dram_cycle_to_ns(dram_cycle):
    return int(dram_cycle * 0.625)

def cpu_cycle_to_ns(cpu_cycle):
    dram_cycle = cpu_cycle * 3 / 8
    return int(dram_cycle * 0.625)

def read_data(filename, lst_x, lst_y):
    with open(filename, "r") as file:
        for line in file:
            line = line.strip('\n').split(" ")
            lst_x.append(cpu_cycle_to_ns(int(line[0])))
            lst_y.append(cpu_cycle_to_ns(int(line[1])))
            if lst_y[-1] > 500:
                print(lst_x[-1], lst_y[-1], line)

def plot_scatter(ax, lst_x, lst_y):
    ax.scatter(lst_x, lst_y, s=10)
    # ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Mem Access\nLatency (ns)')

    formatter = ticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K")
    ax.xaxis.set_major_formatter(formatter)

NUM_CACHELINE = 16
SIZE_CACHELINE = 64 #64 bytes * 8

base_row = 0
# controller_file = "1rv3_rfm4_controller.out.ch0"
# latency_file = "latency_rfm4.out"
# controller_file = "it200_controller.out.ch0"
# controller_file = "all_test_controller/105.ch0"
controller_file = "c_activity.ch0"
latency_file = "latency_cov_activity.out"

with open(controller_file, "r") as file:
    lines = file.readlines()

MAX_TIME = dram_cycle_to_ns(int(lines[-1].split(", ")[0])) // 1000 + 1
print(MAX_TIME)
counts = [[0] * MAX_TIME for _ in range(NUM_CACHELINE)]
# RFMcounts = [0] * MAX_TIME
time_list = [i for i in range(MAX_TIME)]
rfmx, rfmy = [], []

for i in range(len(lines) - 1):
    line = lines[i].split(", ")

    time = dram_cycle_to_ns(int(line[0])) // 1000

    if line[1] == "RFMab":
        # RFMcounts[time] += 1
        rfmx.append(time)
        rfmy.append(1)
        continue
    elif line[1] != "ACT":
        continue
    
    cacheline = (int(line[3]) << 5) | (int(line[4]) << 2) | int(line[5])
    row = int(line[6])
    if cacheline > 16 or row != base_row:
        continue
    counts[cacheline][time] += 1


# Create the plot
fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(6,6), gridspec_kw={'height_ratios': [0.8, 0.5, 1]})

ax1.sharex(ax2)
# Plot Latency
x1, y1 = [], []
read_data(latency_file, x1, y1)
plot_scatter(ax0, x1, y1)
ax0.set_ylim(0, 2000)
ax1.set_ylim(0, 1.5)

# Plot RFM counts
# ax1.plot(time_list, prefix_sum(RFMcounts), 'g', label='RFM')
ax1.stem(rfmx, rfmy)

# Plot ACT counts
ax2.plot(time_list, prefix_sum(counts[0]), label="Cacheline"+str(i))
ax2.axhline(y=512, color='r', linestyle=':')

# left_cutoff = 289
# right_cutoff = 325
# ax2.axvspan(0, left_cutoff, color="khaki", alpha=0.5, label="Left region")
# # ax2.axvspan(left_cutoff, right_cutoff, color="white", alpha=0.5, label="Middle region")
# ax2.axvspan(right_cutoff, max(time_list), color="lightcoral", alpha=0.5, label="Right region")

formatter = ticker.FuncFormatter(lambda x, _: f"{int(x)}K")
ax1.xaxis.set_major_formatter(formatter)
ax2.xaxis.set_major_formatter(formatter)

# ax1.set_xlabel('Time (ns)')
ax1.set_ylabel('RFM Count')
ax2.set_xlabel('Time (ns)')
ax2.set_ylabel('Activation Count')
ax2.set_title("")

# Annotations
# plt.figtext(0.14, 0.3, r"$\text{N}_\text{BO}$ = 256", fontsize=12, color="red")
# plt.figtext(0.17, 0.37, "Victim Activations", fontsize=12, color="black")
# plt.figtext(0.50, 0.37, "Adversary Activations", fontsize=12, color="black")
# plt.figtext(0.7, 0.28, "Row 0", fontsize=12, color="#1f77b4")
# plt.figtext(0.7, 0.14, "Other rows", fontsize=12, color="#1f77b4")
# ax0.annotate(
#     "ABO",
#     xy=(682958, 1580),
#     xytext=(-50, -5),
#     textcoords='offset points',
#     arrowprops=dict(arrowstyle="->", color="red", lw=2),
#     color="red",
#     fontsize=12,
#     # fontweight='bold'
# )

# plt.legend()
plt.subplots_adjust(hspace=0.5)
plt.savefig('histogram.png', dpi=300, bbox_inches='tight')
plt.savefig('Fig5.pdf', bbox_inches='tight')
