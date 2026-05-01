import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Projectile Motion Calculator")
st.write("Calculate motion parameters with negligible air resistance.")

# 1. Sidebar Navigation (Replaces the 'while True' loop)
formula_choice = st.sidebar.selectbox(
    "Select a Formula",
    ["Position at any time", "Velocity at any time", "Maximum height", 
     "Time of flight", "Horizontal range", "Show trajectory"]
)

# 2. Sidebar Inputs (Global inputs used by most formulas)
u = st.sidebar.number_input("Initial Velocity (m/s)", value=20.0)
theta = st.sidebar.slider("Launch Angle (degrees)", 0, 90, 45)
g = st.sidebar.selectbox("Gravity (m/s²)", [9.8, 10.0])
radian = np.radians(theta)

# 3. Logic for each formula
if formula_choice == "Position at any time":
    x0 = st.number_input("Initial X position (m)", value=0.0)
    y0 = st.number_input("Initial Y position (m)", value=0.0)
    t = st.number_input("Time elapsed (s)", value=1.0)
    
    horiz = x0 + u * np.cos(radian) * t
    vert = y0 + u * np.sin(radian) * t - (0.5 * g * t**2)
    st.success(f"Horizontal Position: {horiz:.2f}m")
    st.success(f"Vertical Position: {vert:.2f}m")

elif formula_choice == "Velocity at any time":
    t = st.number_input("Time (s)", value=1.0)
    Vx = u * np.cos(radian)
    Vy = u * np.sin(radian) - g * t
    M = (Vx**2 + Vy**2)**0.5
    st.success(f"Speed: {M:.2f} m/s")
    st.write(f"Angle: {np.degrees(np.arctan2(Vy, Vx)):.2f} degrees")

elif formula_choice == "Maximum height":
    H = (u**2 * np.sin(radian)**2) / (2 * g)
    st.success(f"Maximum Height: {H:.2f}m")

elif formula_choice == "Time of flight":
    T = (2 * u * np.sin(radian)) / g
    st.success(f"Total time of flight: {T:.2f}s")

elif formula_choice == "Horizontal range":
    R = (u**2 * np.sin(2 * radian)) / g
    st.success(f"Horizontal Range: {R:.2f}m")

elif formula_choice == "Show trajectory":
    x0 = st.number_input("Initial X (m)", value=0.0)
    y0 = st.number_input("Initial Y (m)", value=0.0)
    
    fig, ax = plt.subplots()
    
    if theta == 90:
        a, b, c = -0.5 * g, u, y0
        t_flight = max((-b + np.sqrt(b**2 - 4*a*c)) / (2*a), (-b - np.sqrt(b**2 - 4*a*c)) / (2*a))
        t_range = np.linspace(0, t_flight, 100)
        y_range = y0 + (u * t_range) - (0.5 * g * t_range**2)
        ax.plot(np.full_like(t_range, x0), y_range, label="Vertical Trajectory")
    else:
        # Use Time of Flight to determine how far the graph should go automatically
        t_flight = (2 * u * np.sin(radian)) / g
        x_max = u * np.cos(radian) * t_flight
        x_range = np.linspace(x0, x0 + x_max, 100)
        y_range = y0 + (x_range - x0) * np.tan(radian) - (g * (x_range - x0)**2) / (2 * u**2 * np.cos(radian)**2)
        ax.plot(x_range, y_range, label="Trajectory")

    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Vertical Height (m)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig) # Displays the Matplotlib plot in the browser
