# 🔐 Logiciel de chiffrement en Python

Projet pédagogique de chiffrement implémentant les algorithmes de **César** et de **Vigenère** avec une interface graphique Tkinter.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/license-Educational-green.svg)

## 📋 Description

Ce logiciel permet de chiffrer et déchiffrer des messages en utilisant deux algorithmes cryptographiques classiques. Il s'agit d'un projet à vocation **purement pédagogique** : les algorithmes implémentés ne sont pas sécurisés pour un usage réel en production.

### ⚠️ Avertissement

Ce projet est destiné à l'apprentissage des concepts de base de la cryptographie. **Ne jamais utiliser ces algorithmes pour protéger des données sensibles en environnement réel.**

## ✨ Fonctionnalités

### 🔑 Chiffrement de César
- Chiffrement avec clé numérique (décalage fixe)
- Chiffrement avec clé alphabétique (conversion ASCII - 32)
- Déchiffrement avec la même clé
- Support de 95 caractères ASCII (codes 32 à 126)

### 🔐 Chiffrement de Vigenère
- Chiffrement polyalphabétique avec mot-clé
- Décalage variable selon la position dans le message
- Déchiffrement avec le même mot-clé
- Résistance améliorée par rapport à César

### 🖥️ Interface graphique (Tkinter)
- Menu interactif convivial
- Chiffrement/déchiffrement de messages texte
- Chiffrement/déchiffrement de fichiers texte
- Saisie et affichage des résultats

## 🚀 Installation

### Prérequis

- Python 3.x
- Tkinter (généralement inclus avec Python)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/GB-William/Logiciel-de-chiffrement-en-Python.git

# Accéder au répertoire
cd Logiciel-de-chiffrement-en-Python

# Lancer le programme
python main.py
```

## 💻 Utilisation

### Interface en ligne de commande

```python
from main import chiffrer_cesar, dechiffrer_cesar

# Chiffrement de César
message = "Bonjour le monde!"
cle = 3
message_chiffre = chiffrer_cesar(message, cle)
print(f"Message chiffré : {message_chiffre}")

# Déchiffrement
message_original = dechiffrer_cesar(message_chiffre, cle)
print(f"Message déchiffré : {message_original}")
```

### Interface graphique

1. Lancez le programme : `python main.py`
2. Sélectionnez l'action souhaitée dans le menu
3. Saisissez votre message et votre clé
4. Consultez le résultat affiché

## 🔢 Fonctionnement des algorithmes

### Chiffrement de César

Le chiffrement de César effectue un décalage fixe de chaque caractère :

```
caractère_chiffré = (caractère_original + clé) mod 95
```

**Exemple :**
- Message : `"ABC"`
- Clé : `3`
- Résultat : `"DEF"`

### Chiffrement de Vigenère

Le chiffrement de Vigenère utilise un mot-clé qui détermine un décalage variable :

```
Pour chaque position i :
    décalage = valeur_ASCII(clé[i % longueur_clé]) - 32
    caractère_chiffré[i] = (caractère_original[i] + décalage) mod 95
```

**Exemple :**
- Message : `"HELLO"`
- Clé : `"KEY"`
- Décalages : K=43, E=37, Y=57 (répétés)
- Le premier 'H' est décalé de 43, le deuxième 'E' de 37, etc.

## 📁 Structure du projet

```
Logiciel-de-chiffrement-en-Python/
│
├── main.py                 # Programme principal
├── README.md              # Ce fichier
└── exemples/              # Fichiers d'exemple (optionnel)
    ├── message_test.txt
    └── message_chiffre.txt
```

## 🎯 Objectifs pédagogiques

Ce projet permet de travailler sur :

- ✅ Manipulation de chaînes de caractères en Python
- ✅ Utilisation des boucles et conditions
- ✅ Création et utilisation de fonctions
- ✅ Opérations mathématiques (modulo, ASCII)
- ✅ Développement d'interfaces graphiques avec Tkinter
- ✅ Gestion de fichiers (lecture/écriture)
- ✅ Utilisation de Git et GitHub
- ✅ Compréhension des principes de base de la cryptographie

## 🔍 Améliorations possibles

- [ ] Ajouter d'autres algorithmes (ROT13, substitution, transposition)
- [ ] Implémenter une analyse de fréquence pour casser César
- [ ] Ajouter des tests unitaires
- [ ] Créer une interface graphique plus moderne (PyQt, Kivy)
- [ ] Support du chiffrement de fichiers binaires
- [ ] Historique des opérations
- [ ] Export des résultats en différents formats

## 📚 Ressources

- [Chiffre de César - Wikipedia](https://fr.wikipedia.org/wiki/Chiffrement_par_d%C3%A9calage)
- [Chiffre de Vigenère - Wikipedia](https://fr.wikipedia.org/wiki/Chiffre_de_Vigen%C3%A8re)
- [Documentation Python](https://docs.python.org/fr/3/)
- [Documentation Tkinter](https://docs.python.org/fr/3/library/tkinter.html)

## 👥 Auteurs

- **GB-William** - *Développement initial* - [GitHub](https://github.com/GB-William)

## 📄 Licence

Ce projet est à usage éducatif uniquement. Libre d'utilisation pour l'apprentissage.

## 🙏 Remerciements

Projet réalisé dans le cadre d'un cours de programmation Python, pour comprendre les bases de la cryptographie et du développement logiciel.

---

💡 **Note :** Ce README suit les bonnes pratiques de documentation de projets open-source. N'hésitez pas à contribuer en ouvrant des issues ou des pull requests !