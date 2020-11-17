from simulation import Simulation, Arrival
import numpy as np
from heapq import heappush, heappop

num_customers = 100
simulation = Simulation()

initial_arrival = Arrival(id=simulation.event_id,
                                      start_time=simulation.time)
heappush(simulation.event_queue,(initial_arrival.end_time, initial_arrival))
simulation.event_id += 1

while simulation.total_served < num_customers:
    future_arrivals = list(filter(lambda x: x[1].type == 'arrival',simulation.event_queue))
    if not future_arrivals:
        arrival = Arrival(id=simulation.event_id,
                                              start_time=simulation.time,
                                              duration=lambda: np.random.poisson(10)
                          )
        heappush(simulation.event_queue, (arrival.end_time, arrival))
        simulation.event_id += 1
    if simulation.event_queue:
        simulation = simulation.handle_event(heappop(simulation.event_queue))
    print(simulation.time)
    print(simulation)
