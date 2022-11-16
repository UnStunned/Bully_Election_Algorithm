import random
import math


class Machine:
    def __init__(self, id):
        self.network_ID = id
        self.status = "ON"
        self.coordinator_index = False

    def change_status(self, inp = None):
        if inp == "ON":
            self.status = "ON"
        elif inp == "OFF":
            self.status = "OFF"
        else:
            if self.status == "ON":
                self.status = "OFF"
            else:
                self.status = "ON"

    def set_coordinator_index(self):
        self.coordinator_index = True

    def check_status(self):
        if self.status == "ON":
            print("coordinator_index has responded")
            return "I am alive"
        else:
            return "I am dead"


N_machines = int(input("Enter the number of machines: "))
Machine_IDs = []
Machines = []

for _ in range(N_machines):

    while True:
        process_id = math.floor(random.random() * 4 * N_machines) + 1
        if process_id not in Machine_IDs:
            m = Machine(process_id)
            Machines.append(m)
            Machine_IDs.append(process_id)
            break
        else:
            continue

print(Machine_IDs)
coordinator_index = Machine_IDs.index(max(Machine_IDs))
coordinator_machine_no = coordinator_index + 1
Machines[coordinator_index].set_coordinator_index()

print(f"Machine number {coordinator_index + 1} is the current coordinator")
print("")

communicator_machine_no = int(input("Enter the machine number who wishes to communicate: "))
communicator_index = communicator_machine_no - 1
print(f"Machine number {communicator_machine_no} has sent a request to coordinator Machine number {coordinator_machine_no}")

r = math.floor(random.random() * 10) + 1

if r > 5:
    Machines[coordinator_index].change_status()
else:
    pass

e = float(input("Enter crash probability of computer nodes: "))

for _ in range(math.ceil(N_machines*e)):
    r = random.choice(Machines)
    r.change_status("OFF")

coordinator_status = Machines[coordinator_index].check_status()

if coordinator_status == "I am dead":
    print("Coordinator did not respond.")
    print("New coordinator must be elected.")
    print("")

    responded_machines = []
    round_number = 1
    while len(responded_machines) != 1:
        print("")
        print(f"***THIS IS ELECTION ROUND {round_number}***")
        if len(responded_machines) != 1:
            responded_machines.append(Machines[communicator_index])
            print(f'Machine number {Machines.index(responded_machines[0]) + 1} has broadcasted election message!')
            for _ in Machines:
                if _.network_ID > Machines[communicator_index].network_ID and _.network_ID != Machines[coordinator_index].network_ID and _.status == "ON":
                    print(f"Machine number {Machines.index(_) + 1} has responded. ")
                    responded_machines.append(Machines[Machines.index(_)])
            responded_machines.remove(Machines[communicator_index])
            if len(responded_machines) == 1:
                communicator_index = Machines.index(responded_machines[0])
                break
            if len(responded_machines) == 0:
                break
            else:
                communicator_index = Machines.index(responded_machines[0])

            round_number += 1
            responded_machines = []

    coordinator_index = Machines.index(Machines[communicator_index])
    coordinator_machine_no = coordinator_index + 1
    print()

    print(f'Machine number {coordinator_machine_no} is the new coordinator!')

