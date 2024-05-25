import timeit

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='cp1251') as file:
            return file.read()

# Читання текстових файлів з обробкою кодування
text1 = read_file('Article_1.txt')
text2 = read_file('Article_2.txt')

# Пошук підрядка в тексті за допомогою алгоритму Боєра-Мура
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: return 0
    skip = {ch: m for ch in set(text)}
    for k in range(m - 1):
        skip[pattern[k]] = m - k - 1
    k = m - 1
    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1
            i -= 1
        if j == -1:
            return i + 1
        k += skip.get(text[k], m)
    return -1

# Пошук підрядка в тексті за допомогою алгоритму Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Пошук підрядка в тексті за допомогою алгоритму Рабіна-Карпа
def rabin_karp(text, pattern):
    d = 256
    q = 101
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                return s
        if s < n - m:
            t = (t - h * ord(text[s])) % q
            t = (t * d + ord(text[s + m])) % q
            t = (t + q) % q
    return -1

# Тестові підрядки
existing_substring = "пошук"  # Підрядок, який існує в обох текстах
non_existing_substring = "неіснуючийпідрядок"  # Підрядок, якого немає в обох текстах

# Вимірювання часу виконання для кожного алгоритму та кожного підрядка
def measure_time(text, pattern, algorithm):
    stmt = lambda: algorithm(text, pattern)
    times = timeit.repeat(stmt, repeat=3, number=1000)
    return min(times)

# Вимірювання часу для кожного алгоритму на тексті 1
times_text1 = {
    "- Боєра-Мура, Існуючий": measure_time(text1, existing_substring, boyer_moore),
    "- Боєра-Мура, Не Існуючий": measure_time(text1, non_existing_substring, boyer_moore),
    "- КМП, Існуючий": measure_time(text1, existing_substring, kmp_search),
    "- КМП, Не Існуючий": measure_time(text1, non_existing_substring, kmp_search),
    "- Рабіна-Карпа, Існуючий": measure_time(text1, existing_substring, rabin_karp),
    "- Рабіна-Карпа, Не Існуючий": measure_time(text1, non_existing_substring, rabin_karp),
}

# Вимірювання часу для кожного алгоритму на тексті 2
times_text2 = {
    "- Боєра-Мура, Існуючий": measure_time(text2, existing_substring, boyer_moore),
    "- Боєра-Мура, Не Існуючий": measure_time(text2, non_existing_substring, boyer_moore),
    "- КМП, Існуючий": measure_time(text2, existing_substring, kmp_search),
    "- КМП, Не Існуючий": measure_time(text2, non_existing_substring, kmp_search),
    "- Рабіна-Карпа, Існуючий": measure_time(text2, existing_substring, rabin_karp),
    "- Рабіна-Карпа, Не Існуючий": measure_time(text2, non_existing_substring, rabin_karp),
}

# Виведення результатів
print("Час виконання для тексту 1:")
for key, value in times_text1.items():
    print(f"{key}: {value:.6f} секунд")

print("\nЧас виконання для тексту 2:")
for key, value in times_text2.items():
    print(f"{key}: {value:.6f} секунд")

# Визначення найшвидшого алгоритму для кожного тексту окремо та в цілому
fastest_text1 = min(times_text1, key=times_text1.get)
fastest_text2 = min(times_text2, key=times_text2.get)

print("\nНайшвидший алгоритм для тексту 1:", fastest_text1)
print("Найшвидший алгоритм для тексту 2:", fastest_text2)

# Визначення найшвидшого алгоритму в цілому
all_times = {**times_text1, **times_text2}
fastest_overall = min(all_times, key=all_times.get)

print("\nНайшвидший алгоритм в цілому:", fastest_overall)