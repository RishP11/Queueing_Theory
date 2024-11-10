import numpy as np

def m_m_1_q(simTime, del_t, arrRate, depRate):
    """ 
    Function to simulate an M/M/1 queue.
    Just input 
    1. simTime = Time duration (in seconds) that you would like to simulate the queue for.
    2. arrRate = The arrival rate (per unit time)
    3. depRate = The departure rate (per unit time)

    You will get as output 3 lists.
    1. The state of the queue at time t = 0, delT, 2delT, 3delT, and so on.
    2. The interarrival times.
    3. The departure times.   
    4. The individual "waiting times".(i.e., the time required to wait in the queue + the time to get served). 
    """ 
    # To store the inter-arrival and inter-departure times
    intArrTimes = []
    intDepTimes = [] 
    
    # Timers for arrival and departure
    arrTimer = 0 
    depTimer = 0 

    # Start with an empty queue :: Stores the state of the queue at [t=0, t=delT, t=2delT, t=3delT, ...]
    num_runs = int(simTime / del_t)
    stateHistory = np.zeros(num_runs, dtype=int)            
    
    # Individual customer timer and tracking ID (ID corresponds to the one being served).
    individualTimers = []
    customerID = 0                                

    for i in range(1, num_runs):
        # Flip a coin for an arrival  
        isArrival = np.random.binomial(1, min(1, arrRate * del_t))
        # Flip a coin for departure only if there is atleast one customer
        if stateHistory[i-1] >= 1:
            isDeparture = np.random.binomial(1, min(1, depRate * del_t))
        else:
            isDeparture = 0

        # Update the current state
        stateHistory[i] = stateHistory[i-1] + isArrival - isDeparture
        
        # Increment the timers for both inter-arrival and inter-departure
        arrTimer += del_t
        depTimer += del_t
        # Increment the individual customer timers (for all those in the queue (incl. one in service))
        for idx in range(customerID, len(individualTimers)):
            individualTimers[idx] += del_t

        if isArrival:
            intArrTimes.append(arrTimer)        # Record the inter-arrival timer reading
            arrTimer = 0                        # Reset the timer for the same
            individualTimers.append(0)          # Add a new timer for new customer
        # Similarly for departures
        if isDeparture:
            intDepTimes.append(depTimer)        # Record the inter-departure timer reading
            depTimer = 0                        # Reset the timer for the same
            customerID += 1                     # Move on to the next customer.

    return [stateHistory, intArrTimes, intDepTimes, individualTimers]

def m_m_1_N_q(simTime, del_t, arrRate, depRate, N):
    """ 
    Function to simulate an M/M/1/N queue.
    Just input 
    1. simTime = Time duration (in seconds) that you would like to simulate the queue for.
    2. arrRate = The arrival rate (per unit time)
    3. depRate = The departure rate (per unit time)
    4. N       = Buffer size
    You will get as output 3 lists.
    1. The state of the queue at time t = 0, delT, 2delT, 3delT, and so on.
    2. The interarrival times.
    3. The departure times.    
    """ 
    # To store the inter-arrival and inter-departure times
    intArrTimes = []
    intDepTimes = [] 
    
    # Timers for arrival and departure
    arrivalTimer = 0 
    departureTimer = 0 

    # Start with an empty queue
    num_runs = int(simTime / del_t)
    stateHistory = np.zeros(num_runs, dtype=int) 
    
    # Individual customer timer and tracking ID
    individualTimers = []
    customerID = 0                                

    for i in range(1, num_runs):
        # Flip a coin for arrival  
        if stateHistory[i-1] >= N:
            isArrival = 0                               # Queue full : turn down the new arrival(s)
        else:
            isArrival = np.random.binomial(1, min(1, arrRate * del_t))
        # Flip a coin for departure only if there is atleast one customer
        if stateHistory[i-1] >= 1:
            isDeparture = np.random.binomial(1, min(1, depRate * del_t))
        else:
            isDeparture = 0

        # Update the current state
        stateHistory[i] = stateHistory[i-1] + isArrival - isDeparture

        # Increment the timers for both arrival and departure
        arrivalTimer += del_t
        departureTimer += del_t
        
        for idx in range(customerID, len(individualTimers)):
            individualTimers[idx] += del_t
        
        if isArrival:
            intArrTimes.append(arrivalTimer)                # Record the interarrival time
            arrivalTimer = 0                                # Reset the timer for the same
            individualTimers.append(0)                  # Add a timer for the new customer
        # Similarly for departures
        if isDeparture:
            intDepTimes.append(departureTimer)                # Record the interdeparture time
            departureTimer = 0                                # Reset the timer for the same
            customerID += 1                             # Take on the next customer for service.

    return [stateHistory, intArrTimes, intDepTimes, individualTimers]

def m_m_infinite_q(simTime, del_t, arrRate, depRate):
    """ 
    Function to simulate an M/M/infinity queue.
    Just input 
    1. simTime = Time duration (in seconds) that you would like to simulate the queue for.
    2. arrRate = The arrival rate (per unit time)
    3. depRate = The departure rate (per unit time)
    
    You will get as output 3 lists.
    1. The state of the queue at time t = 0, delT, 2delT, 3delT, and so on.
    2. The interarrival times.
    3. The departure times.    
    """ 
    # To store the inter-arrival and inter-departure times
    intArrTimes = []
    intDepTimes = [] 
    
    # Timers for arrival and departure
    arrTimer = 0 
    depTimer = 0 

    # Start with an empty queue
    num_runs = int(simTime / del_t)
    stateHistory = np.zeros(num_runs, dtype=int) 
    
    # Individual customer timer and tracking ID
    individualTimers = []
    customerID = 0                      # For tracking purposes
    activeIDs = []                      # Will keep a record of customers currently at the server 

    for i in range(1, num_runs):
        # Flip a coin for arrival
        isArrival = np.random.binomial(1, min(1, arrRate * del_t))
        # Flip a coin for departure only if there is atleast 1 customer
        if stateHistory[i-1] >= 1:
            # Create a departures list
            isDepartures = [np.random.binomial(1, min(1, depRate * del_t)) for _ in range(stateHistory[i-1])]
        else:
            isDepartures = [] 
        
        # Update the current state
        stateHistory[i] = stateHistory[i-1] + isArrival - np.sum(isDepartures)
        
        # Increment the timers for arrival 
        arrTimer += del_t
        for idx in activeIDs:
            individualTimers[idx] += del_t
        
        # Similarly for departures
        depTimer += del_t
        if np.sum(isDepartures):
            intDepTimes.append(depTimer)
            depTimer = 0                    # Reset the timer  
        
        # Keep only the unserved IDs in the active ID list
        tempIDs = [activeIDs[i] for i in range(len(isDepartures)) if isDepartures[i] == 0]
        activeIDs = tempIDs
        
        # If there was an arrival record the Inter-arrival time and clear the timer (restart)
        if isArrival:
            intArrTimes.append(arrTimer)
            arrTimer = 0
            individualTimers.append(0)      # Add a new customer timer
            activeIDs.append(customerID)    # Add him to the activeIDs
            customerID += 1                 # Next customerID
    
    return [stateHistory, intArrTimes, intDepTimes, individualTimers]

def m_m_m_q(simTime, del_t, arrRate, depRate, numServers):
    """ 
    Function to simulate an M/M/m queue.
    Just input 
    1. simTime = Time duration (in seconds) that you would like to simulate the queue for.
    2. arrRate = The arrival rate (per unit time)
    3. depRate = The departure rate (per unit time)
    4. numServers = Number of servers in the system

    You will get as output 3 lists.
    1. The state of the queue at time t = 0, delT, 2delT, 3delT, and so on.
    2. The interarrival times.
    3. The departure times.    
    """ 
    waiting_room_state = []
    server_room_state = []

    # To store the inter-arrival and inter-departure times
    intArrTimes = []
    intDepTimes = [] 
    
    # Timers for arrival and departure
    arrTimer = 0 
    depTimer = 0 

    # Start with an empty queue
    num_runs = int(simTime / del_t)
    stateHistory = np.zeros(num_runs, dtype=int) 
    
    # Individual customer timer and tracking ID
    individualTimers = []
    customerID = 0                        # For tracking purposes
    activeIDs = []                        # A record of customers currently being served
    waitingIDs = []                       # A record of customers in the waiting "room"

    for i in range(1, num_runs):
        # Flip a coin for arrival
        isArrival = np.random.binomial(1, min(1, arrRate * del_t))
        
        # Flip a coin for departure only if there is atleast 1 customer
        if stateHistory[i-1] >= 1:
            # Create a departures list of indices
            isDepartures = [np.random.binomial(1, min(1, depRate * del_t)) for _ in range(len(activeIDs))]
        else:
            isDepartures = []
        
        # Update the current state
        stateHistory[i] = stateHistory[i-1] + isArrival - np.sum(isDepartures)
        
        # Increment the timers for both arrival and departure
        arrTimer += del_t
        for idx in activeIDs:
            individualTimers[idx] += del_t

        depTimer += del_t
        if isDepartures:
            intDepTimes.append(depTimer)        # Record the inter-departure time 
            depTimer = 0                        # Reset the timer

        # Keep only the unserved IDs in the active ID list
        tempIDs = [activeIDs[i] for i in range(len(isDepartures)) if isDepartures[i] == 0]
        activeIDs = tempIDs
        
        # If there was an arrival 
        if isArrival:
            intArrTimes.append(arrTimer)        # Record the Inter-arrival time
            arrTimer = 0                        # Reset the timer
            individualTimers.append(0)          # Add a custom timer for the new customer

            if len(activeIDs) == numServers :
            # No free server :: Put the arrival in the waiting room 
                waitingIDs.append(customerID)
            else:
            # Send to a free server
                activeIDs.append(customerID)
            customerID += 1

        waiting_room_state.append(len(waitingIDs))
        server_room_state.append(len(activeIDs)) 
        
    return [stateHistory, intArrTimes, intDepTimes, individualTimers, waiting_room_state, server_room_state]