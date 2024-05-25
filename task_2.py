def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 1
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    # Якщо target не знайдено, повертаємо верхню межу
    return iterations, upper_bound


# Приклад використання:
sorted_array = [0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
target_value = 0.55

result = binary_search(sorted_array, target_value)
print(result)  # Виведе кортеж з кількістю ітерацій та верхньою межею
