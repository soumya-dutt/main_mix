import glob
import os
import matplotlib.pyplot as plt

# Define the path to the directory where the files are stored
directory_path = "/home/sdutta46/Desktop/Catch_bond/m3s2"

# Define the file pattern you want to search for
pattern1 = "SASA_peptide_withforce*.dat"
pattern2 = "SASA_peptide_withoutforce*.dat"
# Initialize an empty dictionary
data_dict1 = {}
data_dict2 = {}

# Use glob to find files matching the pattern in the specified directory
file_list1 = glob.glob(os.path.join(directory_path, pattern1))

# Loop through the matching files and read and process them
for file_name in file_list1:
    with open(file_name, 'r') as file:
        # Read the content of the file
        file_content = file.read().strip().split(' ')
        print (file_content)
        
        if len(file_content) >= 4:
            # Extract the 3rd and 4th columns as key and value
            key = (file_content[-3] , file_content[-2])
            value = file_content[-1]
            
            # Add the key-value pair to the dictionary
            data_dict1[key] = value

# Use glob to find files matching the pattern in the specified directory
file_list2 = glob.glob(os.path.join(directory_path, pattern2))

# Loop through the matching files and read and process them
for file_name in file_list2:
    with open(file_name, 'r') as file:
        # Read the content of the file
        file_content = file.read().strip().split(' ')
        print (file_content)
        
        if len(file_content) >= 4:
            # Extract the 3rd and 4th columns as key and value
            key = (file_content[-3] , file_content[-2])
            value = file_content[-1]
            
            # Add the key-value pair to the dictionary
            data_dict2[key] = value

# Now, data_dict contains the data from all the files
print(data_dict1)
print(data_dict2)

# Combine the keys from both dictionaries
all_keys = set(data_dict1.keys()).union(data_dict2.keys())

# Sort all_keys based on the key[1] component
sorted_keys = sorted(all_keys, key=lambda key: key[1])

# Create an index for the x-axis based on the sorted keys
x = range(len(sorted_keys))

# Define bar width and gap
bar_width = 0.25
bar_gap = 0.2

# Create the bar graph with custom visual enhancements
plt.figure(figsize=(16, 12))  # Adjust the figure size

# Set the font styles and sizes
plt.rc('font', family='serif', weight='bold')
plt.rc('axes', titlesize=20)
plt.rc('axes', labelsize=16)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

# Create the bar graph with custom colors and other style settings
plt.bar([i - bar_gap for i in x], [float(data_dict1.get(key, 0)) for key in sorted_keys], width=bar_width, label='With Force', color='orangered', edgecolor='black', lw=0.5)
plt.bar([i + bar_gap for i in x], [float(data_dict2.get(key, 0)) for key in sorted_keys], width=bar_width, label='Without Force', color='steelblue', edgecolor='black', lw=0.5)

# Set x-axis labels and rotate them for better readability
x_labels = [f"{key[0]} - {key[1]}" for key in sorted_keys]
plt.xticks(x, x_labels, rotation=45, ha='right', fontsize=20)

# Set the y-axis label and title
plt.ylabel('SASA (Å²)', fontsize=20, weight='bold')
#plt.title('SASA Comparison', fontsize=20, weight='bold')

# Add a legend with custom styles
plt.legend(fontsize=14)

# Save the plot as an image file with higher resolution
plt.savefig("peptide_m3s2_v2.png", dpi=300)

# Show the plot
plt.show()

