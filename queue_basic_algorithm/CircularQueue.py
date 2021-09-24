# Basic CircularQueue algorithm

import os, time
from tabulate import tabulate

class CircularQueue:
    def __init__(self, capacity):
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        self.capacity = capacity

    def is_Full(self):
        return self.size == self.capacity

    def is_Empty(self):
        return self.size == 0

    def clear(self):
        self.queue = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        print("Queue has been cleared!")

    def display(self):
        queue_Data = ['Q']
        head_Tail_Pos = ['T/H']
        index_Pos = ['Index']

        # Traditional
        # print("[", end=" ")
        # for i in range(0, self.capacity):
        #     print(self.queue[i], end=" ")
        # print("]")

        # Using table for clearer display, real algorithm should use the traditional method
        for i in range(0, self.capacity):
            queue_Data.append(self.queue[i] if self.queue[i] is not None else "None")

            if i == self.head and i == self.tail:
                head_Tail_Pos.append("Head-Tail")
            elif i == self.head:
                head_Tail_Pos.append("Head")
            elif i == self.tail:
                head_Tail_Pos.append("Tail")
            else:
                head_Tail_Pos.append("")

            index_Pos.append(i)

        # Table using tabulate
        table_Data = [queue_Data, head_Tail_Pos, index_Pos]
        print(tabulate(table_Data))

        print("Queue size\t:", self.size)
        print("Head position\t:", self.head)
        print("Tail position\t:", self.tail)

    def enqueue(self, data):
        # Check full
        if self.is_Full(): # size = capacity
            print("Queue is Full!")
            return
        # Circular queue does not have overflow condition

        # Store the data
        self.queue[self.tail] = data
        
        # Calculate the tail and size
        self.tail = (self.tail + 1) % self.capacity # Circular queue implementation
        self.size += 1

        print("Enqueued:", data)

    def dequeue(self):
        # Check empty
        if self.is_Empty():
            print("Queue is Empty!")
            return

        # Get the data
        data = self.queue[self.head]
        # Erase the data
        self.queue[self.head] = None
        
        # Calculate the head and size
        self.head = (self.head + 1) % self.capacity
        self.size -= 1

        print("Dequeued:", data)


if __name__ == "__main__":
    size = 5
    q = CircularQueue(size)
    
    running = True
    while running:
        temp = os.system("clear")
        print("=" * 50)
        print("\t\tCircular Queue Algorithm")
        print("\t\t Max queue size:", size)
        print("=" * 50)
        print("Current queue:")
        q.display()
        print("=" * 50)
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Clear")
        print("4. Exit")
        print("=" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            value = input("Enter value: ")
            if value == '':
                print("Invalid input!")
            else:
                q.enqueue(value)
        elif choice == '2':
            q.dequeue()
        elif choice == '3':
            q.clear()
        elif choice == '4':
            print("Exiting..")
            time.sleep(1)
            os._exit(0)
        else:
            print("Invalid choice")
        
        input("\nPress enter to continue...")
