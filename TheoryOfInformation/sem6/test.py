binary_data = '111111110000000000000000000000001111111100000000000000000000000011111111111111111111111100000000'
my_ls = [[] for _ in range(0, len(binary_data), 8)]
binary = list(binary_data[:8])
my_ls[0].append(binary)
for i in range(8, len(binary_data), 8):
    binary = list(binary_data[i:i + 8])
    my_ls[0].append(binary)
print(my_ls)
