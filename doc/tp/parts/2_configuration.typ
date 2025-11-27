#import "../utils.typ"

= Configuration de votre environnement

== Outils

Pour ce TP, vous aurez besoin de :
- Un poste informatique fonctionnel (sans blague)
- Une installation Terraform (voir la #link("https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli")[documentation officielle])
- Un IDE ou éditeur de texte (#link("https://code.visualstudio.com/")[VSCode], #link("https://www.jetbrains.com/fr-fr/idea/")[Jetbrains], ...), avec l'extension Terraform (pour une meilleure expérience de développement, sinon c'est que vous êtes vraiment très déterminé).
- Un outil de requêtage de base de données (#link("https://www.pgadmin.org/")[pgAdmin], #link("https://dbeaver.io/")[DBeaver], #link("https://www.jetbrains.com/datagrip/")[DataGrip], ...)
- `npm` pour utiliser #link("https://github.com/modelcontextprotocol/inspector")[MCP Inspector] (documentation pour l'installation #link("https://docs.npmjs.com/downloading-and-installing-node-js-and-npm")[ici])

Il n'y a pas de prérequis spécifique pour les méthodes d'installation ni pour les outils, vous avez la liberté totale sur la manière de gérer votre environnement. Utilisez le ou les outils que vous souhaitez pour réaliser les tâches techniques qui vont suivre (excepté un LLM bien entendu). L'élément central reste Terraform sans quoi vous ne pourrez pas faire ce TP.

== Initialisation du projet Terraform

Une fois l'ensemble installé, il est temps d'initialiser votre projet Terraform. Téléchargez les sources du TP, puis rendez-vous dans le dossier `terraform/src/stack`.

#utils.consigne[Exécutez la commande `terraform init` pour initialiser votre projet.]

#utils.question(num: 1)[Que remarquez-vous ? Manque-t-il quelque chose ?]

Sur votre adresse mail étudiante, vous devriez avoir reçu un email de la part de Scaleway (`no-reply@scaleway.net`) avec vos informations d'identification. Authentifiez-vous sur la plateforme et conservez bien votre mot de passe.

Vous avez désormais accès à toute la plateforme Scaleway. Vous faites partie de l'organisation `Cloud Academy`, et avez deux projets en visibilité : 
- General : projet global qui va notamment contenir des ressources partagées entre toutes les années et vos utilisateurs IAM (_Identity & Access Management_)
- #utils.current_year : projet qui va contenir vos ressources spécifiques à votre année (base de données, namespace Docker, ...)
Vous avez les droits de lecture sur l'ensemble des ressources du projet #utils.current_year, et les droits d'écriture sur les ressources `Serverless Containers`, `ServerlessFunctions`, `Object Storage`, `Relational Databases`, `Secret Manager` et `Container Registry`. Sentez-vous libre de vous balader dans les différentes sections de la plateforme pour vous familiariser avec les différents services. Du fait de vos droits, vous pouvez créer à la main des services, tester les interfaces de création, etc. Ayez simplement à l'idée de ne pas casser les ressources des autres (vous partagez tous le même espace de travail), et de tout faire via le Terraform pour répondre aux questions de ce TP.

Pour démarrer la configuration, il va d'abord vous falloir créer un jeton d'accès à l'API Scaleway. Pour cela, rendez-vous dans la section "Management & Gouvernance" de votre compte Scaleway, "IAM", "API Keys" puis "+ Generate an API key".

#figure(
  image("../images/api_key_create.png", width: 110%),
  caption: [Création d'un jeton d'accès à l'API Scaleway]
)

La popup qui va suivre vous permettra d'obtenir votre `access_key` et votre `secret_key`.
#utils.consigne[Utilisez ces informations pour corriger l'initialisation de votre projet, et relancez la commande `terraform init`.]
#utils.question(num: 2)[Qu'a créé Terraform ? Où se situe votre `state` ? Comment faire si vous souhaitez coder à plusieurs ? (aidez-vous de la #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs")[documentation Terraform du provider Scaleway], partie "Guides")]
#utils.question(num: 3)[Expliquez la notion de *state locking* de Terraform et le lien avec la question précédente.]

#pagebreak()