# Retours TP 2025

## A corriger

- Question 2 : le terraform init est ok. A corriger en demandant de faire un terraform init puis un terraform plan.
- Question 6 : les logs ne s'affichent pas, ou souvent mal.
- Les étudiants se mélangent entre sudo docker et docker
- Pour le mot de passe dans la base de données (questions 8-9), utiliser la fonction base64decode() puisque le secret est en réalité un data encodé.
- déplacer le fait de couper/redémarrer le tf apply pour les containers (l'encart bleu) plus haut pour mieux aider les élèves
- ils se trompent constamment de nom d'image à déployer, leur rappeler de bien la nommer <registry>/<image>:<tag>


=> voir pour les deux élèves pour lesquels la configuration ne donne absolument pas lieu à un démarrage des images