# Projets_Bibliotheque
Le nouveau projet de programmation orientée objet 

#Structure du projet : 

bibliotheque/
├── README.md
├── LICENSE
├── requirements.txt
├── main.py                 # Point d'entrée
├── classes/
│   ├── __init__.py
│   ├── document.py         # Classes Document, Livre, BD, etc.
│   ├── adherent.py         # Classe Adherent
│   ├── emprunt.py          # Classe Emprunt
│   └── bibliotheque.py     # Classe Bibliotheque
├── gui/
│   ├── __init__.py
│   └── interface.py        # Interface PyQt6
├── utils/
│   ├── __init__.py
│   └── file_manager.py     # Gestion fichiers CSV
└── data/
    ├── Adherents.txt       # Données adhérents (créé automatiquement)
    ├── Emprunts.txt        # Données emprunts (créé automatiquement)
    └── Biblio.txt          # Données documents (créé automatiquement)

Fonctionnalités

1- Gestion des Adhérents

- Ajouter un adhérent (nom, prénom, email)
- Supprimer un adhérent
- Afficher tous les adhérents
- Validation des données (empêche la suppression si emprunts actifs)

2- Gestion des Documents

- Ajouter des documents (Livre, BD, Dictionnaire, Journal)
- Supprimer des documents
- Afficher tous les documents avec leur statut
- Formulaire dynamique selon le type de document

3- Gestion des Emprunts

- Créer un emprunt (adhérent + livre disponible)
- Retourner un livre
- Afficher tous les emprunts (actifs et historique)
- Détection automatique des retards
- Calcul du nombre de jours de retard

4- Statistiques

- Vue d'ensemble complète
- Nombre de documents, livres, adhérents
- Emprunts actifs et en retard
- Liste détaillée des retards

5- Persistance des Données

- Sauvegarde automatique dans des fichiers CSV
- Chargement au démarrage
- Option de sauvegarde manuelle
- Données de test pour la première utilisation

Utilisation et navigation

L'application est organisée en 4 onglets :
 Adhérents : Gestion des membres de la bibliothèque
 Documents : Gestion du catalogue
 Emprunts : Gestion des prêts et retours
 Statistiques : Vue d'ensemble et suivi des retards

Workflow typique

Ajouter des adhérents dans l'onglet Adhérents
Ajouter des documents dans l'onglet Documents
Créer des emprunts dans l'onglet Emprunts
Retourner les livres dans le même onglet
Consulter les statistiques pour suivre l'activité
Sauvegarder régulièrement (bouton en bas)

Diagramme UML
	
Le système respecte le diagramme UML fourni avec :
Héritage : Document → Volume → (Livre, BD, Dictionnaire) et Journal
Association : Bibliotheque contient des Document et des Adherent
Composition : Emprunt relie un Adherent et un Livre

Interface

L'interface PyQt6 offre :
Design moderne et intuitif
Formulaires dynamiques avec validation
Tables interactives
Messages de confirmation et d'erreur
Boutons d'action contextuels
Sauvegarde avant fermeture

Règles de gestion

Seuls les livres peuvent être empruntés (pas les BD, dictionnaires ou journaux)
Un adhérent ne peut pas être supprimé s'il a des emprunts actifs
La durée d'emprunt est de 14 jours
Les retards sont calculés automatiquement
Un livre emprunté ne peut pas être emprunté à nouveau tant qu'il n'est pas retourné

Notes de développement

Respect des spécifications
- Partie 1 : Toutes les classes implémentées selon le diagramme UML
- Partie 2 : Interface complète (GUI au lieu de menu console)
- Partie 3 : Persistance CSV avec chargement/sauvegarde
- Partie 4 : Validation complète des entrées utilisateur
- Partie 5 : Code structuré, commenté, avec standards Python

Standards de programmation

- Nomenclature PEP8
- Docstrings pour toutes les méthodes
- Gestion des erreurs avec try/except
- Utilisation de l'héritage et polymorphisme
- Properties pour l'encapsulation
- Code modulaire et réutilisable

Support

Pour toute question ou problème, créez une issue sur le dépôt GitHub.

Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.