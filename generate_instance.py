import sys
import random

v = int(sys.argv[1]) if len(sys.argv) > 1 else 10
e = int(sys.argv[2]) if len(sys.argv) > 2 else 20

print(v)
print(e)

for i in range(e):
    a = random.randrange(0, v)
    b = random.randrange(0, v)
    w = random.random()
    print(f'{a} {b} {w:.3f}')
