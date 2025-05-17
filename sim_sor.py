from collections import defaultdict
import pandas as pd
import random
import simpy


class Patient:
    def __init__(self, id, priority, arrival_time):
        self.id = id
        self.priority = priority
        self.arrival_time = arrival_time
        self.triage_time = None
        self.seen_by_doctor_time = None
        self.departure_time = None

class SOR:
    def __init__(self, env, n_doctors, n_nurses, n_rooms, dynamic_allocation=False, fast_track=False):
        self.env = env
        self.doctors = simpy.PriorityResource(env, capacity=n_doctors)
        self.nurses = simpy.Resource(env, capacity=n_nurses)
        self.rooms = simpy.Resource(env, capacity=n_rooms)
        self.dynamic_allocation = dynamic_allocation
        self.fast_track = fast_track

        self.stats = []
        self.utilization = defaultdict(float)
        self.last_usage_time = defaultdict(lambda: env.now)

    def update_utilization(self, name, resource):
        now = self.env.now
        busy = len(resource.users)
        self.utilization[name] += busy * (now - self.last_usage_time[name])
        self.last_usage_time[name] = now

    def triage(self, patient):
        with self.nurses.request() as req:
            yield req
            self.update_utilization("nurses", self.nurses)
            triage_time = random.uniform(5, 15)
            yield self.env.timeout(triage_time)
            patient.triage_time = self.env.now

    def see_doctor(self, patient):
        with self.doctors.request(priority=patient.priority) as req:
            yield req
            self.update_utilization("doctors", self.doctors)
            with self.rooms.request() as room_req:
                yield room_req
                self.update_utilization("rooms", self.rooms)
                treatment_time = random.uniform(10, 30)
                yield self.env.timeout(treatment_time)
                patient.seen_by_doctor_time = self.env.now
                patient.departure_time = self.env.now

    def handle_patient(self, patient):
        yield self.env.process(self.triage(patient))

        if self.fast_track and patient.priority == 2:
            yield self.env.timeout(5)  # Fast-track minimal intervention
            patient.departure_time = self.env.now
        else:
            yield self.env.process(self.see_doctor(patient))

        self.stats.append(patient)
