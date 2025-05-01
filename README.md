# CPU Scheduling Simulation 🖥️⌛

Welcome to the **CPU Scheduling Simulation** project! This project aims to simulate various CPU scheduling algorithms for a set of processes, and calculate key performance metrics such as waiting time, turnaround time, and display Gantt charts for the process scheduling. The simulation covers three different scheduling algorithms and runs for a period of 300 time units.

---

## ✨ Description
This program simulates the CPU scheduling of a set of 7 processes using three different scheduling algorithms over a period of 300 time units. For each algorithm, it generates a Gantt chart, computes the average waiting time, and calculates the average turnaround time.

### Problem Overview
Given the following processes with arrival time, CPU burst time, I/O burst time, and priority, the program simulates the scheduling for each process using the following algorithms:
1. **Non-preemptive Priority Scheduling** 🏅
2. **Preemptive Priority Scheduling with Aging** ⏳
3. **Multilevel Feedback Queue Scheduling** 🧠

## 🌟 Features
- **Multiple Scheduling Algorithms**: Supports three different scheduling algorithms for CPU process management.
- **Average Waiting and Turnaround Time**: Automatically calculates and displays the average waiting time and turnaround time for each algorithm.
- **Gantt Chart Generation**: Displays a Gantt chart representing the execution order of processes.
- **Simulations for 300 Time Units**: Simulates the CPU scheduling for a fixed period of 300 time units.
- **Support for Round Robin within Priority**: For processes with the same priority, the program implements Round Robin scheduling with a quantum of `q = 2`.



2. **Prepare Input Data**: 
   The input data for the processes is provided directly in the program (or in a file like `process_data.txt` if preferred). Each process has:
   - Arrival Time
   - CPU Burst Time
   - I/O Burst Time
   - Priority

3. **Run the Program**: 
   After setting up the environment and input data, execute the program to simulate the scheduling.

   Example for Python:
   ```bash
   python process_scheduling.py
   ```

4. **View Results**: 
   The program will generate:
   - Gantt Chart showing the scheduling of processes over time.
   - Average waiting time and average turnaround time for each scheduling algorithm.

## 💡 Code Explanation

### Main Structure:
1. **Process Creation**: The program starts by initializing 7 processes with arrival time, CPU burst time, I/O burst time, and priority.
2. **Scheduler Process**: Another process is responsible for scheduling these processes using the selected algorithm.
3. **Time Simulation**: The system simulates the scheduling over 300 time units, updating the status of each process.
4. **Metrics Calculation**: For each algorithm, the program calculates:
   - **Average Waiting Time**: The time a process spends waiting in the ready queue.
   - **Average Turnaround Time**: The total time a process spends from arrival to completion.

## 🎯 Algorithms Implemented

### 1. **Non-preemptive Priority Scheduling** 🏅
- Processes are executed based on priority.
- If two processes have the same priority, Round Robin is used with `q = 2` for tie-breaking.

### 2. **Preemptive Priority Scheduling with Aging** ⏳
- Priority is decreased by 1 after a process remains in the ready queue for 5 time units.
- If two processes have the same priority, Round Robin is used with `q = 2`.

### 3. **Multilevel Feedback Queue Scheduling** 🧠
- Uses multiple queues with different time quanta and processes move between the queues based on their behavior.

## 📊 Output

- **Gantt Chart**: A visual representation of process execution and CPU allocation.
- **Average Waiting Time**: Displays the average waiting time for all processes under each scheduling algorithm.
- **Average Turnaround Time**: Displays the average turnaround time for all processes under each scheduling algorithm.

Example output:
```
Non-preemptive Priority Scheduling:
- Average Waiting Time: 24.3 ms
- Average Turnaround Time: 35.6 ms
- Gantt Chart: gantt_chart.png

Preemptive Priority Scheduling with Aging:
- Average Waiting Time: 20.4 ms
- Average Turnaround Time: 30.5 ms
- Gantt Chart: gantt_chart.png

Multilevel Feedback Queue Scheduling:
- Average Waiting Time: 22.1 ms
- Average Turnaround Time: 33.2 ms
- Gantt Chart: gantt_chart.png
```

---
## ✍️ Author
Yara Khattab

📧 Email: yarakhattab16@gmail.com


🔗 [GitHub: @yarakhattab](https://github.com/yarakhattab)



