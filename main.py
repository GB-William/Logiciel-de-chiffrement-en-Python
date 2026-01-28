const = 32

ASCII_MIN = 32
ASCII_MAX = 255
ALPHABET_SIZE = ASCII_MAX - ASCII_MIN + 1  # 224 caractères


def _car_to_index(c: str) -> int | None:
    """Convertit un caractère en indice (0..ALPHABET_SIZE-1) ou None s'il est hors alphabet."""
    code = ord(c)
    if ASCII_MIN <= code <= ASCII_MAX:
        return code - ASCII_MIN
    return None


def _index_to_car(i: int) -> str:
    """Convertit un indice (0..ALPHABET_SIZE-1) en caractère dans la plage ASCII_MIN..ASCII_MAX."""
    return chr(ASCII_MIN + (i % ALPHABET_SIZE))

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

def _texte_vers_indices(texte: str) -> list[int]:
    """Convertit un texte en liste d'indices dans l'alphabet 0..ALPHABET_SIZE-1 (s'il est dans l'intervalle)."""
    indices: list[int] = []
    for c in texte:
        idx = _car_to_index(c)
        if idx is None:
            raise ValueError(
                f"Caractère '{c}' hors alphabet ASCII {ASCII_MIN}..{ASCII_MAX}, "
                "impossible pour cet exercice pédagogique."
            )
        indices.append(idx)
    return indices


def _cle_vigenere_indices(cle: str) -> list[int]:
    """Convertit la clé (mot) en liste d'indices 0..94."""
    if not cle:
        raise ValueError("La clé Vigenère ne doit pas être vide.")
    return _texte_vers_indices(cle)


def chiffrer_vigenere(message: str, cle: str) -> str:
    """
    Chiffrement de Vigenère.
    Pour chaque lettre : lettre_chiffree = (lettre_message + lettre_cle) mod 95
    où les lettres sont représentées par (ASCII - 32).
    """
    if not cle:
        raise ValueError("La clé Vigenère ne doit pas être vide.")

    msg_indices = _texte_vers_indices(message)
    key_indices = _cle_vigenere_indices(cle)

    res = []
    for i, m_idx in enumerate(msg_indices):
        k_idx = key_indices[i % len(key_indices)]
        c_idx = (m_idx + k_idx) % ALPHABET_SIZE
        res.append(_index_to_car(c_idx))
    return "".join(res)

def dechiffrer_vigenere(message: str, cle: str) -> str:
    """
    Déchiffrement de Vigenère.
    lettre_originale = (lettre_chiffree - lettre_cle) mod 95
    """
    if not cle:
        raise ValueError("La clé Vigenère ne doit pas être vide.")

    msg_indices = _texte_vers_indices(message)
    key_indices = _cle_vigenere_indices(cle)

    res = []
    for i, c_idx in enumerate(msg_indices):
        k_idx = key_indices[i % len(key_indices)]
        m_idx = (c_idx - k_idx) % ALPHABET_SIZE
        res.append(_index_to_car(m_idx))
    return "".join(res)
