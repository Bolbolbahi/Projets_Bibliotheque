"""
Module contenant les classes Document et ses sous-classes
Auteur: Votre Nom
Date: 2024
"""

from datetime import date


class Document:
    """Classe de base pour tous les documents de la bibliothèque"""

    def __init__(self, titre):
        """
        Initialise un document

        Args:
            titre (str): Le titre du document
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

        Returns:
            str: Représentation CSV du document
        """
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un document à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV à parser

        Returns:
            Document: Instance du document approprié
        """
        raise NotImplementedError("Méthode à implémenter dans les sous-classes")

    def __str__(self):
        """Représentation textuelle du document"""
        return f"Document: {self._titre}"


class Volume(Document):
    """Classe représentant un volume (livre, BD, dictionnaire)"""

    def __init__(self, titre, auteur):
        """
        Initialise un volume

        Args:
            titre (str): Le titre du volume
            auteur (str): Le nom de l'auteur
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

        Args:
            titre (str): Le titre du livre
            auteur (str): Le nom de l'auteur
            disponible (bool): Si le livre est disponible pour emprunt
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

        Returns:
            bool: True si l'emprunt est possible, False sinon
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

        Returns:
            bool: True si disponible, False sinon
        """
        return self._disponible

    def to_csv(self):
        """
        Convertit le livre en format CSV

        Returns:
            str: Représentation CSV du livre
        """
        return f"Livre,{self._titre},{self._auteur},{self._disponible}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un livre à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV (format: Livre,titre,auteur,disponible)

        Returns:
            Livre: Instance du livre
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 4:
            disponible = parts[3].lower() == 'true'
            return Livre(parts[1], parts[2], disponible)
        return None

    def __str__(self):
        """Représentation textuelle du livre"""
        statut = "Disponible" if self._disponible else "Emprunté"
        return f"Livre: {self._titre} par {self._auteur} ({statut})"


class BD(Volume):
    """Classe représentant une bande dessinée"""

    def __init__(self, titre, auteur, dessinateur):
        """
        Initialise une BD

        Args:
            titre (str): Le titre de la BD
            auteur (str): Le nom de l'auteur/scénariste
            dessinateur (str): Le nom du dessinateur
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

        Returns:
            str: Représentation CSV de la BD
        """
        return f"BD,{self._titre},{self._auteur},{self._dessinateur}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée une BD à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV (format: BD,titre,auteur,dessinateur)

        Returns:
            BD: Instance de la BD
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 4:
            return BD(parts[1], parts[2], parts[3])
        return None

    def __str__(self):
        """Représentation textuelle de la BD"""
        return f"BD: {self._titre} par {self._auteur} (dessin: {self._dessinateur})"


class Dictionnaire(Volume):
    """Classe représentant un dictionnaire"""

    def __init__(self, titre, auteur):
        """
        Initialise un dictionnaire

        Args:
            titre (str): Le titre du dictionnaire
            auteur (str): Le nom de l'auteur/éditeur
        """
        super().__init__(titre, auteur)

    def to_csv(self):
        """
        Convertit le dictionnaire en format CSV

        Returns:
            str: Représentation CSV du dictionnaire
        """
        return f"Dictionnaire,{self._titre},{self._auteur}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un dictionnaire à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV (format: Dictionnaire,titre,auteur)

        Returns:
            Dictionnaire: Instance du dictionnaire
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

        Args:
            titre (str): Le titre du journal
            date_parution (date): La date de parution
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

        Returns:
            str: Représentation CSV du journal
        """
        date_str = self._date_parution.strftime('%Y-%m-%d')
        return f"Journal,{self._titre},{date_str}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un journal à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV (format: Journal,titre,date)

        Returns:
            Journal: Instance du journal
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 3:
            date_parts = parts[2].split('-')
            date_parution = date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            return Journal(parts[1], date_parution)
        return None

    def __str__(self):
        """Représentation textuelle du journal"""
        return f"Journal: {self._titre} du {self._date_parution.strftime('%d/%m/%Y')}"