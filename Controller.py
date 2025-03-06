import random
from FiFo import FIFO, Process as FIFOProcess
from SJF import SJF, Process as SJFProcess
from Prioridad import Prioridad, Process as PrioridadProcess

class Time:
    def __init__(self, algorithm, generator):
        self.current_time = 0
        self.algorithm = algorithm
        self.generator = generator
        self.completed_processes = []

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def get_algorithm(self):
        return self.algorithm

    def set_generator(self, generator):
        self.generator = generator

    def get_generator(self):
        return self.generator

    def add_process(self, process):
        self.algorithm.add_process(process, self.current_time)

    def run(self):
        max_cycles = 30
        process_generator = self.generator.generate_processes()
        while self.current_time < max_cycles or self.algorithm.queue:
            if random.random() < 0.3 and self.current_time < max_cycles:
                new_process = next(process_generator)
                self.add_process(new_process)
            completed_process = self.algorithm.execute(self.current_time)
            if completed_process:
                self.completed_processes.append(completed_process)
            self.current_time += 1

class ProcessGenerator:
    def __init__(self, min_burst_time, max_burst_time, process_class, min_priority=None, max_priority=None):
        self.min_burst_time = min_burst_time
        self.max_burst_time = max_burst_time
        self.process_class = process_class
        self.min_priority = min_priority
        self.max_priority = max_priority
        self.process_number = 1

    def generate_processes(self):
        while True:
            execution_time = random.randint(self.min_burst_time, self.max_burst_time)
            if self.min_priority is not None and self.max_priority is not None:
                priority = random.randint(self.min_priority, self.max_priority)
                yield self.process_class(f"Process {self.process_number}", execution_time, priority)
            else:
                yield self.process_class(f"Process {self.process_number}", execution_time)
            self.process_number += 1

class Metrics:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def calculate_average_te(self):
        total_te = sum(process.calculateTe() for process in self.processes)
        return total_te / len(self.processes)

    def calculate_average_ts(self):
        total_ts = sum(process.calculateTs() for process in self.processes)
        return total_ts / len(self.processes)

class Gestor:
    def __init__(self, algorithm):
        self.time = None
        self.algorithm = None
        self.generator = None
        self.fifo_generator = None
        self.sjf_generator = None
        self.prioridad_generator = None
        self.current_algorithm = None
        self.initialize_generators(min_burst_time=1, max_burst_time=8)
        self._initialize_time(algorithm, type(algorithm).__name__)

    def _initialize_time(self, algorithm, generatorName):
        self.algorithm = algorithm
        self.generator = generatorName
        self.time = Time(algorithm, self.get_generator())
        self.current_algorithm = type(algorithm).__name__

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        self.current_algorithm = type(algorithm).__name__
        if self.time:
            self.time.current_time = 0  # Reiniciar el tiempo
            self.time.set_algorithm(algorithm)
            self.time.completed_processes = []  # Limpiar lista de procesos completados
            self.generator = self.current_algorithm
            self.update_generator()

    def get_algorithm(self):
        return self.algorithm

    def set_generator(self, generator_name):
        self.generator = generator_name
        self.update_generator()

    def get_generator(self):
        if self.generator == "FIFO":
            return self.fifo_generator 
        elif self.generator == "SJF":
            return self.sjf_generator
        elif self.generator == "Prioridad":
            return self.prioridad_generator

        return [self.generator, self.fifo_generator, self.sjf_generator, self.prioridad_generator]

    def initialize_generators(self, min_burst_time, max_burst_time):
        self.fifo_generator = ProcessGenerator(min_burst_time, max_burst_time, FIFOProcess)
        self.sjf_generator = ProcessGenerator(min_burst_time, max_burst_time, SJFProcess)
        self.prioridad_generator = ProcessGenerator(min_burst_time, max_burst_time, PrioridadProcess, min_priority=1, max_priority=5)

    def update_generator(self):
        if self.generator == "FIFO":
            self.time.set_generator(self.fifo_generator)
        elif self.generator == "SJF":
            self.time.set_generator(self.sjf_generator)
        elif self.generator == "Prioridad":
            self.time.set_generator(self.prioridad_generator)

    def run(self):
        if self.time:
            self.time.run()

# Example usage
if __name__ == "__main__":
    gestor = Gestor(FIFO())
    
    # FIFO Example
    print("\nRunning FIFO Algorithm")
    print("-" * 50)
    fifo_metrics = Metrics()
    gestor.run()
    print(f"Completed processes in FIFO: {len(gestor.time.completed_processes)}")
    for process in gestor.time.completed_processes:
        fifo_metrics.add_process(process)
    if fifo_metrics.processes:
        print(f"FIFO - Average Te: {fifo_metrics.calculate_average_te()}")
        print(f"FIFO - Average Ts: {fifo_metrics.calculate_average_ts()}")
    else:
        print("FIFO - No processes were completed.")
    print("\n")

    # SJF Example
    print("Running SJF Algorithm")
    print("-" * 50)
    gestor.set_algorithm(SJF())
    sjf_metrics = Metrics()
    gestor.run()
    print(f"Completed processes in SJF: {len(gestor.time.completed_processes)}")
    for process in gestor.time.completed_processes:
        sjf_metrics.add_process(process)
    if sjf_metrics.processes:
        print(f"SJF - Average Te: {sjf_metrics.calculate_average_te()}")
        print(f"SJF - Average Ts: {sjf_metrics.calculate_average_ts()}")
    else:
        print("SJF - No processes were completed.")
    print("\n")

    # Prioridad Example
    print("Running Prioridad Algorithm")
    print("-" * 50)
    gestor.set_algorithm(Prioridad())
    prioridad_metrics = Metrics()
    gestor.run()
    print(f"Completed processes in Prioridad: {len(gestor.time.completed_processes)}")
    for process in gestor.time.completed_processes:
        prioridad_metrics.add_process(process)
    if prioridad_metrics.processes:
        print(f"Prioridad - Average Te: {prioridad_metrics.calculate_average_te()}")
        print(f"Prioridad - Average Ts: {prioridad_metrics.calculate_average_ts()}")
    else:
        print("Prioridad - No processes were completed.")
    print("\n")
