import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load data from the .dat file
file_path = 'SASA_bindingsite.dat'
data = np.loadtxt(file_path)

# Generate index numbers
index = np.arange(len(data))

# Plotting the numbers against their index
plt.figure(figsize=(20,10))
#plt.subplot(1, 2, 1)
plt.plot(index, data, marker='o', linestyle='-', color='b')
plt.xlabel('Frames')
plt.ylabel('SASA (A^2)')
plt.title('SASA plot')
#plt.savefig('SASA_bindingsite.png')
# Set maximum number of ticks on x-axis and y-axis
plt.locator_params(axis='x', nbins=25)
plt.locator_params(axis='y', nbins=20)

# Plotting a histogram
plt.figure(figsize=(20,10))
#plt.subplot(1, 2, 2)
plt.hist(data, bins=200, color='r', edgecolor='black')
plt.xlabel('SASA')
plt.ylabel('Frequency')
plt.title('Histogram SASA')

# Set maximum number of ticks on x-axis and y-axis
plt.locator_params(axis='x', nbins=25)
plt.locator_params(axis='y', nbins=20)

plt.tight_layout()
plt.savefig('SASA_histogram.png', dpi=200)  # Save the plot as a PNG image
plt.show()