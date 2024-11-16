# Queue Simulation Library

This library provides functions to simulate various queueing models, including M/M/1, M/M/1/N, M/M/infinity, M/M/m, and M/G/1 queues. Each function simulates a different queue structure and returns useful metrics for queue analysis, such as the state history, interarrival times, and departure times.

## Functions

### `m_m_1_q(simTime, del_t, arrRate, depRate)`
Simulates an **M/M/1 queue**.
- **Parameters:**
  - `simTime`: Duration of simulation (in seconds).
  - `del_t`: Time increment for simulation steps.
  - `arrRate`: Arrival rate (per unit time).
  - `depRate`: Departure rate (per unit time).
- **Returns:** State of the queue, interarrival times, departure times, and waiting times.

### `m_m_1_N_q(simTime, del_t, arrRate, depRate, N)`
Simulates an **M/M/1/N queue** with a finite buffer.
- **Parameters:**
  - `N`: Buffer size.
- **Other Parameters and Returns:** Same as `m_m_1_q`.

### `m_m_infinite_q(simTime, del_t, arrRate, depRate)`
Simulates an **M/M/infinity queue**, where there is an infinite number of servers.
- **Parameters and Returns:** Same as `m_m_1_q`.

### `m_m_m_q(simTime, del_t, arrRate, depRate, numServers)`
Simulates an **M/M/m queue** with `numServers` servers.
- **Parameters:**
  - `numServers`: Number of servers available.
- **Returns:** State history, interarrival times, departure times, waiting room size, and active servers count.

### `m_g_1(numTotalCustomers, arrRate, depRate, servDist)`
Simulates an **M/G/1 queue** with customizable service times.
- **Parameters:**
  - `numTotalCustomers`: Total number of customers.
  - `servDist`: Service time distribution (`'exponential'`, `'deterministic'`, etc.).
- **Returns:** State history, interarrival times, and service times.

## Auxiliary Functions

### `argmax_less_than(searchArr, threshold)`
Finds the maximum value in `searchArr` less than `threshold`.
- **Parameters:**
  - `searchArr`: Array to search.
  - `threshold`: Upper limit for values.
- **Returns:** Index of the maximum value below `threshold`, or `-1` if none found.

## Usage Example
```python
from queue_simulation import m_m_1_q

# Simulate an M/M/1 queue
simTime = 100  # seconds
del_t = 0.1    # time increment
arrRate = 2    # arrival rate per second
depRate = 3    # departure rate per second

stateHistory, intArrTimes, intDepTimes, individualTimers = m_m_1_q(simTime, del_t, arrRate, depRate)
