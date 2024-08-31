Commandes
=========

Cette page présente les commandes disponibles dans le programme, commençant par `$`.

### Commandes

* `$config` : configure la variable de configuration
	+ `$config write` : sauvegarde la configuration actuelle
	+ `$config <clé>` : affiche la valeur de la clé de configuration spécifiée
	+ `$config <clé> <valeur>` : modifie la valeur de la clé de configuration spécifiée
* `$conversation` : sauvegarde ou charge une conversation
	+ `$conversation save <fichier>` : sauvegarde la conversation dans un fichier
	+ `$conversation load <fichier>` : charge une conversation à partir d'un fichier
* `$file` : gère la liste des fichiers
	+ `$file` : affiche la liste des fichiers
	+ `$file add <fichier>` : ajoute un fichier à la liste des fichiers
	+ `$file save` : enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
	+ `$file save <fichier>` : enregistre le programme/fichier spécifié
* `$git` : exécute une commande Git
* `$help` : affiche cette aide
* `$history` : affiche l'historique des conversations
	+ `$history purge` : purge l'historique des conversations
* `$model` : affiche les informations sur le modèle de langage utilisé
	+ `$model list` : affiche la liste des modèles de langage disponibles
	+ `$model <nom du modèle>` : sélectionne le modèle de langage spécifié
* `$print` : affiche les lignes du programme sans les numéroter
* `$rc` : sauvegarde ou charge la configuration
	+ `$rc save` : sauvegarde la configuration actuelle
	+ `$rc load` : charge la configuration sauvegardée
* `$system` : exécute une commande système
* `$test` : exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND
* `$toggle` : active ou désactive le mode multi-lignes
* `$undo` : récupère la sauvegarde du programme
* `$write` : enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée) et met à jour le contenu du programme avec la réponse de l'assistant


