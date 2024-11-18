txt, bin_list_txt, max_len_el = input(), [], -1
for el in txt:
    temp = str(bin(ord(el)))[2:]
    len_temp = len(temp)
    print(el, end=" ")

    bin_list_txt.append(temp)

    if len_temp > max_len_el:
        max_len_el = len_temp
print()
print(bin_list_txt)

bin_list_txt = ['0' * (max_len_el - len(el)) + el for el in bin_list_txt]
print(bin_list_txt)
