import timeit
import os

def read_file(filename):
    """Зчитує текстовий файл з припущенням UTF-8 або fallback на Windows-1251"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="windows-1251") as file:
            return file.read()

# Алгоритм Кнута-Морріса-Пратта
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

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Боєра-Мура
def boyer_moore_search(text, pattern):
    def bad_character_rule(pattern):
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = i
        return bad_char

    bad_char = bad_character_rule(pattern)
    m = len(pattern)
    n = len(text)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, prime=101):
    d = 256
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % prime

    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t < 0:
                t += prime
    return -1

# Шлях до файлів
file1 = os.path.join(os.path.dirname(__file__), "стаття 1.txt")
file2 = os.path.join(os.path.dirname(__file__), "стаття 2.txt")

# Зчитування текстів
text1 = read_file(file1)
text2 = read_file(file2)

# Вибрані підрядки
existing_substring = "алгоритмів у бібліотеках"
non_existing_substring = "неіснуючий підрядок"

# Вимірювання часу виконання
results = []

for text, text_name in [(text1, "Article 1"), (text2, "Article 2")]:
    for substring, substring_type in [(existing_substring, "Existing"), (non_existing_substring, "Non-existing")]:
        for algo_name, algo in [("KMP", kmp_search), ("Boyer-Moore", boyer_moore_search), ("Rabin-Karp", rabin_karp_search)]:
            time_taken = timeit.timeit(lambda: algo(text, substring), number=100)
            results.append((algo_name, text_name, substring_type, time_taken))

# Відображення результатів
print(f"{'Algorithm':<15}{'Text':<15}{'Substring':<15}{'Execution Time'}")
print("-" * 60)
for algo, text, substring, time_taken in results:
    print(f"{algo:<15}{text:<15}{substring:<15}{time_taken:.6f}")
