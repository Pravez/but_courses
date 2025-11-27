#import "../utils.typ"

= Introduction

L'objectif de ce TP est de vous permettre d'expérimenter dans le Cloud les principaux composants que vous allez
être amené à utiliser dans votre vie professionnelle. Ces outils ne sont bien souvent rien de plus que les outils
que vous connaissez déjà (Docker, Kubernetes, Bases de données, serveurs web, ...), mais portés à une échelle nettement
plus grande et un "packaging" plus adapté pour les développeurs et leurs usages.

Vous allez donc pratiquer du Docker/Dockerfile et du Terraform pour déployer dans le Cloud un MCP (Model Context Protocol), permettant à un LLM de réaliser des tâches de manière autonome.

#utils.encart(title: "Usage des LLMs", type: "warning")[Ce TP a pour objectif de vous faire travailler tout un ensemble d'outils et de méthodes. Utiliser un LLM pour faire le travail à votre place est sans aucun doute une mauvaise idée : les documentations Terraform bougent beaucoup, ne sont pas très standard, et favorisent l'hallucination de ces outils (en plus de d'agacer votre correcteur).]

Ce TP est *noté*. Le rendu doit être une *archive zip* contenant :
- Le code source de votre Terraform
- Un document de réponses à toutes les questions posées dans le TP (blocs de couleur orange)

Un template de réponses vous est fourni (`ANSWERS.md`), à remplir. N'oubliez pas de préciser votre nom, prénom et nom d'utilisateur dans le fichier (nom d'utilisateur = première lettre prénom + nom, par exemple `pbreton` pour `Paul Breton`, uniquement des lettres minuscules). Vous avez parfaitement le droit d'ajouter des images ou des captures d'écran dans votre document de réponses pour illustrer vos réponses.

Le nom de l'archive doit être au format `tp_cloud_2025_<nom_utilisateur>.zip`.

Attention à ne pas inclure de fichiers inutiles dans votre archive (logs, binaires, répertoires temporaires, etc.). Notamment le répertoire temporaire Terraform et les éventuels résultats temporaires de compilation Rust. Vous pouvez utiliser la commande suivante depuis votre terminal pour créer l'archive :

```bash
zip -r tp_cloud_2025_<nom_utilisateur>.zip [répertoire]/ -x "*/.terraform/*" "*/target/*"
```
#pagebreak()