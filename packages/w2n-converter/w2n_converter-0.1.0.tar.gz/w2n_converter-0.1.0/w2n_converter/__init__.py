def convert(word: str) -> list[int]:
    """
    English: Converts a word to a list of numbers corresponding
    to the positions of the letters in the English alphabet (a=1, ..., z=26)
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return [alphabet.index(char.lower()) + 1 for char in word if char.lower() in alphabet]

