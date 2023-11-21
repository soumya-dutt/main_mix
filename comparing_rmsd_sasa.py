# Step 1: Read the rmsd file and load its contents
file_path = input("Enter the RMSD file path : ")      # Replace 'your_file.dat' with the actual file path

data = []                       # To store the data from the .dat file
with open(file_path, 'r') as file:
    for line in file:
        values = line.strip().split()
        if len(values) == 2:
            data.append((int(values[0]), float(values[1])))
#print(data)
# Step 2: Get the range of numbers from the user
lower_bound = float(input("Enter the lower bound of the range: "))
upper_bound = float(input("Enter the upper bound of the range: "))

# Step 3: Find index numbers for values within the user-defined range in the second column
indices_within_range1 = []
for index, value in data:
    if lower_bound <= value <= upper_bound:
        indices_within_range1.append(index)

#print(indices_within_range1)
print('done with rmsd file')
# Step 2: Read the sasa file and load its contents
file_path = input("Enter the SASA file path : ")  # Replace 'your_single_column_file.dat' with the actual file path

data = []  # To store the data from the single-column file
with open(file_path, 'r') as file:
    for line in file:
        value = float(line.strip())
        data.append(value)
#print(data)
# Step 2: Get the range of numbers from the user
lower_bound = float(input("Enter the lower bound of the range: "))
upper_bound = float(input("Enter the upper bound of the range: "))

# Step 3: Find index numbers for values within the user-defined range
indices_within_range2 = []
for index, value in enumerate(data):
    if lower_bound <= value <= upper_bound:
        indices_within_range2.append(index)

#print(indices_within_range2)
print('done with sasa file')
# Finding the common numbers between the two

def find_common_numbers(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    common_numbers = list(set1.intersection(set2))
    return common_numbers

result = find_common_numbers(indices_within_range1, indices_within_range2)
#print(result)
print('done with common file')
# Plotting the numbers

import plotly.graph_objects as go

def count_entries(*lists):
    counts = [len(lst) for lst in lists]
    return counts

def plot_histogram(*lists, labels=None):
    if labels is None:
        labels = [f"List {i+1}" for i in range(len(lists))]

    counts = count_entries(*lists)

    # Define custom colors for each bar
    colors = ['rgb(158,202,225)', 'rgb(255,187,120)', 'rgb(144,202,249)']

    fig = go.Figure()

    for i in range(len(labels)):
        fig.add_trace(go.Bar(x=[labels[i]], y=[counts[i]], marker_color=colors[i]))

    fig.update_layout(
        title="Comparison Histogram of Numbers in Lists",
        xaxis_title="Lists",
        yaxis_title="Number of Entries",
        xaxis_tickangle=-45,
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        showlegend=False
    )

    fig.show()

# Provide custom labels for the lists (optional)
custom_labels = ["RMSD", "SASA", "common"]

plot_histogram(indices_within_range1, indices_within_range2, result, labels=custom_labels)


