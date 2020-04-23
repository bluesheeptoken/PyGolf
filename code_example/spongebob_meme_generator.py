_input = input()
counter = 0
ans = ""
for x in _input:
    if x.isalpha():
        ans += x.lower() if counter % 2 else x.upper()
        counter += 1
    else:
        ans += x
print(ans)
# Manually reduced to 96 characters
