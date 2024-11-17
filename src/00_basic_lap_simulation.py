import sys
import os

module_path = os.path.abspath(os.path.join("."))
sys.path.append(module_path)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from shapely.ops import linemerge
from pathlib import Path
from utils.geojson import load_geojson

# Import race track
TRACK_DIR = Path("track_data")
file_paths = list(TRACK_DIR.glob("*.geojson"))
geometries = load_geojson(file_paths[0])
racing_line = linemerge(geometries)


# Parameters for vehicle simulation
MAX_SPEED = 100  # Max speed (m/s)
ACCELERATION = 14.2  # Acceleration (m/s^2)
BRAKING = -39  # Braking deceleration (m/s^2)
TIME_STEP = 0.1  # Time step for simulation (s)

# Generate distances along the racing line
line_distances = np.linspace(0, racing_line.length, 500)
vehicle_positions = [racing_line.interpolate(dist) for dist in line_distances]

# Simulate vehicle speed along the line
speeds = np.full_like(line_distances, MAX_SPEED / 2)
for i in range(len(speeds)):
    # Simulate braking in corners (example logic)
    if i > 0 and abs(vehicle_positions[i].x - vehicle_positions[i - 1].x) > 0.5:
        speeds[i] = speeds[i - 1] + BRAKING * TIME_STEP
    else:
        speeds[i] = min(MAX_SPEED, speeds[i - 1] + ACCELERATION * TIME_STEP)

# Initialize animation
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(*racing_line.xy, label="Racing Line", color="gray")
(car,) = ax.plot([], [], "ro", label="Car")  # Car marker


# Function to update animation
def update(frame):
    x, y = vehicle_positions[frame].x, vehicle_positions[frame].y
    car.set_data([x], [y])  # Convert to sequences
    return (car,)


# Create animation
num_frames = len(vehicle_positions)
ani = FuncAnimation(
    fig, update, frames=num_frames, interval=TIME_STEP * 1000, blit=True
)

ax.set_title("Racing Simulation")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.legend()
plt.show()
