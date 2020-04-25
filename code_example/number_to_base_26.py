n = int(input())
l = ""
while n > 0:
    l = chr(65 + n % 26) + l
    n //= 26
if l:
    print(l)
else:
    print("A")
