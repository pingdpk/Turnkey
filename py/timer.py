import timeit

def timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(func.__name__ , ' : ' , sum(runs) / len(runs))
    return wrapper        