

# reading the words
with open("wordList.txt", "r") as word_file:
    words = [tuple(pair.split()) for pair in word_file.readlines()]


