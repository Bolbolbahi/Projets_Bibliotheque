"""
Interface graphique PyQt6 pour le système de gestion de bibliothèque
Auteur: Votre Nom
Date: 2024
"""

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox, QMessageBox, QTabWidget,
                             QTableWidget, QTableWidgetItem, QGroupBox, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date, datetime

from classes.bibliotheque import Bibliotheque
from classes.document import Livre, BD, Dictionnaire, Journal
from classes.adherent import Adherent
from utils.file_manager import FileManager


class BibliothequeGUI(QWidget):
    """Interface graphique principale pour la bibliothèque"""

    def __init__(self):
        super().__init__()
        self.bibliotheque = FileManager.charger_bibliotheque()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Système de Gestion de Bibliothèque")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4CAF50;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()

        # Titre
        titre = QLabel("📚 BIBLIOTHÈQUE - SYSTÈME DE GESTION 📚")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; padding: 15px;")
        main_layout.addWidget(titre)

        # Onglets
        tabs = QTabWidget()
        tabs.addTab(self.create_adherents_tab(), "👥 Adhérents")
        tabs.addTab(self.create_documents_tab(), "📖 Documents")
        tabs.addTab(self.create_emprunts_tab(), "📋 Emprunts")
        tabs.addTab(self.create_stats_tab(), "📊 Statistiques")

        main_layout.addWidget(tabs)

        # Boutons d'action globaux
        btn_layout = QHBoxLayout()

        btn_sauvegarder = QPushButton("💾 Sauvegarder")
        btn_sauvegarder.clicked.connect(self.sauvegarder_donnees)
        btn_layout.addWidget(btn_sauvegarder)

        btn_actualiser = QPushButton("🔄 Actualiser")
        btn_actualiser.clicked.connect(self.actualiser_affichage)
        btn_layout.addWidget(btn_actualiser)

        btn_quitter = QPushButton("❌ Quitter")
        btn_quitter.setStyleSheet("background-color: #f44336;")
        btn_quitter.clicked.connect(self.close)
        btn_layout.addWidget(btn_quitter)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ========== Onglet Adhérents ==========

    def create_adherents_tab(self):
        """Crée l'onglet de gestion des adhérents"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulaire d'ajout
        form_group = QGroupBox("Ajouter un nouvel adhérent")
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Nom:"), 0, 0)
        self.adh_nom_input = QLineEdit()
        form_layout.addWidget(self.adh_nom_input, 0, 1)

        form_layout.addWidget(QLabel("Prénom:"), 1, 0)
        self.adh_prenom_input = QLineEdit()
        form_layout.addWidget(self.adh_prenom_input, 1, 1)

        form_layout.addWidget(QLabel("Email (optionnel):"), 2, 0)
        self.adh_email_input = QLineEdit()
        form_layout.addWidget(self.adh_email_input, 2, 1)

        btn_ajouter = QPushButton("➕ Ajouter Adhérent")
        btn_ajouter.clicked.connect(self.ajouter_adherent)
        form_layout.addWidget(btn_ajouter, 3, 0, 1, 2)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Liste des adhérents
        liste_group = QGroupBox("Liste des adhérents")
        liste_layout = QVBoxLayout()

        self.adherents_table = QTableWidget()
        self.adherents_table.setColumnCount(4)
        self.adherents_table.setHorizontalHeaderLabels(["Nom", "Prénom", "Email", "Actions"])
        self.adherents_table.horizontalHeader().setStretchLastSection(True)
        liste_layout.addWidget(self.adherents_table)

        liste_group.setLayout(liste_layout)
        layout.addWidget(liste_group)

        tab.setLayout(layout)
        self.actualiser_table_adherents()
        return tab

    def ajouter_adherent(self):
        """Ajoute un nouvel adhérent"""
        nom = self.adh_nom_input.text().strip()
        prenom = self.adh_prenom_input.text().strip()
        email = self.adh_email_input.text().strip()

        # Validation
        if not nom or not prenom:
            QMessageBox.warning(self, "Erreur", "Le nom et le prénom sont obligatoires!")
            return

        # Vérifier si l'adhérent existe déjà
        if self.bibliotheque.rechercher_adherent(nom, prenom):
            QMessageBox.warning(self, "Erreur", "Cet adhérent existe déjà!")
            return

        # Créer et ajouter l'adhérent
        adherent = Adherent(nom, prenom, email)
        self.bibliotheque.ajouter_adherent(adherent)

        # Réinitialiser le formulaire
        self.adh_nom_input.clear()
        self.adh_prenom_input.clear()
        self.adh_email_input.clear()

        self.actualiser_table_adherents()
        QMessageBox.information(self, "Succès", f"Adhérent {prenom} {nom} ajouté avec succès!")

    def supprimer_adherent(self, adherent):
        """Supprime un adhérent"""
        reply = QMessageBox.question(self, "Confirmation",
                                     f"Voulez-vous vraiment supprimer {adherent.prenom} {adherent.nom}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.bibliotheque.enlever_adherent(adherent):
                self.actualiser_table_adherents()
                QMessageBox.information(self, "Succès", "Adhérent supprimé!")
            else:
                QMessageBox.warning(self, "Erreur",
                                    "Impossible de supprimer cet adhérent (emprunts actifs)")

    def actualiser_table_adherents(self):
        """Actualise l'affichage de la table des adhérents"""
        adherents = self.bibliotheque.get_adherents()
        self.adherents_table.setRowCount(len(adherents))

        for i, adh in enumerate(adherents):
            self.adherents_table.setItem(i, 0, QTableWidgetItem(adh.nom))
            self.adherents_table.setItem(i, 1, QTableWidgetItem(adh.prenom))
            self.adherents_table.setItem(i, 2, QTableWidgetItem(adh.email))

            btn_suppr = QPushButton("🗑️ Supprimer")
            btn_suppr.setStyleSheet("background-color: #f44336;")
            btn_suppr.clicked.connect(lambda checked, a=adh: self.supprimer_adherent(a))
            self.adherents_table.setCellWidget(i, 3, btn_suppr)

    # ========== Onglet Documents ==========

    def create_documents_tab(self):
        """Crée l'onglet de gestion des documents"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulaire d'ajout
        form_group = QGroupBox("Ajouter un nouveau document")
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Type de document:"), 0, 0)
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems(["Livre", "BD", "Dictionnaire", "Journal"])
        self.doc_type_combo.currentTextChanged.connect(self.update_document_form)
        form_layout.addWidget(self.doc_type_combo, 0, 1)

        form_layout.addWidget(QLabel("Titre:"), 1, 0)
        self.doc_titre_input = QLineEdit()
        form_layout.addWidget(self.doc_titre_input, 1, 1)

        # Champs conditionnels
        self.doc_auteur_label = QLabel("Auteur:")
        form_layout.addWidget(self.doc_auteur_label, 2, 0)
        self.doc_auteur_input = QLineEdit()
        form_layout.addWidget(self.doc_auteur_input, 2, 1)

        self.doc_dessinateur_label = QLabel("Dessinateur:")
        form_layout.addWidget(self.doc_dessinateur_label, 3, 0)
        self.doc_dessinateur_input = QLineEdit()
        form_layout.addWidget(self.doc_dessinateur_input, 3, 1)

        self.doc_date_label = QLabel("Date de parution:")
        form_layout.addWidget(self.doc_date_label, 4, 0)
        self.doc_date_input = QDateEdit()
        self.doc_date_input.setDate(QDate.currentDate())
        self.doc_date_input.setCalendarPopup(True)
        form_layout.addWidget(self.doc_date_input, 4, 1)

        btn_ajouter_doc = QPushButton("➕ Ajouter Document")
        btn_ajouter_doc.clicked.connect(self.ajouter_document)
        form_layout.addWidget(btn_ajouter_doc, 5, 0, 1, 2)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Liste des documents
        liste_group = QGroupBox("Liste des documents")
        liste_layout = QVBoxLayout()

        self.documents_table = QTableWidget()
        self.documents_table.setColumnCount(5)
        self.documents_table.setHorizontalHeaderLabels(["Type", "Titre", "Info", "Statut", "Actions"])
        self.documents_table.horizontalHeader().setStretchLastSection(True)
        liste_layout.addWidget(self.documents_table)

        liste_group.setLayout(liste_layout)
        layout.addWidget(liste_group)

        tab.setLayout(layout)
        self.update_document_form()
        self.actualiser_table_documents()
        return tab

    def update_document_form(self):
        """Met à jour les champs du formulaire selon le type de document"""
        doc_type = self.doc_type_combo.currentText()

        # Cacher tous les champs conditionnels
        self.doc_auteur_label.hide()
        self.doc_auteur_input.hide()
        self.doc_dessinateur_label.hide()
        self.doc_dessinateur_input.hide()
        self.doc_date_label.hide()
        self.doc_date_input.hide()

        # Afficher selon le type
        if doc_type in ["Livre", "Dictionnaire"]:
            self.doc_auteur_label.show()
            self.doc_auteur_input.show()
        elif doc_type == "BD":
            self.doc_auteur_label.show()
            self.doc_auteur_input.show()
            self.doc_dessinateur_label.show()
            self.doc_dessinateur_input.show()
        elif doc_type == "Journal":
            self.doc_date_label.show()
            self.doc_date_input.show()

    def ajouter_document(self):
        """Ajoute un nouveau document"""
        doc_type = self.doc_type_combo.currentText()
        titre = self.doc_titre_input.text().strip()

        if not titre:
            QMessageBox.warning(self, "Erreur", "Le titre est obligatoire!")
            return

        # Vérifier si le document existe déjà
        if self.bibliotheque.rechercher_document(titre):
            QMessageBox.warning(self, "Erreur", "Ce document existe déjà!")
            return

        document = None

        if doc_type == "Livre":
            auteur = self.doc_auteur_input.text().strip()
            if not auteur:
                QMessageBox.warning(self, "Erreur", "L'auteur est obligatoire!")
                return
            document = Livre(titre, auteur)

        elif doc_type == "BD":
            auteur = self.doc_auteur_input.text().strip()
            dessinateur = self.doc_dessinateur_input.text().strip()
            if not auteur or not dessinateur:
                QMessageBox.warning(self, "Erreur", "L'auteur et le dessinateur sont obligatoires!")
                return
            document = BD(titre, auteur, dessinateur)

        elif doc_type == "Dictionnaire":
            auteur = self.doc_auteur_input.text().strip()
            if not auteur:
                QMessageBox.warning(self, "Erreur", "L'éditeur est obligatoire!")
                return
            document = Dictionnaire(titre, auteur)

        elif doc_type == "Journal":
            qdate = self.doc_date_input.date()
            date_parution = date(qdate.year(), qdate.month(), qdate.day())
            document = Journal(titre, date_parution)

        if document:
            self.bibliotheque.ajouter_document(document)
            self.doc_titre_input.clear()
            self.doc_auteur_input.clear()
            self.doc_dessinateur_input.clear()
            self.actualiser_table_documents()
            QMessageBox.information(self, "Succès", f"Document '{titre}' ajouté!")

    def supprimer_document(self, document):
        """Supprime un document"""
        reply = QMessageBox.question(self, "Confirmation",
                                     f"Voulez-vous vraiment supprimer '{document.titre}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.bibliotheque.enlever_document(document)
            self.actualiser_table_documents()
            QMessageBox.information(self, "Succès", "Document supprimé!")

    def actualiser_table_documents(self):
        """Actualise l'affichage de la table des documents"""
        documents = self.bibliotheque.get_documents()
        self.documents_table.setRowCount(len(documents))

        for i, doc in enumerate(documents):
            # Type
            doc_type = doc.__class__.__name__
            self.documents_table.setItem(i, 0, QTableWidgetItem(doc_type))

            # Titre
            self.documents_table.setItem(i, 1, QTableWidgetItem(doc.titre))

            # Info
            info = ""
            if hasattr(doc, 'auteur'):
                info = f"Auteur: {doc.auteur}"
            if hasattr(doc, 'dessinateur'):
                info += f" | Dessin: {doc.dessinateur}"
            if hasattr(doc, 'date_parution'):
                info = f"Date: {doc.date_parution.strftime('%d/%m/%Y')}"
            self.documents_table.setItem(i, 2, QTableWidgetItem(info))

            # Statut
            statut = ""
            if isinstance(doc, Livre):
                statut = "✅ Disponible" if doc.disponible else "❌ Emprunté"
            else:
                statut = "📚 Consultation sur place"
            self.documents_table.setItem(i, 3, QTableWidgetItem(statut))

            # Actions
            btn_suppr = QPushButton("🗑️ Supprimer")
            btn_suppr.setStyleSheet("background-color: #f44336;")
            btn_suppr.clicked.connect(lambda checked, d=doc: self.supprimer_document(d))
            self.documents_table.setCellWidget(i, 4, btn_suppr)

    # ========== Onglet Emprunts ==========

    def create_emprunts_tab(self):
        """Crée l'onglet de gestion des emprunts"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Formulaire d'emprunt
        form_group = QGroupBox("Nouvel emprunt")
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Adhérent:"), 0, 0)
        self.emp_adherent_combo = QComboBox()
        form_layout.addWidget(self.emp_adherent_combo, 0, 1)

        form_layout.addWidget(QLabel("Livre:"), 1, 0)
        self.emp_livre_combo = QComboBox()
        form_layout.addWidget(self.emp_livre_combo, 1, 1)

        btn_emprunter = QPushButton("📤 Emprunter Livre")
        btn_emprunter.clicked.connect(self.creer_emprunt)
        form_layout.addWidget(btn_emprunter, 2, 0, 1, 2)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Formulaire de retour
        retour_group = QGroupBox("Retour d'emprunt")
        retour_layout = QGridLayout()

        retour_layout.addWidget(QLabel("Sélectionner un emprunt actif:"), 0, 0)
        self.ret_emprunt_combo = QComboBox()
        retour_layout.addWidget(self.ret_emprunt_combo, 0, 1)

        btn_retourner = QPushButton("📥 Retourner Livre")
        btn_retourner.clicked.connect(self.retourner_livre)
        retour_layout.addWidget(btn_retourner, 1, 0, 1, 2)

        retour_group.setLayout(retour_layout)
        layout.addWidget(retour_group)

        # Liste des emprunts
        liste_group = QGroupBox("Liste des emprunts")
        liste_layout = QVBoxLayout()

        self.emprunts_table = QTableWidget()
        self.emprunts_table.setColumnCount(5)
        self.emprunts_table.setHorizontalHeaderLabels(["Adhérent", "Livre", "Date Emprunt",
                                                       "Date Retour", "Statut"])
        self.emprunts_table.horizontalHeader().setStretchLastSection(True)
        liste_layout.addWidget(self.emprunts_table)

        liste_group.setLayout(liste_layout)
        layout.addWidget(liste_group)

        tab.setLayout(layout)
        self.actualiser_combos_emprunts()
        self.actualiser_table_emprunts()
        return tab

    def actualiser_combos_emprunts(self):
        """Actualise les listes déroulantes pour les emprunts"""
        # Adhérents
        self.emp_adherent_combo.clear()
        for adh in self.bibliotheque.get_adherents():
            self.emp_adherent_combo.addItem(f"{adh.prenom} {adh.nom}", adh)

        # Livres disponibles
        self.emp_livre_combo.clear()
        for livre in self.bibliotheque.get_livres_disponibles():
            self.emp_livre_combo.addItem(f"{livre.titre} ({livre.auteur})", livre)

        # Emprunts actifs pour retour
        self.ret_emprunt_combo.clear()
        for emp in self.bibliotheque.get_emprunts_actifs():
            text = f"{emp.livre.titre} - {emp.adherent.prenom} {emp.adherent.nom}"
            self.ret_emprunt_combo.addItem(text, emp)

    def creer_emprunt(self):
        """Crée un nouvel emprunt"""
        if self.emp_adherent_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun adhérent disponible!")
            return

        if self.emp_livre_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun livre disponible!")
            return

        adherent = self.emp_adherent_combo.currentData()
        livre = self.emp_livre_combo.currentData()

        success, message = self.bibliotheque.ajouter_emprunt(adherent, livre)

        if success:
            QMessageBox.information(self, "Succès", message)
            self.actualiser_combos_emprunts()
            self.actualiser_table_emprunts()
            self.actualiser_table_documents()
        else:
            QMessageBox.warning(self, "Erreur", message)

    def retourner_livre(self):
        """Enregistre le retour d'un livre"""
        if self.ret_emprunt_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun emprunt actif!")
            return

        emprunt = self.ret_emprunt_combo.currentData()
        success, message = self.bibliotheque.retourner_emprunt(emprunt.adherent, emprunt.livre)

        if success:
            QMessageBox.information(self, "Succès", message)
            self.actualiser_combos_emprunts()
            self.actualiser_table_emprunts()
            self.actualiser_table_documents()
        else:
            QMessageBox.warning(self, "Erreur", message)

    def actualiser_table_emprunts(self):
        """Actualise l'affichage de la table des emprunts"""
        emprunts = self.bibliotheque.get_emprunts()
        self.emprunts_table.setRowCount(len(emprunts))

        for i, emp in enumerate(emprunts):
            # Adhérent
            adherent_text = f"{emp.adherent.prenom} {emp.adherent.nom}"
            self.emprunts_table.setItem(i, 0, QTableWidgetItem(adherent_text))

            # Livre
            self.emprunts_table.setItem(i, 1, QTableWidgetItem(emp.livre.titre))

            # Date emprunt
            date_emp = emp.date_emprunt.strftime('%d/%m/%Y')
            self.emprunts_table.setItem(i, 2, QTableWidgetItem(date_emp))

            # Date retour
            date_ret = emp.date_retour.strftime('%d/%m/%Y') if emp.date_retour else "En cours"
            self.emprunts_table.setItem(i, 3, QTableWidgetItem(date_ret))

            # Statut
            if emp.est_actif():
                if emp.est_en_retard():
                    statut = f"⚠️ RETARD ({emp.jours_retard()} j)"
                else:
                    statut = "✅ En cours"
            else:
                statut = "✔️ Retourné"
            self.emprunts_table.setItem(i, 4, QTableWidgetItem(statut))

    # ========== Onglet Statistiques ==========

    def create_stats_tab(self):
        """Crée l'onglet des statistiques"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Zone de texte pour les statistiques
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.stats_text)

        btn_actualiser_stats = QPushButton("🔄 Actualiser les statistiques")
        btn_actualiser_stats.clicked.connect(self.actualiser_statistiques)
        layout.addWidget(btn_actualiser_stats)

        tab.setLayout(layout)
        self.actualiser_statistiques()
        return tab

    def actualiser_statistiques(self):
        """Actualise l'affichage des statistiques"""
        stats = self.bibliotheque.get_statistiques()

        text = f"""
        📊 STATISTIQUES DE LA BIBLIOTHÈQUE
        ═══════════════════════════════════════

        📚 DOCUMENTS
        ─────────────────
        • Total de documents : {stats['total_documents']}
        • Livres : {stats['total_livres']}
        • Livres disponibles : {stats['livres_disponibles']}
        • Livres empruntés : {stats['livres_empruntes']}

        👥 ADHÉRENTS
        ─────────────────
        • Total d'adhérents : {stats['total_adherents']}

        📋 EMPRUNTS
        ─────────────────
        • Total d'emprunts (historique) : {stats['total_emprunts']}
        • Emprunts actifs : {stats['emprunts_actifs']}
        • Emprunts en retard : {stats['emprunts_retard']}
        """

        # Ajouter liste des retards
        retards = self.bibliotheque.get_emprunts_en_retard()
        if retards:
            text += "\n\n⚠️  EMPRUNTS EN RETARD\n─────────────────\n"
            for emp in retards:
                text += f"• {emp.livre.titre} - {emp.adherent.prenom} {emp.adherent.nom} "
                text += f"({emp.jours_retard()} jours de retard)\n"

        self.stats_text.setPlainText(text)

    # ========== Actions globales ==========

    def sauvegarder_donnees(self):
        """Sauvegarde toutes les données"""
        if FileManager.sauvegarder_bibliotheque(self.bibliotheque):
            QMessageBox.information(self, "Succès", "Données sauvegardées avec succès!")
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la sauvegarde!")

    def actualiser_affichage(self):
        """Actualise tous les affichages"""
        self.actualiser_table_adherents()
        self.actualiser_table_documents()
        self.actualiser_combos_emprunts()
        self.actualiser_table_emprunts()
        self.actualiser_statistiques()
        QMessageBox.information(self, "Succès", "Affichage actualisé!")

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        reply = QMessageBox.question(self, "Confirmation",
                                     "Voulez-vous sauvegarder avant de quitter?",
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No |
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Yes:
            self.sauvegarder_donnees()
            event.accept()
        elif reply == QMessageBox.StandardButton.No:
            event.accept()
        else:
            event.ignore()


def lancer_application():
    """Lance l'application GUI"""
    import sys
    app = QApplication(sys.argv)
    fenetre = BibliothequeGUI()
    fenetre.show()
    sys.exit(app.exec())