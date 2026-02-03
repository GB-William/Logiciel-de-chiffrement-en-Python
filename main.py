import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# --- CONSTANTES ---
ASCII_MIN = 32
ASCII_MAX = 126
ALPHABET_SIZE = ASCII_MAX - ASCII_MIN + 1  # 95 caractères

# --- FONCTIONS UTILITAIRES ---

def _car_to_index(c: str) -> int | None:
    """Convertit un caractère en indice (0..ALPHABET_SIZE-1) ou None s'il est hors alphabet."""
    code = ord(c)
    if ASCII_MIN <= code <= ASCII_MAX:
        return code - ASCII_MIN
    return None

def _index_to_car(i: int) -> str:
    """Convertit un indice (0..ALPHABET_SIZE-1) en caractère dans la plage ASCII_MIN..ASCII_MAX."""
    return chr(ASCII_MIN + (i % ALPHABET_SIZE))

def _texte_vers_indices(texte: str) -> list[int]:
    """Convertit une clé en indices. Ignore les caractères invalides de la clé."""
    indices: list[int] = []
    for c in texte:
        idx = _car_to_index(c)
        if idx is not None:
            indices.append(idx)
    return indices

def _cle_vigenere_indices(cle: str) -> list[int]:
    """Prépare la clé Vigenère."""
    if not cle:
        raise ValueError("La clé Vigenère ne doit pas être vide.")
    indices = _texte_vers_indices(cle)
    if not indices:
        raise ValueError("La clé doit contenir au moins un caractère valide (ASCII 32-126).")
    return indices

# --- LOGIQUE CÉSAR ---

def chiffrer(message: str, cle: int) -> str:
    """
    Chiffre un message avec César (générique) de manière robuste.
    Si un caractère est hors de la plage ASCII, il est recopié tel quel.
    """
    res = []
    for char in message:
        idx = _car_to_index(char)
        if idx is not None:
            # Caractère chiffrable
            nouvel_idx = (idx + cle) % ALPHABET_SIZE
            res.append(_index_to_car(nouvel_idx))
        else:
            # Caractère spécial (accent, saut de ligne, guillemet PDF...) -> on garde
            res.append(char)
    return "".join(res)

def chiffrer_cesar(message: str, cle: int) -> str:
    return chiffrer(message, cle)

def dechiffrer_cesar(message: str, cle: int) -> str:
    return chiffrer(message, -cle)

def chiffrer_cesar_lettre(message: str, cle: str) -> str:
    decalage = ord(cle[0]) - ASCII_MIN
    return chiffrer(message, decalage)

def dechiffrer_cesar_lettre(message: str, cle: str) -> str:
    decalage = ord(cle[0]) - ASCII_MIN
    return chiffrer(message, -decalage)

# --- LOGIQUE VIGENÈRE (CORRIGÉE) ---

def chiffrer_vigenere(message: str, cle: str) -> str:
    """
    Chiffrement Vigenère robuste.
    Ne plante pas sur les caractères inconnus : il les ignore et n'avance pas la clé.
    """
    key_indices = _cle_vigenere_indices(cle)
    res = []
    key_position = 0 
    
    for char in message:
        m_idx = _car_to_index(char)
        
        if m_idx is not None:
            # On chiffre seulement si le caractère est valide
            k_idx = key_indices[key_position % len(key_indices)]
            c_idx = (m_idx + k_idx) % ALPHABET_SIZE
            res.append(_index_to_car(c_idx))
            
            # On avance la clé UNIQUEMENT si on a consommé une lettre
            key_position += 1
        else:
            # Sinon on recopie le caractère (espace, retour ligne, symbole PDF...)
            res.append(char)
    
    return "".join(res)

def dechiffrer_vigenere(message: str, cle: str) -> str:
    """
    Déchiffrement Vigenère robuste.
    """
    key_indices = _cle_vigenere_indices(cle)
    res = []
    key_position = 0
    
    for char in message:
        c_idx = _car_to_index(char)
        
        if c_idx is not None:
            k_idx = key_indices[key_position % len(key_indices)]
            m_idx = (c_idx - k_idx) % ALPHABET_SIZE
            res.append(_index_to_car(m_idx))
            key_position += 1
        else:
            res.append(char)
    
    return "".join(res)

# --- GESTION FICHIERS ---

def chiffrer_fichier(source: str, destination: str, algo: str, cle) -> None:
    try:
        with open(source, "r", encoding="utf-8") as f:
            contenu = f.read()
    except UnicodeDecodeError:
        # Tentative de repli si le fichier n'est pas en UTF-8
        with open(source, "r", encoding="latin-1") as f:
            contenu = f.read()

    if algo == "cesar_num":
        resultat = chiffrer_cesar(contenu, cle)
    elif algo == "cesar_lettre":
        resultat = chiffrer_cesar_lettre(contenu, cle)
    elif algo == "vigenere":
        resultat = chiffrer_vigenere(contenu, cle)
    else:
        raise ValueError("Algorithme inconnu.")

    with open(destination, "w", encoding="utf-8") as f:
        f.write(resultat)

def dechiffrer_fichier(source: str, destination: str, algo: str, cle) -> None:
    try:
        with open(source, "r", encoding="utf-8") as f:
            contenu = f.read()
    except UnicodeDecodeError:
        with open(source, "r", encoding="latin-1") as f:
            contenu = f.read()

    if algo == "cesar_num":
        resultat = dechiffrer_cesar(contenu, cle)
    elif algo == "cesar_lettre":
        resultat = dechiffrer_cesar_lettre(contenu, cle)
    elif algo == "vigenere":
        resultat = dechiffrer_vigenere(contenu, cle)
    else:
        raise ValueError("Algorithme inconnu.")

    with open(destination, "w", encoding="utf-8") as f:
        f.write(resultat)

# --- INTERFACE GRAPHIQUE (TKINTER) ---

class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Logiciel de chiffrement pédagogique (Corrigé)")
        self.geometry("700x450")

        self._creer_widgets()
        self._creer_menus()

    def _creer_widgets(self) -> None:
        label = tk.Label(
            self,
            text="Logiciel de chiffrement (César et Vigenère)",
            font=("Arial", 16, "bold"),
        )
        label.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        btn_cesar_chiffrer = tk.Button(
            frame,
            text="1 - Chiffrer un message (César)",
            command=self.action_chiffrer_cesar,
            width=30,
        )
        btn_cesar_chiffrer.grid(row=0, column=0, padx=5, pady=5)

        btn_cesar_dechiffrer = tk.Button(
            frame,
            text="2 - Déchiffrer un message (César)",
            command=self.action_dechiffrer_cesar,
            width=30,
        )
        btn_cesar_dechiffrer.grid(row=1, column=0, padx=5, pady=5)

        btn_quitter = tk.Button(
            frame,
            text="3 - Quitter le programme",
            command=self.quit,
            width=30,
        )
        btn_quitter.grid(row=2, column=0, padx=5, pady=5)

        # Zone d'affichage
        self.resultat_var = tk.StringVar()
        label_res = tk.Label(self, text="Résultat :", font=("Arial", 12, "bold"))
        label_res.pack(pady=5)

        # Utilisation d'un widget Text pour mieux gérer les longs textes (scroll)
        self.text_area = tk.Text(self, height=8, wrap="word", bg="#f0f0f0")
        self.text_area.pack(padx=10, pady=5, fill="both", expand=True)
        # Scrollbar pour le texte
        scrollbar = tk.Scrollbar(self.text_area, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def afficher_resultat(self, texte: str):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", texte)

    def _creer_menus(self) -> None:
        menubar = tk.Menu(self)

        menu_cesar = tk.Menu(menubar, tearoff=0)
        menu_cesar.add_command(label="Chiffrer (clé lettre)", command=self.action_chiffrer_cesar_lettre)
        menu_cesar.add_command(label="Déchiffrer (clé lettre)", command=self.action_dechiffrer_cesar_lettre)
        menubar.add_cascade(label="César avancé", menu=menu_cesar)

        menu_vigenere = tk.Menu(menubar, tearoff=0)
        menu_vigenere.add_command(label="Chiffrer un message", command=self.action_chiffrer_vigenere)
        menu_vigenere.add_command(label="Déchiffrer un message", command=self.action_dechiffrer_vigenere)
        menubar.add_cascade(label="Vigenère", menu=menu_vigenere)

        menu_fichier = tk.Menu(menubar, tearoff=0)
        menu_fichier.add_command(label="Chiffrer fichier (César num.)", command=lambda: self.action_fichier(True, "cesar_num"))
        menu_fichier.add_command(label="Déchiffrer fichier (César num.)", command=lambda: self.action_fichier(False, "cesar_num"))
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Chiffrer fichier (César lettre)", command=lambda: self.action_fichier(True, "cesar_lettre"))
        menu_fichier.add_command(label="Déchiffrer fichier (César lettre)", command=lambda: self.action_fichier(False, "cesar_lettre"))
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Chiffrer fichier (Vigenère)", command=lambda: self.action_fichier(True, "vigenere"))
        menu_fichier.add_command(label="Déchiffrer fichier (Vigenère)", command=lambda: self.action_fichier(False, "vigenere"))
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Fichier", menu=menu_fichier)

        self.config(menu=menubar)

    # --- Actions Interface ---

    def _demander_message(self) -> str | None:
        return simpledialog.askstring("Message", "Entrez le message :")

    def _demander_cle_num(self) -> int | None:
        cle_str = simpledialog.askstring("Clé numérique", "Entrez la clé (nombre entier) :")
        if cle_str is None: return None
        try:
            return int(cle_str)
        except ValueError:
            messagebox.showerror("Erreur", "La clé doit être un nombre entier.")
            return None

    def _demander_cle_lettre(self) -> str | None:
        cle = simpledialog.askstring("Clé (lettre)", "Entrez une lettre clé :")
        if not cle:
            messagebox.showerror("Erreur", "La clé lettre ne doit pas être vide.")
            return None
        return cle[0]

    def _demander_cle_vigenere(self) -> str | None:
        cle = simpledialog.askstring("Clé Vigenère", "Entrez la clé (mot-clé) :")
        if not cle:
            messagebox.showerror("Erreur", "La clé ne doit pas être vide.")
            return None
        return cle

    def action_chiffrer_cesar(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_num()
            if cle is not None:
                self.afficher_resultat(chiffrer_cesar(msg, cle))

    def action_dechiffrer_cesar(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_num()
            if cle is not None:
                self.afficher_resultat(dechiffrer_cesar(msg, cle))

    def action_chiffrer_cesar_lettre(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_lettre()
            if cle:
                self.afficher_resultat(chiffrer_cesar_lettre(msg, cle))

    def action_dechiffrer_cesar_lettre(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_lettre()
            if cle:
                self.afficher_resultat(dechiffrer_cesar_lettre(msg, cle))

    def action_chiffrer_vigenere(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_vigenere()
            if cle:
                try:
                    self.afficher_resultat(chiffrer_vigenere(msg, cle))
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))

    def action_dechiffrer_vigenere(self) -> None:
        msg = self._demander_message()
        if msg:
            cle = self._demander_cle_vigenere()
            if cle:
                try:
                    self.afficher_resultat(dechiffrer_vigenere(msg, cle))
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))

    def action_fichier(self, chiffrer_mode: bool, algo: str) -> None:
        source = filedialog.askopenfilename(title="Fichier source")
        if not source: return
        destination = filedialog.asksaveasfilename(title="Enregistrer sous", defaultextension=".txt")
        if not destination: return

        cle = None
        if algo == "cesar_num": cle = self._demander_cle_num()
        elif algo == "cesar_lettre": cle = self._demander_cle_lettre()
        elif algo == "vigenere": cle = self._demander_cle_vigenere()

        if cle is None: return

        try:
            if chiffrer_mode:
                chiffrer_fichier(source, destination, algo, cle)
            else:
                dechiffrer_fichier(source, destination, algo, cle)
            messagebox.showinfo("Succès", f"Fichier traité :\n{destination}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec : {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()