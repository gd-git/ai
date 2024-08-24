Table des matières
* Introduction
* Arguments de la ligne de commande
* Fonctionnalités
* Configuration
* Utilisation
* Exemples

Introduction
Le programme ai est un outil de conversation avec un assistant intelligent. Il utilise un modèle de langage pour générer des réponses à des questions ou des demandes.

Arguments de la ligne de commande
Le programme ai accepte les arguments suivants :
* -c ou --conversation : spécifie un fichier de conversation pour reprendre une discussion
* -f ou --file : spécifie un ou plusieurs fichiers à charger
* -h ou --help : affiche l'aide et quitte
* -l ou --length_history : spécifie la longueur de l'historique
* -m ou --model : spécifie le modèle de langage à utiliser
* -o ou --option : spécifie une ou plusieurs options de configuration
* -p ou --provider : spécifie le fournisseur de modèle de langage
* -q ou --question : spécifie une question à poser et quitte
* -r ou --system-file : spécifie un ou plusieurs fichiers de configuration du système
* -s ou --system : spécifie le type de système
* -t ou --temperature : spécifie la température pour le modèle de langage
* -v ou --verbose : active le mode verbose
* -x ou --multi-lines : active le mode multi-lignes pour les questions
* -z ou --compress : active la compression des réponses

Fonctionnalités
Le programme ai offre les fonctionnalités suivantes :
* conversation avec un assistant intelligent
* chargement de fichiers de configuration et de données
* personnalisation du modèle de langage et du fournisseur
* affichage de l'historique des conversations
* possibilité de poser des questions et d'obtenir des réponses

Configuration
Le programme ai utilise un fichier de configuration pour stocker les paramètres. Le fichier de configuration est généré automatiquement si il n'existe pas.

Les options de configuration sont les suivantes :
* system : spécifie le type de système
* model : spécifie le modèle de langage
* provider : spécifie le fournisseur de modèle de langage
* temperature : spécifie la température pour le modèle de langage
* length_history : spécifie la longueur de l'historique
* verbose : active le mode verbose
* multi_lines : active le mode multi-lignes pour les questions
* compress : active la compression des réponses

Utilisation
Pour utiliser le programme ai, il suffit de l'exécuter avec les arguments souhaités. Par exemple :
* ai -q "Bonjour, comment allez-vous ?" pour poser une question et obtenir une réponse
* ai -f fichier.txt pour charger un fichier de données
* ai -c conversation.txt pour reprendre une conversation

Exemples
Voici quelques exemples d'utilisation du programme ai :
* ai -q "Quel est le sens de la vie ?"
* ai -f fichier.txt -m mon_modele
* ai -c conversation.txt -p mon_fournisseur
* ai -s mon_systeme -t 0.5 -v

