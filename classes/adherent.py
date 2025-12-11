"""
Module contenant la classe Adherent
Auteur: Votre Nom
Date: 2024
"""


class Adherent:
    """Classe représentant un adhérent de la bibliothèque"""

    def __init__(self, nom, prenom, email=""):
        """
        Initialise un adhérent

        Args:
            nom (str): Le nom de l'adhérent
            prenom (str): Le prénom de l'adhérent
            email (str): L'email de l'adhérent (optionnel)
        """
        self._nom = nom
        self._prenom = prenom
        self._email = email

    @property
    def nom(self):
        """Retourne le nom de l'adhérent"""
        return self._nom

    @nom.setter
    def nom(self, value):
        """Modifie le nom de l'adhérent"""
        self._nom = value

    @property
    def prenom(self):
        """Retourne le prénom de l'adhérent"""
        return self._prenom

    @prenom.setter
    def prenom(self, value):
        """Modifie le prénom de l'adhérent"""
        self._prenom = value

    @property
    def email(self):
        """Retourne l'email de l'adhérent"""
        return self._email

    @email.setter
    def email(self, value):
        """Modifie l'email de l'adhérent"""
        self._email = value

    def emprunter_livre(self, livre):
        """
        Emprunte un livre (méthode pour compatibilité avec le diagramme UML)

        Args:
            livre (Livre): Le livre à emprunter

        Returns:
            bool: True si l'emprunt est réussi, False sinon
        """
        if livre.empruntable():
            return livre.emprunter()
        return False

    def rendre_livre(self, livre):
        """
        Rend un livre (méthode pour compatibilité avec le diagramme UML)

        Args:
            livre (Livre): Le livre à rendre
        """
        livre.rendre()

    def get_identifiant(self):
        """
        Retourne un identifiant unique pour l'adhérent

        Returns:
            str: Identifiant au format "NOM_PRENOM"
        """
        return f"{self._nom}_{self._prenom}"

    def to_csv(self):
        """
        Convertit l'adhérent en format CSV

        Returns:
            str: Représentation CSV de l'adhérent
        """
        return f"{self._nom},{self._prenom},{self._email}"

    @staticmethod
    def from_csv(csv_line):
        """
        Crée un adhérent à partir d'une ligne CSV

        Args:
            csv_line (str): Ligne CSV (format: nom,prenom,email)

        Returns:
            Adherent: Instance de l'adhérent
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 2:
            email = parts[2] if len(parts) > 2 else ""
            return Adherent(parts[0], parts[1], email)
        return None

    def __str__(self):
        """Représentation textuelle de l'adhérent"""
        if self._email:
            return f"{self._prenom} {self._nom} ({self._email})"
        return f"{self._prenom} {self._nom}"

    def __eq__(self, other):
        """
        Compare deux adhérents

        Args:
            other (Adherent): Autre adhérent à comparer

        Returns:
            bool: True si les adhérents sont identiques
        """
        if not isinstance(other, Adherent):
            return False
        return (self._nom == other._nom and
                self._prenom == other._prenom)