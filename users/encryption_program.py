from decouple import config

def encryption(data: dict) -> str:

    chars = config('ENCRYPTION_KEY')
    key = chars.copy

    cipher_data = ""
    for letter in data:
        index = chars.index(letter)
        cipher_data += chars[index]
    return cipher_data

def decryption(cipher_data: str) -> dict :

    chars = config('ENCRYPTION_KEY')
    key = chars

    data = ""
    for letter in cipher_data:
        index = chars.index(letter)
        data += chars[index]

    return data