my_str = '11000'
my_new_str = str((int(my_str[-1]) ^ int(my_str[-3]) ^ int(my_str[-5]))) + my_str[:-1]
print(f'{1}, {my_str} | {my_str[-1]}')
count = 2
while my_new_str != '11000':
    print(f'{count}, {my_new_str} | {my_new_str[-1]}')
    temp = str((int(my_new_str[-1]) ^ int(my_new_str[-3]) ^ int(my_new_str[-5]))) + my_new_str[:-1]
    my_new_str = temp
    count += 1
print(count, my_new_str)
