import math
import sys

n = int(input())
min_val = float("inf")
min_path = 0
for i in range(n):
    q, v = [int(j) for j in input().split()]
    if q * v < min_val:
        min_val = q * v
        min_path = i + 1

print(min_path)
