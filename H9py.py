# %%
def dna_to_rna(dna):
    translation = {
        'G': 'C',
        'C': 'G',
        'T': 'A',
        'A': 'T'
    }
    rna = ''.join(translation[base] for base in dna)
    
    return rna
dna = "GGCTAA"
rna = dna_to_rna(dna)
print(f"Вход: {dna} Результат: {rna}")


# %%
def get_vowel_positions(word):
    vowels = "ауоыиэяюёе"
    return [i for i, letter in enumerate(word) if letter in vowels]

def find_similar_words(base_word, words):
    base_vowel_positions = get_vowel_positions(base_word)
    similar_words = [word for word in words if get_vowel_positions(word) == base_vowel_positions]
    return similar_words

base_word = input("Введите начальное слово: ").strip().lower()
p = int(input("Введите количество слов для сравнения: ").strip())

words = []
for _ in range(p):
    word = input("Введите слово: ").strip().lower()
    words.append(word)

similar_words = find_similar_words(base_word, words)

print("Слова, похожие на {}:".format(base_word))
for word in similar_words:
    print(word)


# %%
def frequency_analysis(text):
    text = text.lower()
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    sorted_frequency = sorted(frequency.items(), key=lambda item: (-item[1], item[0]))
    for char, freq in sorted_frequency[:10]:
        print(f"{char} - {freq}")
text = "Мама мыла раму"
frequency_analysis(text)


