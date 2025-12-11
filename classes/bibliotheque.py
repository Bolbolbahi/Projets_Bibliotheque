"""
Module contenant la classe Bibliotheque
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
        """
        if adherent not in self._adherents:
            self._adherents.append(adherent)
            return True
        return False

    def enlever_adherent(self, adherent):
        """
        Enlève un adhérent de la bibliothèque
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
        """
        for adherent in self._adherents:
            if adherent.nom == nom and adherent.prenom == prenom:
                return adherent
        return None

    def get_adherents(self):
        """
        Retourne la liste des adhérents
        """
        return self._adherents.copy()

    # ========== Gestion des Documents ==========

    def ajouter_document(self, document):
        """
        Ajoute un document à la bibliothèque
        """
        self._documents.append(document)
        return True

    def enlever_document(self, document):
        """
        Enlève un document de la bibliothèque
        """
        if document in self._documents:
            self._documents.remove(document)
            return True
        return False

    def rechercher_document(self, titre):
        """
        Recherche un document par titre
        """
        for document in self._documents:
            if document.titre.lower() == titre.lower():
                return document
        return None

    def get_documents(self):
        """
        Retourne la liste des documents
        """
        return self._documents.copy()

    def get_livres(self):
        """
        Retourne uniquement les livres de la bibliothèque
        """
        from classes.document import Livre
        return [doc for doc in self._documents if isinstance(doc, Livre)]

    def get_livres_disponibles(self):
        """
        Retourne les livres disponibles pour l'emprunt
        """
        from classes.document import Livre
        return [doc for doc in self._documents
                if isinstance(doc, Livre) and doc.disponible]

    # ========== Gestion des Emprunts ==========

    def ajouter_emprunt(self, adherent, livre):
        """
        Crée un nouvel emprunt
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
        """
        return self._emprunts.copy()

    def get_emprunts_actifs(self):
        """
        Retourne la liste des emprunts actifs (non encore retournés par leurs emprunteur respectifs )
        """
        return [e for e in self._emprunts if e.est_actif()]

    def get_emprunts_adherent(self, adherent):
        """
        Retourne les emprunts d'un adhérent
        """
        return [e for e in self._emprunts if e.adherent == adherent]

    def get_emprunts_en_retard(self):
        """
        Retourne les emprunts en retard
        """
        return [e for e in self._emprunts if e.est_en_retard()]

    # ========== Statistiques ==========

    def get_statistiques(self):
        """
        Retourne des statistiques sur la bibliothèque
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
        stats = self.get_statistiques()
        return (f"Bibliothèque - {stats['total_documents']} documents, "
                f"{stats['total_adherents']} adhérents, "
                f"{stats['emprunts_actifs']} emprunts actifs")