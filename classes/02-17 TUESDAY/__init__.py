def fibonacci(n):
    sequence = [0, 1]
    
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

print(fibonacci(10))