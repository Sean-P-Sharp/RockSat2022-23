import time
from random import random

lines = []
for i in range(0, 10000):
    lines.append(str(random()) + "\n")

a_start = time.time() * 1000
for line in lines:
    with open("test_a.txt", "a") as file:
        file.write(line)
a_end = time.time() * 1000
print(f"With open each time took {str((a_end - a_start) / 10000)} milliseconds per record")

b_start = time.time() * 1000
file = open("test_b.txt", "a")
for line in lines:
    file.write(line)
file.close()
b_end = time.time() * 1000
print(f"Single file took {str((b_end - b_start) / 10000)} milliseconds per record")
