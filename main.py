"""
Point d'entrée principal pour le système de gestion de bibliothèque
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.interface import lancer_application
from utils.file_manager import FileManager


def initialiser_application():
    """Initialise l'application et crée les données de test si nécessaire"""
    print("=" * 60)
    print("  SYSTÈME DE GESTION DE BIBLIOTHÈQUE")
    print("=" * 60)
    print("\n Initialisation de l'application...")

    # Créer le dossier data et les fichiers s'ils n'existent pas
    FileManager.initialiser_fichiers()
    print("✓ Fichiers de données initialisés")

    # Vérifier si les fichiers sont vides (première utilisation)
    if os.path.getsize(FileManager.ADHERENTS_FILE) == 0:
        print("\n Première utilisation détectée")
        reponse = input("Voulez-vous créer des données de test? (o/n): ")

        if reponse.lower() in ['o', 'oui', 'y', 'yes']:
            print("Création des données de test...")
            FileManager.creer_donnees_test()
            print("✓ Données de test créées avec succès!")
            print("\nDonnées créées:")
            print("  • 3 adhérents")
            print("  • 8 documents (3 livres, 2 BD, 1 dictionnaire, 2 journaux)")
            print("  • 1 emprunt actif")

    print("\n✓ Application prête!")
    print("=" * 60)
    print()


def main():
    """Fonction principale"""
    try:
        # Initialiser l'application
        initialiser_application()

        # Lancer l'interface graphique
        lancer_application()

    except KeyboardInterrupt:
        print("\n\n Application interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()