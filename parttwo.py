#yara khattab 1210520

import matplotlib.pyplot as plt
import copy
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

def preemptive_priority_scheduling_with_aging(process_list, total_time):
    time = 0
    current_process = None
    processes = []
    times = []
    ready_queue = deque()
    waiting_queue = {}
    aging_tracker = {}

    while time < total_time:
        for p in process_list:
            if p.arrival_time <= time and not p.has_started:
                ready_queue.append(p)
                p.has_started = True
                aging_tracker[p.name] = 0

        for process, comeback_time in list(waiting_queue.items()):
            if comeback_time <= time:
                aging_tracker[process.name] = 0
                ready_queue.append(process)
                del waiting_queue[process]

        if ready_queue:
            # Group processes with the same priority
            priority_groups = {}
            for p in ready_queue:
                priority_groups.setdefault(p.remaining_priority, []).append(p)

            # Select the process with the highest priority
            highest_priority = min(priority_groups.keys())
            future_process = min(priority_groups[highest_priority], key=lambda p: p.arrival_time)

            # Check if there are multiple processes with the same priority
            if len(priority_groups[highest_priority]) > 1:
                # Apply round-robin scheduling with a time quantum of 2
                future_process = priority_groups[highest_priority][0]  # Choose the first process in the group
                ready_queue.rotate(-1)  # Move the first process to the end of the queue

            if not current_process or current_process.remaining_burst_time == 0:
                if current_process:
                    current_process.remaining_priority = current_process.priority
                    current_process.remaining_burst_time = current_process.burst_time
                    current_process.ready_queue_time = 0
                    current_process.wait_queue_time = 0
                    waiting_queue[current_process] = time + current_process.IO_Bursttime
                current_process = future_process
                current_process.total_ready_queue_time += current_process.ready_queue_time
                current_process.total_wait_queue_time += current_process.wait_queue_time
                ready_queue.remove(current_process)
                processes.append(current_process.name)
                times.append(time)

            elif current_process.remaining_priority > future_process.remaining_priority:
                aging_tracker[current_process.name] = 0
                current_process.ready_queue_time = 0
                current_process.wait_queue_time = 0
                ready_queue.append(current_process)
                current_process = future_process
                current_process.total_ready_queue_time += current_process.ready_queue_time
                current_process.total_wait_queue_time += current_process.wait_queue_time
                ready_queue.remove(current_process)
                processes.append(current_process.name)
                times.append(time)

        for process in ready_queue:
            process.ready_queue_time += 1
        for process in waiting_queue:
            process.wait_queue_time += 1

        if current_process:
            current_process.CPU_time += 1
            current_process.remaining_burst_time -= 1
        time += 1

        for p in ready_queue:
            aging_tracker[p.name] += 1
            if aging_tracker[p.name] == 5:
                p.remaining_priority = max(p.remaining_priority - 1, 0)
                aging_tracker[p.name] = 0

    times.append(total_time)
    print_times(process_list, processes, "Preemptive Priority Scheduling with Aging")
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

# Preemptive Priority Scheduling with Aging
processes, times = preemptive_priority_scheduling_with_aging(copy.deepcopy(process_list), 300)
drawgantchart(processes, times, "Preemptive Priority Scheduling with Aging ", 10)
