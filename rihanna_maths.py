

def add(a,b):
    return a + b


def subtract(a,b):
    return a - b


def divide(a,b):
    return a / b


def multiply(a,b):
    return a * b


def format_maths_string(string):
    numbers = []
    ops = []
    p = -1
    for i in string:
        if (not i.isnumeric()) and (i != '.') and (i != ' '):
            #print(f"i = {i}")

            if i in ops:
                start = p + 1
                e = string.index(i, start, -1)
                a = string[start:e].strip()
            else:
                e = string.index(i)
                a = string[p+1:e].strip()
            #print(f"a = {a}")
            b = float(a)
            #print(f"b = {b}")
            numbers.append(b)
            ops.append(i)
            p = e + 0
    numbers.append(float(string.split(ops[-1])[-1]))
    return numbers,ops


def calculate(string):
    try:
        data = format_maths_string(string)
        _ops = data[1]
        nums = data[0]
        result = nums[0]
        maths = {'*': multiply, '+': add, '-': subtract, '/': divide}
        k = 1
        for i in _ops:
            result = maths[i](result,nums[k])
            k += 1

        return string + ' = ' + result
    except Exception as e:
        return "I'm sorry I have forgotten how to solve that :("


#print(calculate("10 + 10 / 10 - 10"))