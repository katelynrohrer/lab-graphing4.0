import pandas as pd
import os
import matplotlib.pyplot as plt

# choose the file
result = os.popen('gum file')
chosen_file = result.readline()[:-1]
result.close()

df = pd.read_csv(chosen_file)

# create the column choices
command = "gum choose"
for col in df.columns:
    command += f' "{col}"'

# which column to be the x axis
result = os.popen(command)
x_choice = result.readline()[:-1]
result.close()

# which column to be the y axis
result = os.popen(command)
y_choice = result.readline()[:-1]
result.close()

# choose the type of graph
result = os.popen("gum choose scatter line")
graph_choice = result.readline()[:-1]
result.close()

# plot the graph
df.plot(x=x_choice, y=y_choice, kind=graph_choice)
plt.show()
