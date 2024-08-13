# IA : Un assistant conversationnel
=====================================

## Table des matières
--------------------

[Introduction](#introduction)
[Fonctionnalités](#fonctionnalités)
[Commandes](#commandes)
[Options de ligne de commande](#options-de-ligne-de-commande)
[Fichier de configuration](#fichier-de-configuration)
[Environnement](#environnement)
[Dépendances](#dépendances)
[Licence](#licence)

## Introduction
---------------

IA est un programme qui permet de créer un assistant conversationnel capable de répondre à des questions et de discuter avec un utilisateur. Le programme utilise des modèles de langues pour générer des réponses cohérentes et pertinentes.

### Fonctionnement de l'application

L'application fonctionne de la manière suivante :

L'utilisateur saisit une question ou une phrase dans la console.
L'application utilise un modèle de langue pour générer une réponse à la question ou à la phrase saisie par l'utilisateur.
La réponse est ensuite affichée dans la console.

### Fonctionnalités de l'application

L'application dispose des fonctionnalités suivantes :

*   **Dialogue avec l'utilisateur** : L'application permet de créer un dialogue avec l'utilisateur en utilisant des modèles de langues pour générer des réponses.
*   **Gestion de la conversation** : L'application permet de gérer la conversation enregistrée avec l'utilisateur, y compris la possibilité de sauvegarder et de recharger la conversation.
*   **Personnalisation** : L'application permet de personnaliser le comportement de l'assistant en utilisant des paramètres tels que la température, le modèle de langue, etc.

## Commandes
-------------

### $help

Affiche l'aide pour les commandes disponibles.

### $history

Affiche l'historique de la conversation.

### $config

Permet de configurer les paramètres de l'assistant.

### $model

Permet de sélectionner le modèle de langue à utiliser.

### $write

Permet de sauvegarder la conversation et de mettre à jour le contenu du programme.

### $undo

Permet de récupérer la sauvegarde du programme.

### $print

Affiche les lignes du programme sans les numéroter.

### $test

Exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND.

## Options de ligne de commande
---------------------------------

### -c, --conversation

Spécifie le fichier de conversation à utiliser.

### -d, --document

Spécifie les documents à charger.

### -g, --seed

Spécifie la graine à utiliser pour le modèle de langue.

### -h, --help

Affiche l'aide pour les options de ligne de commande.

### -l, --length_history

Spécifie la longueur de l'historique de la conversation.

### -m, --model

Spécifie le modèle de langue à utiliser.

### -p, --program

Spécifie le programme à charger.

### -q, --question

Spécifie la question à poser à l'assistant.

### -s, --system

Spécifie le type d'assistant à utiliser.

### -t, --temperature

Spécifie la température à utiliser pour le modèle de langue.

### -v, --verbose

Affiche des informations supplémentaires.

### -x, --multi-lines

Permet de saisir des questions sur plusieurs lignes.

## Fichier de configuration
-----------------------------

L'application utilise un fichier de configuration pour stocker les paramètres de l'assistant. Le fichier de configuration par défaut est `~/.iarc`.

## Environnement
-----------------

L'application utilise des variables d'environnement pour stocker des informations sur l'exécution de l'application. Les variables d'environnement suivantes sont utilisées :

### AI_TEST_COMMAND

Variable d'environnement qui spécifie la commande à exécuter pour le test.

## Dépendances
----------------

L'application utilise des bibliothèques externes pour fonctionner. Les bibliothèques suivantes sont utilisées :

### groq

Bibliothèque pour l'accès aux modèles de langues.

### requests

Bibliothèque pour les requêtes HTTP.

## Licence
------------

L'application est distribuée sous la licence GPLv3.
