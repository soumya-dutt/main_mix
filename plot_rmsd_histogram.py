import matplotlib.pyplot as plt
import numpy as np

# Read data from the .dat file
file_path = 'trajrmsd_ploop.dat'
data = np.loadtxt(file_path)

# Extract columns
index = data[:, 0]
values = data[:, 1]

# Plot the data as a line plot
plt.figure(figsize=(16, 8))
plt.plot(index, values, marker='o', markersize=1, linestyle='-', color='b', linewidth=0.5)
plt.xlabel('Frames')
plt.ylabel('RMSD ploop in A')
plt.title('RMSD plot')

# Adjust the number of ticks on the x-axis and y-axis
plt.locator_params(axis='x', nbins=25 , tight=False)
plt.locator_params(axis='y', nbins=20)

#plt.grid(True)

# Save the line plot as a PNG image
line_plot_filename = 'rmsd_ploop.png'
plt.savefig(line_plot_filename)

# Plot a histogram of the data
plt.figure(figsize=(16, 8))
plt.hist(values, bins=100, color='r', edgecolor='black')
plt.xlabel('RMSD ploop')
plt.ylabel('Frequency')
plt.title('Histogram')

# Adjust the number of ticks on the x-axis
plt.locator_params(axis='x', nbins=25)
plt.locator_params(axis='y', nbins=20)

#plt.grid(True)

# Save the histogram plot as a PNG image
histogram_filename = 'ploop_rmsd_histogram.png'
plt.savefig(histogram_filename)
plt.show()