from data_io.process_loader import load_processes
from data_io.sync_loader    import load_resources, load_actions
from synchronization.mutex   import simulate as simulate_mutex
from synchronization.semaphore import simulate as simulate_semaphore

def print_timeline(timeline):
    for cycle, pid, resource, state in timeline:
        print(f"[Cycle {cycle:2d}] {pid:4s} → {resource:3s} : {state}")

def main():
    processes = load_processes("data/processes.txt")
    resources = load_resources("data/resources.txt")
    actions   = load_actions("data/actions.txt")

    print("=== SEMÁFORO ===")
    sem_res = simulate_semaphore(processes, resources, actions)
    print_timeline(sem_res.timeline)
    print("\nWaiting counts:", sem_res.waiting_counts)

    print("\n=== MUTEX ===")
    mut_res = simulate_mutex(processes, resources, actions)
    print_timeline(mut_res.timeline)
    print("\nWaiting counts:", mut_res.waiting_counts)

if __name__ == "__main__":
    main()
