# Table des matières

* [Commandes](#commandes)
* [Config](#config)
* [Help](#help)
* [History](#history)
* [Model](#model)
* [Print](#print)
* [Test](#test)
* [Undo](#undo)
* [Write](#write)
* [Toggle](#toggle)
* [Rc](#rc)
* [Conversation](#conversation)

# Commandes

## $config

### Description

La commande `$config` permet de gérer la configuration de l'assistant.

### Sous-commandes

* `$config` : affiche la configuration actuelle
* `$config write` : sauvegarde la configuration actuelle
* `$config <clé>` : affiche la valeur de la clé de configuration spécifiée
* `$config <clé> <valeur>` : modifie la valeur de la clé de configuration spécifiée

## $help

### Description

La commande `$help` affiche l'aide de l'assistant.

## $history

### Description

La commande `$history` affiche l'historique des conversations avec l'assistant.

## $model

### Description

La commande `$model` permet de gérer les modèles de langage utilisés par l'assistant.

### Sous-commandes

* `$model` : affiche le modèle de langage actuel
* `$model list` : affiche la liste des modèles de langage disponibles

## $print

### Description

La commande `$print` affiche les lignes du programme sans les numéroter.

## $test

### Description

La commande `$test` exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND.

## $undo

### Description

La commande `$undo` récupère la sauvegarde du programme.

## $write

### Description

La commande `$write` enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée) et met à jour le contenu du programme avec la réponse de l'assistant.

## $toggle

### Description

La commande `$toggle` permet de basculer entre le mode mono-ligne et le mode multi-lignes.

## $rc

### Description

La commande `$rc` permet de gérer les fichiers de configuration.

### Sous-commandes

* `$rc save` : sauvegarde la configuration actuelle
* `$rc load` : charge la configuration à partir d'un fichier

## $conversation

### Description

La commande `$conversation` permet de gérer les conversations avec l'assistant.

### Sous-commandes

* `$conversation save <fichier>` : sauvegarde la conversation dans un fichier