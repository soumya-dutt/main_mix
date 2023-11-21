import matplotlib.pyplot as plt

# Prompt user for the name of the .dat file
dat_file_name = input("Enter the name of the .dat file containing RMSF values: ")

# Read the RMSF values from the specified .dat file
rmsf_values = []
with open(dat_file_name, 'r') as file:
    lines = file.readlines()
    for line in lines:
        rmsf_values.append(float(line.strip()))

# Create a beautiful plot
plt.figure(figsize=(10, 6))
plt.plot(rmsf_values, color='green', linewidth=1, label='RMSF')
plt.title('Root-Mean-Square Fluctuation (RMSF) Plot')
plt.xlabel('Resid')
plt.ylabel('RMSF Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Increase the number of tick labels on the x-axis
num_ticks = 30  # You can adjust this number as needed
plt.xticks(range(0, len(rmsf_values), len(rmsf_values) // num_ticks))

# Prompt user for the name of the output image file
output_file_name = input("Enter the name of the output image file (e.g., plot.png): ")

# Save the plot as the user-provided image file name
plt.savefig(output_file_name, dpi=300)

# Show the plot
plt.show()