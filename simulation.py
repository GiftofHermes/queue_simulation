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
        self.max_wait_time = 0
        self.queue_length = 0
        self.total_arrival = 0
        self.total_served = 0



    def handle_event(self, event):
        event = event[1]
        if event.type == 'arrival':
            self.total_arrival += 1
            self.queue_length += 1
            if self.event_queue:
                max_end_time_event = heapq.nlargest(1,
                             self.event_queue,
                             key=lambda x: x[1].end_time)
                start_time = max_end_time_event[0][1].end_time
            else:
                start_time = self.time
            service = (Service(id=self.event_id,
                               event_time=self.time,
                               start_time=start_time,
                               duration=lambda: np.random.randint(6,10))
                        )
            heapq.heappush(self.event_queue, (service.end_time, service))
            self.event_id += 1
        if event.type == 'service':
            self.queue_length -=1
            self.total_wait_time += self.time - event.event_time
            if self.max_wait_time < self.time - event.event_time:
                self.max_wait_time = self.time - event.event_time
            self.time += event.duration
            self.total_served += 1
        return self

    def __str__(self):
        return (f'Time: {self.time}\n'
               f'queue_length: {self.queue_length}\n'
               f'wait_time: {self.total_wait_time}\n'
               f'average_wait_time: {self.total_wait_time / self.total_arrival}\n'
               f'max_wait_time: {self.max_wait_time}'
              )

class Event(ABC):
    """
    Abstract event class
    """
    type: str = NotImplemented

    def __init__(self, id, event_time, start_time, duration=lambda: 0):
        self.id = id
        self.event_time = event_time
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
