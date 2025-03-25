def sliding_window_max_sum(arr, k):
    if not arr or k <= 0 or k > len(arr):
        return None

    TempSum = sum(arr[:k])
    max_sum = TempSum

    for i in range(k, len(arr)):
        TempSum = TempSum - arr[i - k] + arr[i]
        print(TempSum)
        max_sum = max(max_sum, TempSum)

    return max_sum


arr = [1, 3, -1, -3, 5, 3, 6, 7]
len_window = 3
result = sliding_window_max_sum(arr, len_window)
print(f"Максимальная сумма подмассива длиной {len_window}: {result}")
