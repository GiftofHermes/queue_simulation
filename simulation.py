from abc import ABC
import numpy as np
from collections import deque
import heapq

class Simulation:
    """
        Fill here according to python guidelines
    """
    def __init__(self):
        self.event_id = 0
        self.time = 0.0
        self.event_queue = [] #should be a heapq
        self.num_events = 0
        self.total_wait_time = 0
        self.queue_length = 0
        self.total_served = 0


    def handle_event(self, event):
        event = event[1]
        if event.type == 'arrival':
            self.queue_length += 1
            service = (Service(id=self.event_id,
                                            start_time=self.time,
                                            duration=lambda: np.random.randint(5,15))
                        )
            heapq.heappush(self.event_queue, (service.end_time, service))
            self.event_id += 1
        if event.type == 'service':
            self.queue_length -=1
            self.time += event.duration
            self.total_served += 1
        return self

    def __str__(self):
        return f'Time: {self.time}\n queue_length: {self.queue_length}'

class Event(ABC):
    """
    Abstract event class
    """
    type: str = NotImplemented

    def __init__(self, id, start_time, duration=lambda: 0):
        self.id = id
        self.start_time = start_time
        self.duration = duration() # may change to a function
        self.end_time = self.start_time + self.duration
    pass

    def __lt__(self, other):
        return self.end_time < other.end_time

    def __eq__(self, other):
        return self.end_time == other.end_time

    def __gt__(self, other):
        return self.end_time > other.end_time

class Arrival(Event):
    type = 'arrival'

class Service(Event):
    type = 'service'
