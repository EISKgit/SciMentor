import numpy as np
import matplotlib.pyplot as plt

# Define the population size and initial infected individuals
N = 100000
I0 = 10

# Define the infection rate and recovery rate
beta = 0.2
gamma = 0.1

# Define the time steps and total time
dt = 0.1
t_max = 100

# Initialize the arrays to store the number of susceptible, infected, and recovered individuals
S = np.zeros(int(t_max/dt) + 1)
I = np.zeros(int(t_max/dt) + 1)
R = np.zeros(int(t_max/dt) + 1)

# Initialize the initial conditions
S[0] = N - I0
I[0] = I0
R[0] = 0

# Simulate the spread of the flu
for i in range(int(t_max/dt)):
    S[i+1] = S[i] - beta * S[i] * I[i] / N * dt
    I[i+1] = I[i] + beta * S[i] * I[i] / N * dt - gamma * I[i] * dt
    R[i+1] = R[i] + gamma * I[i] * dt

# Plot the results
plt.plot(np.arange(0, t_max+dt, dt), S, label='Susceptible')
plt.plot(np.arange(0, t_max+dt, dt), I, label='Infected')
plt.plot(np.arange(0, t_max+dt, dt), R, label='Recovered')
plt.xlabel('Time')
plt.ylabel('Number of individuals')
plt.legend()
plt.savefig('flu_outbreak_simulation.png')