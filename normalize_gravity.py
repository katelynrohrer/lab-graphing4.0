import pandas as pd
import numpy as np

# Load accelerometer data into a Pandas DataFrame
data = pd.read_csv('accelerometer_data.csv')

# Extract accelerometer data from the DataFrame
acc_x = data['x']
acc_y = data['y']
acc_z = data['z']

# Determine the direction of gravity
gravity = np.array([0, 0, -1])  # Assuming gravity is in the negative Z direction

# Subtract gravity from the acceleration signal
acc_xyz = np.column_stack((acc_x, acc_y, acc_z))  # Stack the three arrays into a single 2D array
acc_motion = acc_xyz - (np.dot(acc_xyz, gravity) / np.dot(gravity, gravity))[:, None] * gravity

# Normalize the acceleration signal
mag = np.linalg.norm(acc_motion, axis=1)  # Compute the magnitude of the acceleration vector
acc_norm = acc_motion / mag[:, None]  # Divide the acceleration signal by its magnitude

# Convert the normalized acceleration signal back to separate arrays
acc_x_norm = acc_norm[:, 0]
acc_y_norm = acc_norm[:, 1]
acc_z_norm = acc_norm[:, 2]

# Store the normalized accelerometer data back into the original DataFrame
data['x_norm'] = acc_x_norm
data['y_norm'] = acc_y_norm
data['z_norm'] = acc_z_norm

# Save the DataFrame to a CSV file
data.to_csv('normalized_accelerometer_data.csv', index=False)

