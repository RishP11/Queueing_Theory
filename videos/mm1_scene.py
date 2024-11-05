from manim import *
import numpy as np

class M_M_1_Queue(Scene):
    def construct(self):
        simTime = 30  # Simulation time in seconds
        arrRate = 0.1  # Arrival rate (customers per second)
        depRate = 0.05  # Departure rate (customers per second)
        global del_t  # Declare del_t globally
        del_t = 1  # Time step for the simulation (1 second)

        # Run the simulation
        queue, intArrTimes, intDepTimes = m_m_1_q(simTime, arrRate, depRate)

        # Create the visual elements
        queue_boxes = []
        max_queue_length = int(np.max(queue))
        for i in range(max_queue_length):
            box = Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.5)
            queue_boxes.append(box)

        # Initial positions of the boxes
        for i, box in enumerate(queue_boxes):
            box.move_to(LEFT * (max_queue_length / 2 - i))

        self.play(*[FadeIn(box) for box in queue_boxes])

        # Animate the queue changes over time
        for t in range(len(queue)):
            current_length = int(queue[t])
            # Update the queue boxes
            for i, box in enumerate(queue_boxes):
                if i < current_length:
                    box.set_fill(opacity=1)
                else:
                    box.set_fill(opacity=0.5)

            self.play(*[FadeIn(box) for box in queue_boxes[:current_length]],
                      *[FadeOut(box) for box in queue_boxes[current_length:]],
                      run_time=1)

            # Add arrival and departure indications
            if t < len(intArrTimes) and t == intArrTimes[t]:
                arrival_indicator = Text("Arrival", color=GREEN).scale(0.5)
                self.play(Write(arrival_indicator))
                self.wait(0.5)
                self.play(FadeOut(arrival_indicator))

            if t < len(intDepTimes) and t == intDepTimes[t]:
                departure_indicator = Text("Departure", color=RED).scale(0.5)
                self.play(Write(departure_indicator))
                self.wait(0.5)
                self.play(FadeOut(departure_indicator))

        self.wait(2)

def m_m_1_q(simTime, arrRate, depRate):
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
    """ 
    import numpy as np

    # To store the inter-arrival and inter-departure times
    intArrTimes = []
    intDepTimes = [] 
    # Timers for arrival and departure
    arrTimer = 0 
    depTimer = 0 
    # Start with an empty queue
    num_runs = int(simTime / del_t)
    queue = np.zeros(num_runs) 
    for i in range(1, num_runs):
        # Flip a coin for arrival  
        isArrival = np.random.binomial(1, min(1, arrRate * del_t))
        # Flip a coin for departure only if there is an arrival
        if queue[i-1] >= 1:
            isDeparture = np.random.binomial(1, min(1, depRate * del_t))
        else:
            isDeparture = 0
        # Update the current state
        queue[i] = queue[i-1] + isArrival - isDeparture
        # Increment the timers for both arrival and departure
        arrTimer += del_t
        depTimer += del_t
        # If there was an arrival record the Inter-arrival time and clear the timer (restart)
        if isArrival:
            intArrTimes.append(arrTimer)
            arrTimer = 0
        # Similarly for departures
        if isDeparture:
            intDepTimes.append(depTimer)
            depTimer = 0 

    return [queue, intArrTimes, intDepTimes]

    