"""
Module contenant les classes Document et ses sous-classes
"""

from datetime import date


class Document:
    """Classe de base pour tous les documents de la bibliothèque"""

    def __init__(self, titre):
        """
        Initialise un document
        """
        self._titre = titre

    @property
    def titre(self):
        """Retourne le titre du document"""
        return self._titre

    @titre.setter
    def titre(self, value):
        """Modifie le titre du document"""
        self._titre = value

    def to_csv(self):
        """
        Convertit le document en format CSV
        """
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un document à partir d'une ligne CSV
        """
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")

    def __str__(self):
        return f"Document: {self._titre}"


class Volume(Document):
    """Classe représentant un volume (livre, BD, dictionnaire)"""

    def __init__(self, titre, auteur):
        """
        Initialise un volume
        """
        super().__init__(titre)
        self._auteur = auteur

    @property
    def auteur(self):
        """Retourne l'auteur du volume"""
        return self._auteur

    @auteur.setter
    def auteur(self, value):
        """Modifie l'auteur du volume"""
        self._auteur = value

    def __str__(self):
        """Représentation textuelle du volume"""
        return f"Volume: {self._titre} par {self._auteur}"


class Livre(Volume):
    """Classe représentant un livre (peut être emprunté)"""

    def __init__(self, titre, auteur, disponible=True):
        """
        Initialise un livre
        """
        super().__init__(titre, auteur)
        self._disponible = disponible

    @property
    def disponible(self):
        """Retourne si le livre est disponible"""
        return self._disponible

    @disponible.setter
    def disponible(self, value):
        """Modifie la disponibilité du livre"""
        self._disponible = value

    def emprunter(self):
        """
        Marque le livre comme emprunté
        """
        if self._disponible:
            self._disponible = False
            return True
        return False

    def rendre(self):
        """Marque le livre comme rendu"""
        self._disponible = True

    def empruntable(self):
        """
        Vérifie si le livre peut être emprunté
        """
        return self._disponible

    def to_csv(self):
        """
        Convertit le livre en format CSV
        """
        return f"Livre,{self._titre},{self._auteur},{self._disponible}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un livre à partir d'une ligne CSV
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 4:
            disponible = parts[3].lower() == 'true'
            return Livre(parts[1], parts[2], disponible)
        return None

    def __str__(self):
        statut = "Disponible" if self._disponible else "Emprunté"
        return f"Livre: {self._titre} par {self._auteur} ({statut})"


class BD(Volume):
    """Classe représentant une bande dessinée"""

    def __init__(self, titre, auteur, dessinateur):
        """
        Initialise une BD
        """
        super().__init__(titre, auteur)
        self._dessinateur = dessinateur

    @property
    def dessinateur(self):
        """Retourne le dessinateur de la BD"""
        return self._dessinateur

    @dessinateur.setter
    def dessinateur(self, value):
        """Modifie le dessinateur de la BD"""
        self._dessinateur = value

    def to_csv(self):
        """
        Convertit la BD en format CSV
        """
        return f"BD,{self._titre},{self._auteur},{self._dessinateur}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée une BD à partir d'une ligne CSV
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 4:
            return BD(parts[1], parts[2], parts[3])
        return None

    def __str__(self):
        return f"BD: {self._titre} par {self._auteur} (dessin: {self._dessinateur})"


class Dictionnaire(Volume):
    """Classe représentant un dictionnaire"""

    def __init__(self, titre, auteur):
        """
        Initialise un dictionnaire
        """
        super().__init__(titre, auteur)

    def to_csv(self):
        """
        Convertit le dictionnaire en format CSV
        """
        return f"Dictionnaire,{self._titre},{self._auteur}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un dictionnaire à partir d'une ligne CSV
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 3:
            return Dictionnaire(parts[1], parts[2])
        return None

    def __str__(self):
        """Représentation textuelle du dictionnaire"""
        return f"Dictionnaire: {self._titre} édité par {self._auteur}"


class Journal(Document):
    """Classe représentant un journal"""

    def __init__(self, titre, date_parution):
        """
        Initialise un journal
        """
        super().__init__(titre)
        self._date_parution = date_parution

    @property
    def date_parution(self):
        """Retourne la date de parution"""
        return self._date_parution

    @date_parution.setter
    def date_parution(self, value):
        """Modifie la date de parution"""
        self._date_parution = value

    def to_csv(self):
        """
        Convertit le journal en format CSV
        """
        date_str = self._date_parution.strftime('%Y-%m-%d')
        return f"Journal,{self._titre},{date_str}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un journal à partir d'une ligne CSV
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 3:
            date_parts = parts[2].split('-')
            date_parution = date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            return Journal(parts[1], date_parution)
        return None

    def __str__(self):
        return f"Journal: {self._titre} du {self._date_parution.strftime('%d/%m/%Y')}"