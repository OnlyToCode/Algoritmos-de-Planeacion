import random

class Process:
    _first_time = True
    def __init__(self, name, execution_time, priority):
        self.name = name
        self.execution_time = execution_time
        self.priority = priority
        self._arrival_time = None
        self._start_time = None
        self._end_time = None

    def getArrivalTime(self):
        return self._arrival_time
    
    def setArrivalTime(self, arrival_time):
        self._arrival_time = arrival_time

    def getStartTime(self):
        return self._start_time
    
    def setStartTime(self, start_time):
        self._start_time = start_time

    def getEndTime(self):
        return self._end_time
    
    def setEndTime(self, end_time):
        self._end_time = end_time

    def calculateTe(self):
        return self._start_time - self._arrival_time

    def calculateTs(self):
        return self._end_time - self._arrival_time

class Prioridad:
    def __init__(self):
        self.queue = []
        self.current_process = None

    def add_process(self, process, current_time):
        if process.getArrivalTime() is None:
            process.setArrivalTime(current_time)
        self.queue.append(process)
        self.queue.sort(key=lambda p: p.priority)

    def execute(self, current_time):
        print(f"Current Time: {current_time:<3}", end="\t" if self.queue else "\n")
        if self.current_process is None and self.queue:
            self.current_process = self.queue.pop(0)
        if self.current_process:
            process = self.current_process
            if process._first_time:
                process.setStartTime(current_time)
                print(f"{process.name:<10} Arrival Time: {process.getArrivalTime():<5} Execution Time: {process.execution_time:<5} Priority: {process.priority:<5}")
                process._first_time = False
            else:
                print(f"{'':<29} Execution Time: {process.execution_time:<5}")
            process.execution_time -= 1
            if process.execution_time == 0:
                process.setEndTime(current_time + 1)
                self.current_process = None
                return process
        return None

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
    def __init__(self, min_burst_time, max_burst_time):
        self.min_burst_time = min_burst_time
        self.max_burst_time = max_burst_time
        self.process_number = 1

    def generate_processes(self):
        while True:
            execution_time = random.randint(self.min_burst_time, self.max_burst_time)
            priority = random.randint(1, 5)  # Set max priority to 5
            yield Process(f"Process {self.process_number}", execution_time, priority)
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

# Example usage
if __name__ == "__main__":
    generator = ProcessGenerator(min_burst_time=1, max_burst_time=8)
    time = Time(Prioridad(), generator)
    metrics = Metrics()
    time.run()
    for process in time.completed_processes:
        metrics.add_process(process)
    if metrics.processes:
        print(f"Average Te: {metrics.calculate_average_te()}")
        print(f"Average Ts: {metrics.calculate_average_ts()}")
    else:
        print("No processes were completed.")
