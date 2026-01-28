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
        messageChiffre += chr(((ord(character) - ASCII_MIN + cle) % 95)+ASCII_MIN)
    print(messageChiffre)
    return messageChiffre


def dechiffrer(message, cle):
    messageDechiffre = ''
    for character in message:
        messageDechiffre += chr(((ord(character) - ASCII_MIN - cle) % 95) + ASCII_MIN)
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



# --- Interface Tkinter ---


class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Logiciel de chiffrement pédagogique")
        self.geometry("700x400")

        self._creer_widgets()
        self._creer_menus()

    def _creer_widgets(self) -> None:
        label = tk.Label(
            self,
            text="Logiciel de chiffrement (César et Vigenère)",
            font=("Arial", 16, "bold"),
        )
        label.pack(pady=10)

        # Boutons principaux (version minimale demandée)
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

        # Zone d'affichage du résultat
        self.resultat_var = tk.StringVar()
        label_res = tk.Label(self, text="Résultat :", font=("Arial", 12, "bold"))
        label_res.pack(pady=5)

        self.resultat_label = tk.Label(
            self, textvariable=self.resultat_var, wraplength=650, justify="left"
        )
        self.resultat_label.pack(padx=10, pady=5, fill="both", expand=True)

    def _creer_menus(self) -> None:
        menubar = tk.Menu(self)

        # Menu César avancé (clé lettre)
        menu_cesar = tk.Menu(menubar, tearoff=0)
        menu_cesar.add_command(
            label="Chiffrer (clé lettre)", command=self.action_chiffrer_cesar_lettre
        )
        menu_cesar.add_command(
            label="Déchiffrer (clé lettre)", command=self.action_dechiffrer_cesar_lettre
        )
        menubar.add_cascade(label="César avancé", menu=menu_cesar)

        # Menu Vigenère
        menu_vigenere = tk.Menu(menubar, tearoff=0)
        menu_vigenere.add_command(
            label="Chiffrer un message", command=self.action_chiffrer_vigenere
        )
        menu_vigenere.add_command(
            label="Déchiffrer un message", command=self.action_dechiffrer_vigenere
        )
        menubar.add_cascade(label="Vigenère", menu=menu_vigenere)

        # Menu fichiers
        menu_fichier = tk.Menu(menubar, tearoff=0)
        menu_fichier.add_command(
            label="Chiffrer un fichier (César num.)",
            command=lambda: self.action_fichier(chiffrer=True, algo="cesar_num"),
        )
        menu_fichier.add_command(
            label="Déchiffrer un fichier (César num.)",
            command=lambda: self.action_fichier(chiffrer=False, algo="cesar_num"),
        )
        menu_fichier.add_separator()
        menu_fichier.add_command(
            label="Chiffrer un fichier (César lettre)",
            command=lambda: self.action_fichier(chiffrer=True, algo="cesar_lettre"),
        )
        menu_fichier.add_command(
            label="Déchiffrer un fichier (César lettre)",
            command=lambda: self.action_fichier(chiffrer=False, algo="cesar_lettre"),
        )
        menu_fichier.add_separator()
        menu_fichier.add_command(
            label="Chiffrer un fichier (Vigenère)",
            command=lambda: self.action_fichier(chiffrer=True, algo="vigenere"),
        )
        menu_fichier.add_command(
            label="Déchiffrer un fichier (Vigenère)",
            command=lambda: self.action_fichier(chiffrer=False, algo="vigenere"),
        )
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Fichier", menu=menu_fichier)

        self.config(menu=menubar)

    # --- Actions César simple (boutons 1 et 2) ---

    def _demander_message(self) -> str | None:
        return simpledialog.askstring("Message", "Entrez le message :")

    def _demander_cle_num(self) -> int | None:
        cle_str = simpledialog.askstring(
            "Clé numérique", "Entrez la clé (nombre entier, positif ou négatif) :"
        )
        if cle_str is None:
            return None
        try:
            return int(cle_str)
        except ValueError:
            messagebox.showerror("Erreur", "La clé doit être un nombre entier.")
            return None

    def action_chiffrer_cesar(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_num()
        if cle is None:
            return
        resultat = chiffrer_cesar(message, cle)
        self.resultat_var.set(resultat)

    def action_dechiffrer_cesar(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_num()
        if cle is None:
            return
        resultat = dechiffrer_cesar(message, cle)
        self.resultat_var.set(resultat)

    # --- Actions César par lettre ---

    def _demander_cle_lettre(self) -> str | None:
        cle = simpledialog.askstring(
            "Clé (lettre)",
            "Entrez une lettre qui représente la clé (décalage = ASCII(le) - 32) :",
        )
        if not cle:
            messagebox.showerror("Erreur", "La clé lettre ne doit pas être vide.")
            return None
        return cle[0]

    def action_chiffrer_cesar_lettre(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_lettre()
        if cle is None:
            return
        resultat = chiffrer_cesar_lettre(message, cle)
        self.resultat_var.set(resultat)

    def action_dechiffrer_cesar_lettre(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_lettre()
        if cle is None:
            return
        resultat = dechiffrer_cesar_lettre(message, cle)
        self.resultat_var.set(resultat)

    # --- Actions Vigenère ---

    def _demander_cle_vigenere(self) -> str | None:
        cle = simpledialog.askstring(
            "Clé Vigenère",
            "Entrez la clé (mot-clé, caractères ASCII entre 32 et 126) :",
        )
        if not cle:
            messagebox.showerror("Erreur", "La clé Vigenère ne doit pas être vide.")
            return None
        return cle

    def action_chiffrer_vigenere(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_vigenere()
        if cle is None:
            return
        try:
            resultat = chiffrer_vigenere(message, cle)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.resultat_var.set(resultat)

    def action_dechiffrer_vigenere(self) -> None:
        message = self._demander_message()
        if message is None:
            return
        cle = self._demander_cle_vigenere()
        if cle is None:
            return
        try:
            resultat = dechiffrer_vigenere(message, cle)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.resultat_var.set(resultat)

    # --- Actions fichiers ---

    def action_fichier(self, chiffrer: bool, algo: str) -> None:
        source = filedialog.askopenfilename(
            title="Choisir le fichier texte",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if not source:
            return

        destination = filedialog.asksaveasfilename(
            title="Enregistrer le résultat sous",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if not destination:
            return

        # Demande de clé selon l'algorithme
        try:
            if algo == "cesar_num":
                cle = self._demander_cle_num()
                if cle is None:
                    return
            elif algo == "cesar_lettre":
                cle = self._demander_cle_lettre()
                if cle is None:
                    return
            elif algo == "vigenere":
                cle = self._demander_cle_vigenere()
                if cle is None:
                    return
            else:
                messagebox.showerror("Erreur", "Algorithme de fichier inconnu.")
                return

            if chiffrer:
                chiffrer_fichier(source, destination, algo, cle)
            else:
                dechiffrer_fichier(source, destination, algo, cle)

            messagebox.showinfo(
                "Succès", f"Le fichier a été traité et enregistré dans :\n{destination}"
            )
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


def main() -> None:
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()

