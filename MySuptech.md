# CAHIER DES CHARGES - PROJET "MYSUPTECH"
**Version :** 1.0  
**Client :** Groupe ISI SUPTECH  
**Type :** Application Web de Gestion Pédagogique  

---

## 1. PRÉSENTATION DU PROJET

**MySuptech** est une plateforme web centralisée destinée à la gestion de la vie scolaire et au suivi pédagogique au sein de l'établissement **ISI SUPTECH**. 

Elle vise à remplacer les supports papiers (cahiers de textes, feuilles d'appel) par une solution numérique accessible sur ordinateur et smartphone, facilitant la communication entre l'administration (Directeur/Surveillants) et le corps professoral.

---

## 2. OBJECTIFS PRINCIPAUX

1.  **Fiabiliser le suivi pédagogique :** Assurer la continuité des cours grâce à un historique numérique et des rappels intelligents pour les professeurs.
2.  **Contrôler l'assiduité :** Suivre en temps réel la présence des étudiants et la tenue effective des cours par les professeurs.
3.  **Centraliser la planification :** Offrir un emploi du temps unique, clair et géré par l'administration.

---

## 3. LES ACTEURS (RÔLES)

### 3.1. L'Administrateur (Directeur des Études / Surveillant)
*   Dispose des droits complets sur la plateforme.
*   Gère les données de base (utilisateurs, classes, plannings).
*   Supervise le déroulement des cours en temps réel.

### 3.2. Le Professeur
*   Utilisateur final (principalement sur mobile en classe).
*   Consulte son emploi du temps.
*   Valide sa présence, fait l'appel des étudiants et remplit le cahier de texte.

---

## 4. FONCTIONNALITÉS DÉTAILLÉES

### 4.1. Module Administration (Back-Office)

*   **Gestion des Utilisateurs :**
    *   Création/Modification/Suppression des comptes Professeurs (Nom, Prénom, Matières, Login).
    *   Importation des listes d'Étudiants par classe.
*   **Gestion de la Structure :**
    *   Création des Classes (ex: Licence 1 GL, Master 2 Réseaux).
    *   Création des Matières.
*   **Gestion du Planning (Emploi du temps) :**
    *   Attribution des créneaux : *Jour + Heure + Classe + Matière + Professeur + Salle*.
*   **Tableau de Bord "LIVE" (Temps Réel) :**
    *   Vue d'ensemble des cours en cours.
    *   Indicateurs visuels :
        *   🟢 Vert : Cours démarré / Professeur présent.
        *   🔴 Rouge : Retard / Cours non démarré après 15 min.
        *   ⚪ Gris : Aucun cours prévu.
*   **Statistiques :**
    *   Suivi des absences par étudiant (Total d'heures).
    *   Historique des cahiers de texte (Vérification de l'avancement du programme).

### 4.2. Module Professeur (Front-Office Mobile)

*   **Tableau de Bord Personnel :**
    *   Vue "Timeline" de la journée (Chronologie des cours).
    *   Distinction claire des matières (si le prof en enseigne plusieurs).
*   **Action : Démarrer le Cours :**
    *   Bouton de validation de présence (horodatage du début de cours).
*   **Action : Faire l'Appel :**
    *   Liste des étudiants de la classe pré-cochés "Présents".
    *   Système de cases à cocher pour marquer les "Absents".
    *   **Visualisation du taux d'absence :** Affichage du compteur d'absences cumulées à côté du nom de chaque étudiant.
*   **Le "Rappel Intelligent" (Fonctionnalité Clé) :**
    *   Avant/Au début du cours, affichage automatique d'une alerte : *"Lors du dernier cours de [Matière] avec la [Classe], vous vous êtes arrêté à : [Point d'arrêt précédent]"*.
*   **Cahier de Texte Numérique :**
    *   Formulaire à remplir en fin de séance :
        *   *Résumé de la séance.*
        *   *Devoirs donnés.*
        *   *Point d'arrêt précis (Chapitre, Page, Exercice).*

---

## 5. SPÉCIFICATIONS TECHNIQUES

### 5.1. Architecture
*   **Type :** Application Web (Site Internet) Responsive.
*   **Approche :** Mobile-First (Design pensé prioritairement pour l'écran du smartphone du professeur).

### 5.2. Stack Technologique (Recommandée)
*   **Langage Backend :** Python.
*   **Framework Web :** **Flask**.
    *   Choisi pour sa légèreté, sa flexibilité et sa rapidité de mise en place.
*   **Base de Données :**
    *   ORM : **SQLAlchemy**.
    *   SGBD Dev : SQLite.
    *   SGBD Prod : PostgreSQL.
*   **Frontend :**
    *   Moteur de template : **Jinja2** (intégré à Flask).
    *   Framework CSS : **Bootstrap 5** (pour la grille responsive et les composants UI).
    *   Interactivité : JavaScript Vanilla ou HTMX (pour l'appel sans rechargement de page).

### 5.3. Modèle de Données (Structure BDD Simplifiée)

1.  **Table `USERS` :** ID, Nom, Email, Password, Role (Admin/Prof).
2.  **Table `CLASSES` :** ID, Nom (ex: L1 GL).
3.  **Table `MATIERES` :** ID, Nom (ex: Java, Algèbre).
4.  **Table `ETUDIANTS` :** ID, Nom, Prénom, ID_Classe.
5.  **Table `PLANNING` (Créneaux Théoriques) :** ID, Jour, Heure_Debut, Heure_Fin, ID_Classe, ID_Matiere, ID_Prof.
6.  **Table `SESSIONS` (Cahier de Texte & Historique) :** ID, Date, ID_Planning, Contenu, Devoirs, Point_Arret, Statut (En cours/Terminé).
7.  **Table `PRESENCES` :** ID, ID_Session, ID_Etudiant, Statut (Present/Absent).

---

## 6. ERGONOMIE ET CHARTE GRAPHIQUE

*   **Identité Visuelle :** Couleurs sobres et professionnelles (ex: Bleu Marine ISI, Blanc, Gris clair).
*   **Navigation Mobile :**
    *   Barre de navigation fixée en bas pour les Professeurs (Accueil, Agenda, Profil).
    *   Menu latéral (Sidebar) pour l'Admin sur ordinateur.
*   **Expérience Utilisateur (UX) :**
    *   Nombre de clics minimum pour faire l'appel.
    *   Feedback visuel immédiat (Message de succès lors de l'enregistrement).

---

## 7. LIVRABLES ATTENDUS

1.  Code source complet (Projet Flask).
2.  Script d'installation de la base de données.
3.  Compte "Super Admin" pré-configuré.
4.  Documentation utilisateur simplifiée (PDF).