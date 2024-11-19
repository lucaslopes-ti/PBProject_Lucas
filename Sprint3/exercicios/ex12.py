def my_map(lst, f):
    return [f(x) for x in lst]

# teste da funcao

input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def square(x):
    return x ** 2

output_list = my_map(input_list, square)
print(output_list)