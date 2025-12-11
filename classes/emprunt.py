"""
Module contenant la classe Emprunt
"""

from datetime import date, timedelta


class Emprunt:
    """Classe représentant un emprunt de livre par un adhérent"""

    # Durée d'emprunt par défaut (14 jours)
    DUREE_EMPRUNT_JOURS = 14

    def __init__(self, adherent, livre, date_emprunt=None, date_retour=None):
        """
        Initialise un emprunt
        """
        self._adherent = adherent
        self._livre = livre
        self._date_emprunt = date_emprunt if date_emprunt else date.today()
        self._date_retour = date_retour

    @property
    def adherent(self):
        """Retourne l'adhérent de l'emprunt"""
        return self._adherent

    @property
    def livre(self):
        """Retourne le livre de l'emprunt"""
        return self._livre

    @property
    def date_emprunt(self):
        """Retourne la date d'emprunt"""
        return self._date_emprunt

    @date_emprunt.setter
    def date_emprunt(self, value):
        """Modifie la date d'emprunt"""
        self._date_emprunt = value

    @property
    def date_retour(self):
        """Retourne la date de retour"""
        return self._date_retour

    @date_retour.setter
    def date_retour(self, value):
        """Modifie la date de retour"""
        self._date_retour = value

    def prolonger_date_retour(self, jours=7):
        """
        Prolonge la date de retour prévue
        """
        if self._date_retour:
            self._date_retour += timedelta(days=jours)
        else:
            date_retour_prevue = self._date_emprunt + timedelta(days=self.DUREE_EMPRUNT_JOURS)
            self._date_retour = date_retour_prevue + timedelta(days=jours)

    def calculer_date_retour_prevue(self):
        """
        Calcule la date de retour prévue
        """
        return self._date_emprunt + timedelta(days=self.DUREE_EMPRUNT_JOURS)

    def est_en_retard(self):
        """
        Vérifie si l'emprunt est en retard
        """
        if self._date_retour:
            return False  # Déjà retourné

        date_limite = self.calculer_date_retour_prevue()
        return date.today() > date_limite

    def jours_retard(self):
        """
        Calcule le nombre de jours de retard
        """
        if not self.est_en_retard():
            return 0

        date_limite = self.calculer_date_retour_prevue()
        delta = date.today() - date_limite
        return delta.days

    def est_actif(self):
        """
        Vérifie si l'emprunt est toujours actif (livre non encore retourné)
        """
        return self._date_retour is None

    def to_csv(self):
        """
        Convertit l'emprunt en format CSV
        """
        adherent_id = self._adherent.get_identifiant()
        livre_titre = self._livre.titre
        date_emp_str = self._date_emprunt.strftime('%Y-%m-%d')
        date_ret_str = self._date_retour.strftime('%Y-%m-%d') if self._date_retour else "None"
        return f"{adherent_id},{livre_titre},{date_emp_str},{date_ret_str}"

    @staticmethod
    def from_csv(csv_line, adherents_dict, livres_dict):
        """
        Crée un emprunt à partir d'une ligne CSV
        """
        parts = csv_line.strip().split(',')
        if len(parts) >= 4:
            adherent_id = parts[0]
            livre_titre = parts[1]

            # Récupérer l'adhérent et le livre
            adherent = adherents_dict.get(adherent_id)
            livre = livres_dict.get(livre_titre)

            if adherent and livre:
                # Parser les dates
                date_emp_parts = parts[2].split('-')
                date_emprunt = date(int(date_emp_parts[0]),
                                    int(date_emp_parts[1]),
                                    int(date_emp_parts[2]))

                date_retour = None
                if parts[3] != "None":
                    date_ret_parts = parts[3].split('-')
                    date_retour = date(int(date_ret_parts[0]),
                                       int(date_ret_parts[1]),
                                       int(date_ret_parts[2]))

                return Emprunt(adherent, livre, date_emprunt, date_retour)

        return None

    def __str__(self):
        retour_info = f"retourné le {self._date_retour.strftime('%d/%m/%Y')}" if self._date_retour else "en cours"
        retard_info = f" (RETARD: {self.jours_retard()} jours)" if self.est_en_retard() else ""

        return (f"Emprunt: {self._livre.titre} par {self._adherent.prenom} {self._adherent.nom} "
                f"(emprunté le {self._date_emprunt.strftime('%d/%m/%Y')}, {retour_info}){retard_info}")