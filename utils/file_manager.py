"""
Module de gestion des fichiers CSV pour la bibliothèque
"""

import os
from classes.document import Livre, BD, Dictionnaire, Journal
from classes.adherent import Adherent
from classes.emprunt import Emprunt
from datetime import date


class FileManager:
    """Gestionnaire de fichiers CSV pour la persistance des données"""

    # Chemins des fichiers
    DATA_DIR = "data"
    ADHERENTS_FILE = os.path.join(DATA_DIR, "Adherents.txt")
    EMPRUNTS_FILE = os.path.join(DATA_DIR, "Emprunts.txt")
    BIBLIO_FILE = os.path.join(DATA_DIR, "Biblio.txt")

    @staticmethod
    def initialiser_dossier_data():
        """Crée le dossier data s'il n'existe pas"""
        if not os.path.exists(FileManager.DATA_DIR):
            os.makedirs(FileManager.DATA_DIR)

    @staticmethod
    def initialiser_fichiers():
        """Crée les fichiers s'ils n'existent pas"""
        FileManager.initialiser_dossier_data()

        for filepath in [FileManager.ADHERENTS_FILE,
                         FileManager.EMPRUNTS_FILE,
                         FileManager.BIBLIO_FILE]:
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    pass  # Crée un fichier vide

    # ========== Sauvegarde ==========

    @staticmethod
    def sauvegarder_adherents(adherents):
        """
        Sauvegarde les adhérents dans le fichier CSV
        """
        try:
            FileManager.initialiser_dossier_data()
            with open(FileManager.ADHERENTS_FILE, 'w', encoding='utf-8') as f:
                for adherent in adherents:
                    f.write(adherent.to_csv() + '\n')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des adhérents: {e}")
            return False

    @staticmethod
    def sauvegarder_documents(documents):
        """
        Sauvegarde les documents dans le fichier CSV
        """
        try:
            FileManager.initialiser_dossier_data()
            with open(FileManager.BIBLIO_FILE, 'w', encoding='utf-8') as f:
                for document in documents:
                    f.write(document.to_csv() + '\n')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des documents: {e}")
            return False

    @staticmethod
    def sauvegarder_emprunts(emprunts):
        """
        Sauvegarde les emprunts dans le fichier CSV
        """
        try:
            FileManager.initialiser_dossier_data()
            with open(FileManager.EMPRUNTS_FILE, 'w', encoding='utf-8') as f:
                for emprunt in emprunts:
                    f.write(emprunt.to_csv() + '\n')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des emprunts: {e}")
            return False

    @staticmethod
    def sauvegarder_bibliotheque(bibliotheque):
        """
        Sauvegarde toutes les données de la bibliothèque
        """
        success = True
        success &= FileManager.sauvegarder_adherents(bibliotheque.get_adherents())
        success &= FileManager.sauvegarder_documents(bibliotheque.get_documents())
        success &= FileManager.sauvegarder_emprunts(bibliotheque.get_emprunts())
        return success

    # ========== Chargement ==========

    @staticmethod
    def charger_adherents():
        """
        Charge les adhérents depuis le fichier CSV
        """
        adherents = []
        adherents_dict = {}

        try:
            if os.path.exists(FileManager.ADHERENTS_FILE):
                with open(FileManager.ADHERENTS_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            adherent = Adherent.from_csv(line)
                            if adherent:
                                adherents.append(adherent)
                                adherents_dict[adherent.get_identifiant()] = adherent
        except Exception as e:
            print(f"Erreur lors du chargement des adhérents: {e}")

        return adherents, adherents_dict

    @staticmethod
    def charger_documents():
        """
        Charge les documents depuis le fichier CSV
        """
        documents = []
        documents_dict = {}
        livres_dict = {}

        try:
            if os.path.exists(FileManager.BIBLIO_FILE):
                with open(FileManager.BIBLIO_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            # Déterminer le type de document
                            parts = line.split(',')
                            if len(parts) > 0:
                                doc_type = parts[0]
                                document = None

                                if doc_type == "Livre":
                                    document = Livre.from_csv(line)
                                    if document:
                                        livres_dict[document.titre] = document
                                elif doc_type == "BD":
                                    document = BD.from_csv(line)
                                elif doc_type == "Dictionnaire":
                                    document = Dictionnaire.from_csv(line)
                                elif doc_type == "Journal":
                                    document = Journal.from_csv(line)

                                if document:
                                    documents.append(document)
                                    documents_dict[document.titre] = document
        except Exception as e:
            print(f"Erreur lors du chargement des documents: {e}")

        return documents, documents_dict, livres_dict

    @staticmethod
    def charger_emprunts(adherents_dict, livres_dict):
        """
        Charge les emprunts depuis le fichier CSV
        """
        emprunts = []

        try:
            if os.path.exists(FileManager.EMPRUNTS_FILE):
                with open(FileManager.EMPRUNTS_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            emprunt = Emprunt.from_csv(line, adherents_dict, livres_dict)
                            if emprunt:
                                emprunts.append(emprunt)
        except Exception as e:
            print(f"Erreur lors du chargement des emprunts: {e}")

        return emprunts

    @staticmethod
    def charger_bibliotheque():
        """
        Charge toutes les données de la bibliothèque
        """
        from classes.bibliotheque import Bibliotheque

        FileManager.initialiser_fichiers()

        bibliotheque = Bibliotheque()

        # Charger les adhérents
        adherents, adherents_dict = FileManager.charger_adherents()
        for adherent in adherents:
            bibliotheque.ajouter_adherent(adherent)

        # Charger les documents
        documents, documents_dict, livres_dict = FileManager.charger_documents()
        for document in documents:
            bibliotheque.ajouter_document(document)

        # Charger les emprunts
        emprunts = FileManager.charger_emprunts(adherents_dict, livres_dict)
        for emprunt in emprunts:
            bibliotheque._emprunts.append(emprunt)

        return bibliotheque

    # ========== Données de test ==========

    @staticmethod
    def creer_donnees_test():
        """Crée des données de test pour la bibliothèque"""
        from classes.bibliotheque import Bibliotheque

        bibliotheque = Bibliotheque()

        # Créer des adhérents
        adh1 = Adherent("Dupont", "Marie", "marie.dupont@email.com")
        adh2 = Adherent("Martin", "Pierre", "pierre.martin@email.com")
        adh3 = Adherent("Lefebvre", "Sophie")

        bibliotheque.ajouter_adherent(adh1)
        bibliotheque.ajouter_adherent(adh2)
        bibliotheque.ajouter_adherent(adh3)

        # Créer des documents
        livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", True)
        livre2 = Livre("1984", "George Orwell", True)
        livre3 = Livre("Harry Potter à l'école des sorciers", "J.K. Rowling", False)

        bd1 = BD("Astérix et Obélix", "René Goscinny", "Albert Uderzo")
        bd2 = BD("Tintin au Tibet", "Hergé", "Hergé")

        dict1 = Dictionnaire("Larousse 2024", "Éditions Larousse")

        journal1 = Journal("Le Monde", date(2024, 12, 10))
        journal2 = Journal("Le Figaro", date(2024, 12, 11))

        bibliotheque.ajouter_document(livre1)
        bibliotheque.ajouter_document(livre2)
        bibliotheque.ajouter_document(livre3)
        bibliotheque.ajouter_document(bd1)
        bibliotheque.ajouter_document(bd2)
        bibliotheque.ajouter_document(dict1)
        bibliotheque.ajouter_document(journal1)
        bibliotheque.ajouter_document(journal2)

        # Créer quelques emprunts
        bibliotheque.ajouter_emprunt(adh1, livre3)

        # Sauvegarder
        FileManager.sauvegarder_bibliotheque(bibliotheque)

        return bibliotheque