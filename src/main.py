from data_io.process_loader import load_processes
from data_io.sync_loader import load_resources, load_actions
from scheduling.fifo import schedule as fifo_schedule
from scheduling.sjf import schedule as sjf_schedule
from scheduling.priority import schedule as priority_schedule
from scheduling.rr import schedule as rr_schedule
from scheduling.srt import schedule as srt_schedule
from synchronization.mutex import simulate as mutex_sim
from synchronization.semaphore import simulate as sem_sim
from core.scheduler import run_scheduling
from core.sync_engine import run_synchronization
from utils.metrics import compute_avg_waiting_time, compute_total_waits

procs = load_processes("data/processes.txt")
# print(procs)
res = load_resources("data/resources.txt")
acts = load_actions("data/actions.txt")
# print(ress, acts)


# result = fifo_schedule(procs)
# print("Timeline FIFO:", result.timeline)
# print("Waiting times:", result.waiting_times)

# res = sjf_schedule(procs)
# print("Timeline SJF:", res.timeline)
# print("Waiting times SJF:", res.waiting_times)

# res = priority_schedule(procs)
# print("Timeline Priority:", res.timeline)
# print("Waiting times Priority:", res.waiting_times)


# res = rr_schedule(procs, quantum=4)
# print("Timeline RR:", res.timeline)
# print("Waiting times RR:", res.waiting_times)

# res = srt_schedule(procs)
# print("Timeline SRT:", res.timeline)
# print("Waiting times SRT:", res.waiting_times)

# mutex_res = mutex_sim(procs, res, acts)
# print("Mutex timeline:", mutex_res.timeline)
# print("Mutex waits:", mutex_res.waiting_counts)

# sem_res = sem_sim(procs, res, acts)
# print("Semaphore timeline:", sem_res.timeline)
# print("Semaphore waits:", sem_res.waiting_counts)

# res_fifo = run_scheduling(procs, 'fifo')
# res_rr  = run_scheduling(procs, 'rr', quantum=3)

# print(res_fifo.timeline, res_fifo.waiting_times)
# print(res_rr.timeline, res_rr.waiting_times)

# sync_res_mutex = run_synchronization(procs, res, acts, mode='mutex')
# print("Mutex waits:", sync_res_mutex.waiting_counts)

# sync_res_sem = run_synchronization(procs, res, acts, mode='semaphore')
# print("Semaphore waits:", sync_res_sem.waiting_counts)

# Scheduling
# sched = run_scheduling(procs, 'rr', quantum=4)
# awt = compute_avg_waiting_time(sched.waiting_times)
# print(f"RR AWT: {awt:.2f}")

# # Synchronization
# sync = run_synchronization(procs, res, acts, mode='mutex')
# total_waits = compute_total_waits(sync.waiting_counts)
# print(f"Total mutex waits: {total_waits}")

