#yara khattab 1210520

import matplotlib.pyplot as plt
from collections import deque

class Process:
    def __init__(self, pid, arrival_time, cpu_burst_time, io_burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_burst_time = cpu_burst_time
        self.io_burst_time = io_burst_time
        self.remaining_cpu_burst = cpu_burst_time
        self.completed = False
        self.turnaround_time = 0
        self.waiting_time = 0

def drawgantchart(gantt_chart, title, size):
    color_map = plt.get_cmap('tab10')
    fig, ax = plt.subplots(figsize=(17, 7), dpi=70)

    for index, (start, pid) in enumerate(gantt_chart):
        process_color = color_map(pid % 10)
        ax.barh(str(pid), 1, left=start, color=process_color)

    ax.set_ylabel('Processes')
    ax.set_xlabel('Timeline')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()

def multilevel_feedback_queue_scheduling(processes, total_time):
    queue1 = deque()
    queue2 = deque()
    queue3 = deque()

    time = 0
    gantt_chart = []

    while time < total_time or queue1 or queue2 or queue3:
        for p in processes:
            if p.arrival_time == time:
                queue1.append(p)

        if queue1:
            current_queue = queue1
            quantum = 2
        elif queue2:
            current_queue = queue2
            quantum = 4
        elif queue3:
            current_queue = queue3
            quantum = 8
        else:
            time += 1
            continue

        current_process = current_queue.popleft()
        run_time = min(current_process.remaining_cpu_burst, quantum)
        for _ in range(run_time):
            gantt_chart.append((time, current_process.pid))
            current_process.remaining_cpu_burst -= 1
            time += 1
            if current_process.remaining_cpu_burst == 0:
                if current_process.io_burst_time > 0:
                    time += current_process.io_burst_time
                current_process.completed = True
                break

        if not current_process.completed:
            if current_queue == queue1:
                queue2.append(current_process)
            elif current_queue == queue2:
                queue3.append(current_process)
            else:
                queue3.append(current_process)

    for p in processes:
        if not p.completed:
            p.turnaround_time = total_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.cpu_burst_time

    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)

    print("Process\tWaiting Time\tTurnaround Time")
    for p in processes:
        print(f"{p.pid}\t{p.waiting_time}\t\t{p.turnaround_time}")

    return gantt_chart, avg_waiting_time, avg_turnaround_time

#  here Define a list of processes with their attributes (pid, arrival time, cpu burst time, io burst time)
processes = [
    Process(1, 0, 15, 3),
    Process(2, 1, 23, 2),
    Process(3, 3, 14, 3),
    Process(4, 4, 16, 1),
    Process(5, 6, 10, 0),
    Process(6, 7, 22, 1),
    Process(7, 8, 28, 2)
]

# Total time for the scheduling
total_time = 300

# Run Multilevel Feedback Queue Scheduling
gantt_chart, avg_waiting_time, avg_turnaround_time = multilevel_feedback_queue_scheduling(processes, total_time)

# Draw Gantt chart
drawgantchart(gantt_chart, "Multilevel Feedback Queue Scheduling", 10)

# Print average waiting time and turnaround time
print("\nAverage Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)
