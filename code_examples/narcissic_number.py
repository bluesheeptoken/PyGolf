num = int(input())

def is_nar(n):
    a = len(str(n))
    return sum(map(lambda x: int(x)**a, str(n))) == n

print(str(is_nar(num)).lower())
