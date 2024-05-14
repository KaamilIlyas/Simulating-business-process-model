# random is used to generate random values for service times and arrival intervals
# queue is used to create a (FIFO) data structure to simulate the waiting lines for each department
import random
from queue import Queue

# constants are defined to control the simulation
NUM_STUDENTS = 1000      # number of customers to simulate
MAX_SERVICE_TIME = 5   # maximum service time for each department
ARRIVAL_INTERVAL = 2   # arrival interval between customers

# these functions are defined to generate random values for service time and arrival interval
def get_random_service_time():
    return random.randint(1, MAX_SERVICE_TIME)

def get_random_arrival_time():
    return random.randint(1, ARRIVAL_INTERVAL)

# defining function to simulate a student arriving at the university
def student(arrival_time, admission_queue):

  # generating random values to simulate whether the student has necessary documents and has passed the test
    has_documents = random.random() < 0.8
    has_passed_test = random.random() < 0.6

   # checking whether the student has the necessary documents and has passed the test
   # if yes, adding the student to the admission queue
   # if not, not adding the student to the admission queue
    if has_documents and has_passed_test:
        admission_queue.put((arrival_time, None))
        print(f"Student arrived at {arrival_time}. Documents and test are good. Joined admission queue.")
    else:
        print(f"Student arrived at {arrival_time}. Documents or test are not good. Did not join admission queue.")


# defining a function to simulate the admission committee serving a student
def admission_committee(current_time, admission_queue, exam_queue):

  # checking if the admission queue is not empty
    if not admission_queue.empty():

      # checking if the first student in the admission queue has arrived
        student_arrival_time, _ = admission_queue.queue[0]
        if student_arrival_time <= current_time:
            admission_queue.get()
            exam_queue.put((current_time, get_random_service_time()))
            print(f"Admission committee served student at {current_time}. Sent to exam committee.")


# defining a function to simulate the exam committee serving a student
def exam_committee(current_time, exam_queue, acceptance_queue, waiting_times, service_times, departure_queue):

  # checking if the exam queue is not empty
    if not exam_queue.empty():

      # checking if the first student in the exam queue has finished being served
        student_arrival_time, service_time = exam_queue.queue[0]
        if student_arrival_time + service_time <= current_time:
            exam_queue.get()

            # checking if the student is accepted or rejected
            if random.random() < 0.6:
                departure_time = current_time + service_time
                acceptance_queue.put((current_time, departure_time))
                print(f"Exam committee served student at {current_time}. Accepted. Departure time: {departure_time}")

                # calculating waiting and service times and adding them to their respective lists
                waiting_times.append(current_time - student_arrival_time)
                service_times.append(service_time)
                departure_queue.put(departure_time)
            else:
                print(f"Exam committee served student at {current_time}. Rejected.")

# creating necessary queues and setting initial values
departure_queue = Queue()
student_arrival_queue = Queue()
admission_queue = Queue()
exam_queue = Queue()
acceptance_queue = Queue()
current_time = 0
accept_count = 0
waiting_times = []
service_times = []

# following loop runs for NUM_STUDENTS and simulates the arrival of students to the university
# for each iteration, a random arrival time is generated and added to the student_arrival_queue
for i in range(NUM_STUDENTS):
    next_arrival_time = current_time + get_random_arrival_time()
    student_arrival_queue.put(next_arrival_time)

    student(next_arrival_time, admission_queue)   # then, the student function is called with the current arrival time and the admission_queue

    current_time = next_arrival_time # the current_time is updated to the next_arrival_time

   # admission committee is called to check if any student can be sent to the exam committee
   # arguments are passed to the admission_committee function  
    admission_committee(current_time, admission_queue, exam_queue)

   # exam committee is called to check if any student can be served
   # arguments are passed to the exam_committee function
    exam_committee(current_time, exam_queue, acceptance_queue, waiting_times, service_times, departure_queue)


# following loop runs until there are no more students in the student_arrival_queue
# it checks if there are any students in the acceptance_queue and calculates the waiting time
while not student_arrival_queue.empty():
    arrival_time = student_arrival_queue.get()

# if there are, the accept_count is incremented and the student's arrival time, acceptance time, departure time, and waiting time are printed
    if not acceptance_queue.empty():
        acceptance_time, departure_time = acceptance_queue.get()
        waiting_time = departure_time - arrival_time
        accept_count += 1
        print(f"Student arrived at {arrival_time}. Accepted at {acceptance_time}. Departed at {departure_time}. Waited for {waiting_time} units.")

    # if not, the student is rejected  
    else:
        print(f"Student arrived at {arrival_time}. Rejected.")

# average waiting time and average service time are calculated and printed
avg_waiting_time = sum(waiting_times) / len(waiting_times)
avg_service_time = sum(service_times) / len(service_times)

print(f"\nNumber of students accepted: {accept_count}")
print(f"\nAverage waiting time: {avg_waiting_time:.2f}")
print(f"\nAverage service time: {avg_service_time:.2f}")