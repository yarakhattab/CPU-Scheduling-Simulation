#yara khattab 1210520

import matplotlib.pyplot as plt
import copy  # Used for creating deep copies of objects
from collections import deque

class Process:
    def __init__(self, name, arrival_time, burst_time, priority, IO_Bursttime):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.IO_Bursttime = IO_Bursttime
        self.remaining_burst_time = burst_time
        self.remaining_priority = priority
        self.total_ready_queue_time = 0
        self.total_wait_queue_time = 0
        self.ready_queue_time = 0
        self.wait_queue_time = 0
        self.CPU_time = 0
        self.has_started = False

def drawgantchart(processes, times, title, size):
    combinations = [(processes[i], times[i + 1] - times[i], times[i]) for i in range(len(processes))]
    combinations.sort(key=lambda x: (x[0], x[2]))

    color_map = plt.get_cmap('tab10')
    fig, ax = plt.subplots(figsize=(17, 7), dpi=70)

    for index, (process, duration, start) in enumerate(combinations):
        process_color = color_map(int(process.split()[-1]) % 10)
        ax.barh(process, duration, left=start, color=process_color)
        ax.axvline(x=start + duration, linestyle='--', linewidth=0.5)

    ax.set_ylabel('Processes')
    ax.set_xlabel('Timeline')
    ax.set_xticks(times)
    ax.set_xticklabels(times, fontsize=size, rotation='vertical')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()

def non_preemptive_priority_scheduling_with_rr(process_list, total_time):
    time = 0
    current_process = None
    processes = []
    times = []
    ready_queue = deque()
    waiting_queue = {}
    quantum = 2
    round_robin_queue = deque()

    while time < total_time:
        for p in process_list:
            if p.arrival_time <= time and not p.has_started:
                ready_queue.append(p)
                p.has_started = True

        for process, comeback_time in list(waiting_queue.items()):
            if comeback_time <= time:
                ready_queue.append(process)
                del waiting_queue[process]

        if not current_process or current_process.remaining_burst_time == 0:
            if current_process:
                current_process.remaining_priority = current_process.priority
                current_process.remaining_burst_time = current_process.burst_time
                current_process.ready_queue_time = 0
                current_process.wait_queue_time = 0
                waiting_queue[current_process] = time + current_process.IO_Bursttime

            if ready_queue:
                min_priority = min(ready_queue, key=lambda p: p.remaining_priority).remaining_priority
                same_priority_processes = [p for p in ready_queue if p.remaining_priority == min_priority]
                if len(same_priority_processes) > 1:
                    round_robin_queue.extend(same_priority_processes)
                    for p in same_priority_processes:
                        ready_queue.remove(p)
                    current_process = round_robin_queue.popleft()
                else:
                    current_process = ready_queue.popleft()
                current_process.total_ready_queue_time += current_process.ready_queue_time
                current_process.total_wait_queue_time += current_process.wait_queue_time
                processes.append(current_process.name)
                times.append(time)

        for process in ready_queue:
            process.ready_queue_time += 1
        for process in waiting_queue:
            process.wait_queue_time += 1

        if current_process:
            current_process.CPU_time += 1
            current_process.remaining_burst_time -= 1
            quantum -= 1
            if current_process.remaining_burst_time == 0 or quantum == 0:
                if current_process.remaining_burst_time > 0:
                    round_robin_queue.append(current_process)
                quantum = 2

        time += 1

    times.append(total_time)
    print_times(process_list, processes, "Non Preemptive Priority Scheduling with Round Robin")
    return processes, times

def print_times(process_list, processes, title):
    total_wait_time = 0
    total_turnaround_time = 0
    number_of_process = 0

    print(title, ":")

    for process in process_list:
        if process.name in processes:
            number_of_process += 1
            total_wait_time += process.total_ready_queue_time
            total_turnaround_time += process.CPU_time + process.total_ready_queue_time + process.total_wait_queue_time
            print(process.name, ": wait time=", process.total_ready_queue_time, "turnaround time=", process.CPU_time + process.total_ready_queue_time + process.total_wait_queue_time)

    print("Avg wait time:", total_wait_time / float(number_of_process))
    print("Avg turnaround time:", total_turnaround_time / float(number_of_process), "\n\n")

# Define a list of processes with their attributes (name, arrival time, burst time, priority, comeback time)
process_list = [
    Process("Process 1", 0, 15, 5, 3),
    Process("Process 2", 1, 23, 14, 2),
    Process("Process 3", 3, 14, 6, 3),
    Process("Process 4", 4, 16, 15, 1),
    Process("Process 5", 6, 10, 13, 0),
    Process("Process 6", 7, 22, 4, 1),
    Process("Process 7", 8, 28, 10, 2)
]

# Non-Preemptive Priority Scheduling with Round Robin for same priority processes
processes, times = non_preemptive_priority_scheduling_with_rr(copy.deepcopy(process_list), 300)
drawgantchart(processes, times, "Non Preemptive Priority Scheduling with Round Robin", 10)
