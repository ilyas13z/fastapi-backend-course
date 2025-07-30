data = {'0': ['task0', 'active'], '1': ['task1', 'active']}

# list1 = list(map(lambda x: {int(x): data[x]}, data.keys()))
list2 = {int(i): data[i] for i in data.keys()}
print(list2)