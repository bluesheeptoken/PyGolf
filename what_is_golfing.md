# What is golfing ?

Golfing is the art of use as few characters as possible to implement an algorithm.

If you want some inspirations about rules or if you just want to shorten your code, here are some tips.

## if else side effect statement

Instead of writing 
```python
if condition:
    print(a)
else:
    print(b)
```

you can write
```python
print([b,a][condition])
```

However, Python will eagerly evaluate every variable, if you need to lazily evaluate, you can alternatively write:

```python
print(a if condition else b)
```

This also works for reasignement

For example

```python
if condition:
    v += 5
else:
    v += 2
```

becomes

```python
v+=2+3*condition
```

## Iterate over a cartesian product of range

````python
for i in range(n):
    for j in range(m):
        do_something(i, j)
````

can become

````python
for i in range(n*m):
    do_something(i//n,j%m)
````

## Iterate with a variable you do not need

````python
for i in range(n):
    do_something_without_i()
````

can become

````python
for i in'|'*n:
    do_something_without_i()
````

## Star assignement for lists

````python
l=list(map(int, input().split()))
````
can become
````python
*l,=map(int,input().split())
````

## Lists manipulations

`l.append(a)` => `l+=[a]`
`a=l[0]` => `a,_*=l`
`a=l[-1]` => `_*,a=l`

## Floor and Ceil

`math.floor(n)` => `n//1`
`math.ceil(n)` => `-(-n//1)`

## Raise an exception to terminate program

In most exercises, you can terminate your program by raising an exception.

````python
n=int(input())
for i in range(n):
    do_stuff(input())
````

can become

````python
input()
while 1:
    do_stuff(input())
````

## Multiple statements

If you have multiple statement in a row, you can separate them by `;`

```python
for i in range(n):print(i);print(i+1)
```

## Tabulations

Python accepts any kind of tabulations. Therefore, you can use a single space:

```python
while True:
 pass
```
