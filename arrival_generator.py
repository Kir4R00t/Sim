from sim_sor import SOR, Patient
import simpy
import random

# Generowanie 'napływui' pacjentów do szpitala
def patient_arrivals(env, hospital, lam, duration):
    id_counter = 0
    while env.now < duration:
        arrival_rate = lam(env.now)
        time_until_next = random.expovariate(arrival_rate / 60.0)
        yield env.timeout(time_until_next) # Czekaj na kolejnego pacjenta
        
        priority = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2])[0]
        patient = Patient(id=id_counter, priority=priority, arrival_time=env.now)
        env.process(hospital.handle_patient(patient))
        id_counter += 1

def run_simulation(n_doctors=3, n_nurses=5, n_rooms=2, duration=720, dynamic_allocation=False, fast_track=False):
    env = simpy.Environment()
    hospital = SOR(env, n_doctors, n_nurses, n_rooms, dynamic_allocation, fast_track)

    def arrival_lambda(time):
        if 480 <= time <= 840:  # 8:00 to 14:00
            return 10
        elif 960 <= time <= 1320:  # 16:00 to 22:00 (godziny szczytu)
            return 20
        else:
            return 5

    env.process(patient_arrivals(env, hospital, arrival_lambda, duration))
    env.run(until=duration)

    return hospital.stats, hospital.utilization, duration
