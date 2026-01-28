const = 32

def chiffrer(message, cle):
    messageChiffre = ''
    for character in message:
        messageChiffre += chr(((ord(character) - const + cle) % 95)+const)
    print(messageChiffre)
    return messageChiffre


def dechiffrer(message, cle):
    messageDechiffre = ''
    for character in message:
        messageDechiffre += chr(((ord(character) - const - cle) % 95) + const)
    print(messageDechiffre)
    return messageDechiffre