"""
Module contenant la classe Bibliotheque
Auteur: Votre Nom
Date: 2024
"""

from datetime import date


class Bibliotheque:
    """Classe représentant la bibliothèque et sa gestion"""

    def __init__(self):
        """Initialise une nouvelle bibliothèque"""
        self._documents = []
        self._adherents = []
        self._emprunts = []

    # ========== Gestion des Adhérents ==========

    def ajouter_adherent(self, adherent):
        """
        Ajoute un adhérent à la bibliothèque

        Args:
            adherent (Adherent): L'adhérent à ajouter

        Returns:
            bool: True si ajouté, False si déjà existant
        """
        if adherent not in self._adherents:
            self._adherents.append(adherent)
            return True
        return False

    def enlever_adherent(self, adherent):
        """
        Enlève un adhérent de la bibliothèque

        Args:
            adherent (Adherent): L'adhérent à enlever

        Returns:
            bool: True si enlevé, False si non trouvé
        """
        # Vérifier si l'adhérent a des emprunts actifs
        emprunts_actifs = [e for e in self._emprunts
                           if e.adherent == adherent and e.est_actif()]

        if emprunts_actifs:
            return False  # Ne peut pas supprimer un adhérent avec des emprunts actifs

        if adherent in self._adherents:
            self._adherents.remove(adherent)
            return True
        return False

    def rechercher_adherent(self, nom, prenom):
        """
        Recherche un adhérent par nom et prénom

        Args:
            nom (str): Le nom de l'adhérent
            prenom (str): Le prénom de l'adhérent

        Returns:
            Adherent: L'adhérent trouvé ou None
        """
        for adherent in self._adherents:
            if adherent.nom == nom and adherent.prenom == prenom:
                return adherent
        return None

    def get_adherents(self):
        """
        Retourne la liste des adhérents

        Returns:
            list: Liste des adhérents
        """
        return self._adherents.copy()

    # ========== Gestion des Documents ==========

    def ajouter_document(self, document):
        """
        Ajoute un document à la bibliothèque

        Args:
            document (Document): Le document à ajouter

        Returns:
            bool: True si ajouté avec succès
        """
        self._documents.append(document)
        return True

    def enlever_document(self, document):
        """
        Enlève un document de la bibliothèque

        Args:
            document (Document): Le document à enlever

        Returns:
            bool: True si enlevé, False si non trouvé
        """
        if document in self._documents:
            self._documents.remove(document)
            return True
        return False

    def rechercher_document(self, titre):
        """
        Recherche un document par titre

        Args:
            titre (str): Le titre du document

        Returns:
            Document: Le document trouvé ou None
        """
        for document in self._documents:
            if document.titre.lower() == titre.lower():
                return document
        return None

    def get_documents(self):
        """
        Retourne la liste des documents

        Returns:
            list: Liste des documents
        """
        return self._documents.copy()

    def get_livres(self):
        """
        Retourne uniquement les livres de la bibliothèque

        Returns:
            list: Liste des livres
        """
        from classes.document import Livre
        return [doc for doc in self._documents if isinstance(doc, Livre)]

    def get_livres_disponibles(self):
        """
        Retourne les livres disponibles pour l'emprunt

        Returns:
            list: Liste des livres disponibles
        """
        from classes.document import Livre
        return [doc for doc in self._documents
                if isinstance(doc, Livre) and doc.disponible]

    # ========== Gestion des Emprunts ==========

    def ajouter_emprunt(self, adherent, livre):
        """
        Crée un nouvel emprunt

        Args:
            adherent (Adherent): L'adhérent qui emprunte
            livre (Livre): Le livre à emprunter

        Returns:
            tuple: (bool, str) - (succès, message)
        """
        from classes.emprunt import Emprunt

        # Vérifications
        if adherent not in self._adherents:
            return False, "Adhérent non inscrit à la bibliothèque"

        if livre not in self._documents:
            return False, "Livre non disponible dans la bibliothèque"

        if not livre.empruntable():
            return False, "Livre déjà emprunté"

        # Créer l'emprunt
        emprunt = Emprunt(adherent, livre)
        livre.emprunter()
        self._emprunts.append(emprunt)

        return True, f"Emprunt créé avec succès. Date de retour prévue: {emprunt.calculer_date_retour_prevue().strftime('%d/%m/%Y')}"

    def retourner_emprunt(self, adherent, livre):
        """
        Enregistre le retour d'un livre

        Args:
            adherent (Adherent): L'adhérent qui retourne le livre
            livre (Livre): Le livre retourné

        Returns:
            tuple: (bool, str) - (succès, message)
        """
        # Trouver l'emprunt actif correspondant
        for emprunt in self._emprunts:
            if (emprunt.adherent == adherent and
                    emprunt.livre == livre and
                    emprunt.est_actif()):

                emprunt.date_retour = date.today()
                livre.rendre()

                if emprunt.est_en_retard():
                    jours = emprunt.jours_retard()
                    return True, f"Livre retourné avec {jours} jour(s) de retard"
                else:
                    return True, "Livre retourné avec succès"

        return False, "Aucun emprunt actif trouvé pour ce livre et cet adhérent"

    def get_emprunts(self):
        """
        Retourne la liste de tous les emprunts

        Returns:
            list: Liste des emprunts
        """
        return self._emprunts.copy()

    def get_emprunts_actifs(self):
        """
        Retourne la liste des emprunts actifs (non retournés)

        Returns:
            list: Liste des emprunts actifs
        """
        return [e for e in self._emprunts if e.est_actif()]

    def get_emprunts_adherent(self, adherent):
        """
        Retourne les emprunts d'un adhérent

        Args:
            adherent (Adherent): L'adhérent concerné

        Returns:
            list: Liste des emprunts de l'adhérent
        """
        return [e for e in self._emprunts if e.adherent == adherent]

    def get_emprunts_en_retard(self):
        """
        Retourne les emprunts en retard

        Returns:
            list: Liste des emprunts en retard
        """
        return [e for e in self._emprunts if e.est_en_retard()]

    # ========== Statistiques ==========

    def get_statistiques(self):
        """
        Retourne des statistiques sur la bibliothèque

        Returns:
            dict: Dictionnaire contenant les statistiques
        """
        from classes.document import Livre

        livres = self.get_livres()
        livres_disponibles = self.get_livres_disponibles()
        emprunts_actifs = self.get_emprunts_actifs()
        emprunts_retard = self.get_emprunts_en_retard()

        return {
            'total_documents': len(self._documents),
            'total_livres': len(livres),
            'livres_disponibles': len(livres_disponibles),
            'livres_empruntes': len(livres) - len(livres_disponibles),
            'total_adherents': len(self._adherents),
            'emprunts_actifs': len(emprunts_actifs),
            'emprunts_retard': len(emprunts_retard),
            'total_emprunts': len(self._emprunts)
        }

    def __str__(self):
        """Représentation textuelle de la bibliothèque"""
        stats = self.get_statistiques()
        return (f"Bibliothèque - {stats['total_documents']} documents, "
                f"{stats['total_adherents']} adhérents, "
                f"{stats['emprunts_actifs']} emprunts actifs")