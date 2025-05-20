# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Scoring functions ---
def score_run(d: float, t: float, h: float) -> float:
    """
    Calculate running score.
    d: distance in kilometers
    t: time in minutes
    h: elevation gain in meters
    Returns 0 if t < 15.
    """
    return 0.0 if t < 15 else (1.1 * d + 0.11 * t + 0.02 * h)

def score_cycle(d: float, t: float, h: float) -> float:
    """
    Calculate cycling score.
    d: distance in kilometers
    t: time in minutes
    h: elevation gain in meters
    Returns 0 if t < 15.
    """
    return 0.0 if t < 15 else 0.5 * (0.75 * d + 0.075 * t + 0.02 * h)

def score_swim(d: float, t: float, h: float = 0.0) -> float:
    """
    Calculate swimming score.
    d: distance in kilometers
    t: time in minutes
    h: elevation gain (ignored)
    Returns 0 if t < 15.
    """
    return 0.0 if t < 15 else 1.5 * (1.5 * d + 0.125 * t)

# --- Streamlit UI ---
st.set_page_config(page_title="Activity Score Calculator", layout="wide")
st.title("Activity Score Calculator")

# Sidebar for inputs
st.sidebar.header("Inputs")
sport = st.sidebar.selectbox("Select Sport:", ["Running", "Cycling", "Swimming"])
d = st.sidebar.number_input("Distance (km)", min_value=0.0, value=5.0)
t = st.sidebar.number_input("Duration (minutes)", min_value=1.0, value=50.0)
h = st.sidebar.number_input("Elevation Gain (meters)", min_value=0.0, value=100.0)

# Calculate and display score
if sport == "Running":
    score = score_run(d, t, h)
elif sport == "Cycling":
    score = score_cycle(d, t, h)
else:
    score = score_swim(d, t, h)

st.metric(label=f"{sport} Score", value=f"{score:.2f} pts")

# --- Score Surface Plot for Selected Sport ---
# Configure ranges based on sport
if sport == "Running":
    times = np.linspace(20, 120, 100)   # 20 to 120 min
    speeds = np.linspace(6, 20, 100)
    S = np.zeros((len(speeds), len(times)))
    for i, sp in enumerate(speeds):
        for j, ti in enumerate(times):
            dist = sp * (ti / 60)
            S[i, j] = score_run(dist, ti, h)
elif sport == "Cycling":
    times = np.linspace(30, 360, 100)  # 30 to 360 min
    speeds = np.linspace(10, 50, 100)
    S = np.zeros((len(speeds), len(times)))
    for i, sp in enumerate(speeds):
        for j, ti in enumerate(times):
            dist = sp * (ti / 60)
            S[i, j] = score_cycle(dist, ti, h)
else:
    times = np.linspace(15, 180, 100)
    speeds = np.linspace(1, 4, 100)
    S = np.zeros((len(speeds), len(times)))
    for i, sp in enumerate(speeds):
        for j, ti in enumerate(times):
            dist = sp * (ti / 60)
            S[i, j] = score_swim(dist, ti)

# Plotting with compact layout and tight margins
fig, ax = plt.subplots(figsize=(5, 3))
cs = ax.contourf(times, speeds, S, levels=20)

# Vertical colorbar to the right
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(cs, cax=cax)
cbar.ax.tick_params(labelsize=6, length=0)
cbar.set_label("Score", fontsize=6)

# Axis labels and title
ax.set_xlabel("Duration (min)", fontsize=6)
ax.set_ylabel("Speed (km/h)", fontsize=6)
ax.set_title(f"{sport} Score Surface @ {h:.0f} m Elevation", fontsize=6)

# Tick labels only, no marks
ax.tick_params(axis='both', which='major', labelsize=6, length=0)

# Tight margins
fig.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.2)

# Render plot
st.pyplot(fig, use_container_width=True)
