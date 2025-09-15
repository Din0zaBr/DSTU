
# keyword: list = list(input())
row_count, colum_count = int(input()), int(input())

for row in range(0, row_count * colum_count, row_count):
    print(row)
