import datetime

import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog

volume_list = []
level_list = []

before_time = datetime.datetime.now()

print("Importing text file")
print("____________________________________")

root = tk.Tk()
root.withdraw()

filename = filedialog.askopenfilename(title="Select point text file")

try:
    df = np.genfromtxt(filename, delimiter=" ")
    num_cols = df.shape[1]
except:
    try:
        df = np.genfromtxt(filename, delimiter=",")
        num_cols = df.shape[1]
    except:
        try:
            df = np.genfromtxt(filename, delimiter="\t")
            num_cols = df.shape[1]
        except:
            print("Not Uploaded")
            raise SystemExit


print("Uploaded successfully")

if num_cols == 3:
    x, y, z = df[:, 0], df[:, 1], df[:, 2]
elif num_cols == 4:
    x, y, z = df[:, 1], df[:, 2], df[:, 3]
else:
    raise ValueError(f"There are {num_cols} columns in point text data. Should have 3 or 4 columns")

print("____________________________________")

S = int(input("Enter fixed distance between points: "))
print("____________________________________")

if type(S) is str:
    raise TypeError("You entered wrong")

print("For the water volume calculation below a certain level;")
print("Two height levels will be required. Water volumes will be calculated for all intermediate levels at 1 meter intervals!")
print("____________________________________")

max_level = int(input("Enter a height level: ")) + 1
if type(max_level) is str:
    raise TypeError("You entered wrong")
min_level = int(input("Now enter a lower height level: "))
if type(min_level) is str:
    raise TypeError("You entered wrong")

print("____________________________________")

if min_level > max_level:
    raise Exception("You must enter the second value lower")

save_dir = filedialog.askdirectory(title="Select the folder to save")
for height in range(min_level, max_level):
    # Point filter according to input level
    level_list.append(height)
    filtered_points = df[z < height]

    n = len(filtered_points)

    # Volume Calculations
    if num_cols == 3:
        f = height - np.mean(filtered_points[:, 2])
    elif num_cols == 4:
        f = height - np.mean(filtered_points[:, 3])
    area = (((np.sqrt(n) - 1) * S) ** 2)
    volume = area * f
    volume_list.append(volume)

    # Graph points
    fig, ax = plt.subplots(figsize=(8, 6))
    if num_cols == 3:
        ax.scatter(df[:, 0], df[:, 1], c='grey', alpha=0.2)
        scatter = ax.scatter(filtered_points[:, 0], filtered_points[:, 1], c=filtered_points[:, 2], cmap='viridis', s=1)
    elif num_cols == 4:
        ax.scatter(df[:, 1], df[:, 2], c='grey', alpha=0.2)
        scatter = ax.scatter(filtered_points[:, 1], filtered_points[:, 2], c=filtered_points[:, 3], cmap='viridis', s=1)
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_title(f'Z={height}. LEVEL')

    filename = "{}.jpeg".format(height)
    print(f"{filename} it is drawn and the calculations are saved to the text file")
    plt.colorbar(scatter, ax=ax)
    resolution_value = 300
    plt.savefig(f"{save_dir}/{filename}", dpi=resolution_value)

    with open(f"{save_dir}/RESULTS.txt", "a") as dosya:
        dosya.write("_______________________\n")
        dosya.write(f"Height:   {height}\n")
        dosya.write("***********\n")
        dosya.write(f"Number of points below level {height}: {n}\n")
        dosya.write(f"Difference of Z-means from {height}. level: {f:.2f}\n")
        dosya.write("Area: {:,.2f} m2\n".format(area))
        dosya.write("Volume: {:,.2f} m3\n".format(volume))

second = (datetime.datetime.now() - before_time).total_seconds()

with open(f"{save_dir}/RESULTS.txt", "a") as file:
    file.write("_______________________\n\n")
    file.write(f"Total process time: {second:.0f} seconds\n")
    file.write("_______________________\n\n")

file.close()

plt.clf()
x = level_list
y = []
for vol in volume_list:
    y.append(vol/1000000)

yy = min(y) / 3

plt.bar(x, y)
plt.xticks(x)
plt.yticks(y)
plt.ylim(ymin=yy)
plt.ylabel('Volume (million m3)')
plt.xlabel('Water Height Levels (m)')
plt.title('Water Volume Graph')
plt.savefig(f"{save_dir}/{min_level}_{max_level-1}.jpeg")
