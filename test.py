# write a program that encrypt messages using a substitution cipher.
# The program should ask the user to enter a message and a substitution cipher key.
# The cipher key should include 26 alphabetic characters, in which a character is mapped to another character.
# The program should then encrypt the message using the substitution cipher and display the encrypted message.
# for example, $ ./substitution JTREKYAVOGDXPSNCUIZLFBMWHQ; plaintext:  HELLO; ciphertext: VKXXN

def encrypt(key, message):
    cipher = ""
    for letter in message:
        if letter.isalpha():
            if letter.isupper():
                cipher += key[ord(letter.lower()) - ord('a')].upper()
            else:
                cipher += key[ord(letter) - ord('a')] 
        else:
            cipher += key[ord(letter) - ord('a')] 
    return cipher


def main():
    key = input("Enter a substitution cipher key: ")
    message = input("Enter a message to encrypt: ")
    print("Encrypted message:", encrypt(key, message))


if __name__ == "__main__":
    main()

