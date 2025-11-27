#import "../utils.typ"

= Déploiement de votre MCP

Votre MCP est un code Rust qui utilise la bibliothèque officielle Rust #link("https://github.com/modelcontextprotocol/rust-sdk")[`rmcp`] pour communiquer avec un LLM. Un MCP peut faire beaucoup de choses grâce à ses `tools`. Dans le cadre de ce TP, votre MCP expose surtout des `tools` pour récupérer un schéma de base de données, et exécuter des requêtes SQL dans celle-ci.

== Déploiement de votre image Docker

L'application MCP est déjà dockerisée, il ne vous reste qu'à la déployer dans votre registry Scaleway. Première étape, déployer votre image dans votre registry Scaleway. Rendez-vous en ligne sur la console Scaleway pour trouver votre `Container Registry` (qui devrait démarrer par _funcscw..._). Sur celui-ci, vous trouverez suffisamment d'informations pour vous authentifier et déployer votre image. Une fois ces informations trouvées, rendez-vous donc dans le dossier `project`, qui contient le code source de votre MCP et son `Dockerfile`.

#utils.consigne[A l'aide de la commande `docker login` et `docker build`, déployez votre image dans votre registry Scaleway. N'oubliez pas de tagger votre image suivant votre registry, et de lui donner un nom qui vous est propre (par exemple, en rajoutant votre nom/prénom dans l'image : encore une fois vous partagez ce registry avec tous les autres étudiants).]

Rust est un langage compilé, entre autres intéressant pour ses performances et sa sécurité. Un de ses défauts cependant réside dans ses dépendances de compilation, qui peuvent vite s'avérer être lourdes (en termes de stockage). Le `Container Registry` vous est facturé au temps mais aussi au stockage, il est donc important de réduire au maximum la taille de vos images.

#utils.consigne[Grâce au #link("https://docs.docker.com/build/building/multi-stage/")[Docker multi-stage], réduisez la taille de votre image Docker (indice: vous n'avez logiquement besoin que de votre exécutable pour faire fonctionner votre MCP). Pour trouver la taille d'une image (en bytes), utilisez la commande `docker image inspect <image_name> | grep Size`.]
#utils.question(num: 4)[Comment fonctionne le multi-stage ? De combien de Mégaoctets avez-vous réussi à réduire la taille de votre image ?]

Votre image est maintenant déployée dans votre registry Scaleway. Vous pouvez désormais la récupérer et l'utiliser dans vos conteneurs Scaleway !

== Déploiement de votre conteneur Scaleway

Il est temps maintenant de déployer votre conteneur via Terraform. En allant regarder la #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/container")[documentation Terraform des Serverless Containers], vous pourrez constater toute la configuration nécessaire pour déployer un conteneur.

#utils.consigne[Notez bien les informations dont vous allez avoir besoin :
- Les besoins en ressources (CPU, RAM)
- Le scaling
Rendez-vous sur l'interface Scaleway pour créer "à blanc" un conteneur : allez dans la partie "Serverless Containers", sélectionnez votre _Namespace_, plus "+ Deploy a container". Faites ainsi une simulation de configuration pour estimer les ressources nécessaires.
]

#utils.question(num: 5)[En prenant en compte l'extrême efficacité CPU et RAM de Rust, quelles sont les ressources nécessaires pour faire tourner votre MCP ? Quel est le coût mensuel associé pour une disponibilité sans interruptions ?]

À vos IDEs maintenant ! Dans votre répertoire Terraform, à côté du fichier `_main.tf`, créez un fichier `containers.tf` et ajoutez-y la configuration nécessaire pour déployer votre conteneur. Parcourez le code Rust pour vous aider à trouver toutes les informations nécessaires pour le port de votre MCP.

#utils.encart(title: "Terraform Remote State", type: "info")[Votre enseignant a lui-même utilisé Terraform pour provisionner l'ensemble de l'infrastructure sur Scaleway (utilisateurs, registry Docker, namespaces, etc.). Comme vous allez partager des ressources, vous allez devoir utiliser le `remote state` de Terraform pour récupérer les informations nécessaires à la configuration de votre conteneur. L'idée est simplement que votre configuration Terraform accède au state d'une autre configuration pour récupérer ses `outputs`. Vous pourrez trouver la configuration de ce remote state dans le fichier `terraform/student_src/stack/_external.tf`. Voici le code des outputs du remote state de votre enseignant :
```terraform
output "rdb_instance" {
  value = {
    id            = scaleway_rdb_instance.instance.id
    name          = scaleway_rdb_instance.instance.name
    database_name = scaleway_rdb_database.db.name
  }
}

output "container_namespace_id" {
  value = scaleway_container_namespace.namespace.id
}
```
Pour accéder à l'une de ces valeurs, il vous suffit d'utiliser la syntaxe Terraform`
data.terraform_remote_state.global.outputs.<output_name>`.
]

Pour la suite du TP, lorsque vous créez des ressources Terraform sur Scaleway :
- *Préfixez vos ressources*, utilisez la variable locale `local.resources_prefix` pour préfixer le nom de vos ressources.
- *N'oubliez pas de préciser le `project_id`* dans les ressources qui le nécessitent, sinon elles seront créées dans le projet par défaut de votre compte Scaleway.
#utils.consigne[À l'aide du `remote state`, créez un `data` pour récupérer votre #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/data-sources/container_namespace")[container namespace]. Puis, créez un `data` pour récupérer votre #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/data-sources/registry_image")[registry image], celle que vous avez déployée dans votre registry Scaleway (via votre `container namespace` et son attribut `registry_namespace_id`). Ensuite, créez un `resource` pour déployer votre #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/container")[conteneur], en utilisant les valeurs récupérées précédemment. Attention à ne pas recopier toutes la configuration par défaut de la documentation ! (et précisez bien `min_scale = 1`).

Une fois le code écrit, il ne vous reste plus qu'à exécuter la commande `terraform apply`, visualiser les changements proposés par Terraform, et les valider. Si tout se passe bien, votre conteneur devrait être en cours de déploiement.

Allez regarder dans l'interface ! Dans la section Serverless Containers trouvez votre namespace, votre container, et constatez votre déploiement en cours.]

#utils.question(num: 6)[Utilisez les logs de votre conteneur (Onglet "Logs" > "Open Grafana logs dashboard") pour vérifier que votre MCP tourne. Pourquoi celui-ci ne démarre-t-il pas ? Citez le log Grafana qui vous a permis de le détecter.]

#pagebreak()