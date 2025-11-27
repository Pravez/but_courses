#import "../utils.typ"

= Utilisation de votre MCP par un LLM

== Consultation de la base de données

Votre MCP est maintenant disponible en libre accès sur le web, vous pouvez le brancher à n'importe quel outil IA qui supporte le protocole MCP. Vous pouvez l'utiliser avec :
- Vos IDEs IA (Cursor, Claude Code, Google Antigravity / Gemini CLI, Warp, Jetbrains/VSCode avec extensions etc.)
- Des outils en ligne (Claude, ChatGPT, Mistral)

Pour ce TP, il est recommandé d'utiliser l'outil Mistral directement sur LeChat (#link("https://chat.mistral.ai/")[https://chat.mistral.ai/]), car il est le seul à offrir cette fonctionnalité gratuitement et sans installation préalable (vous aurez tout de même besoin de vous créer un compte).

#utils.consigne[Connectez-vous sur Mistral LeChat, puis, dans la section "Intelligence" > "Connectors" > "+ Add Connector", sélectionnez "Custom MCP Connector". Donnez-lui un nom, configurez son URL avec la même que celle utilisée pour le MCP Inspector. Pas d'authentification. Fermez la boîte de dialogue, revenez sur l'interface conversationnelle, assurez-vous que le connector soit bien sélectionné. Demandez au LLM de vous donner le schéma de votre base de données.]

Vous pouvez donc faire tout ce que vous voulez sur votre base de données, directement via un LLM ! 

#figure(
  image("../images/llm_first_question.png", width: 60%),
  caption: [Configuration du connector MCP sur Mistral LeChat]
)

== Une question de sécurité

Maintenant que tout est configuré, c'est le moment de s'amuser avec le LLM.

#utils.question(num: 8)[Demandez au LLM de vous fournir la liste des classes, et de la formatter en JSON.]

Petit détail qui nous vient à l'idée : sauf erreur, nous avons branché le MCP sur notre utilisateur administrateur ! Cela veut donc dire que le LLM a absolument tous les droits. C'est pas le moment de faire des bêtises !

#utils.question(num: 9)[Tentez de vous ajouter par le LLM en tant que nouvel(le) étudiant(e) dans la base de données. Montrez la requête SQL écrite par le LLM (dans le document de réponses au TP), et exécutez-la. Via votre outil de management de base de données, vérifiez que vous avez bien été ajouté(e).]

Vous vous en doutez : c'est très clairement une faille de sécurité énorme. Il faut que le LLM n'ait qu'un accès en lecture seule à la base de données. Vous avez cependant toujours besoin de votre accès administrateur.

#utils.consigne[Avec Terraform, Créez un nouvel utilisateur en base de données, et accordez-lui uniquement les droits nécessaires pour lire la base de données. Puis, ajustez les variables d'environnement de votre conteneur (pour qu'il utilise ce nouvel utilisateur), et relancez-le grâce au `terraform apply`. Tentez à nouveau de créer une nouvelle entrée dans la base de données avec le LLM, dans n'importe quel table, et assurez-vous que cela ne fonctionne plus. Si vous avez détruit toute la base, appelez votre enseignant en essayant de trouver une excuse (bonne chance).]

Le requêtage de la base est maintenant sécurisé. Cependant, si pour une raison quelconque votre environnement Scaleway est compromis, l'accès à la base de données apparaît maintenant en clair (dans les variables d'environnement du conteneur). C'est ici aussi une faille de sécurité non négligeable. Il vous faut donc obfusquer la `connection_string` sur Scaleway, tout en vous permettant de la lire d'une manière sécurisée. Vous pouvez pour cela utiliser un _Secret Manager_ (espace de stockage sécurisé).

#utils.consigne[Si vous ne l'avez pas encore fait, avec la #link("https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password")[ressource `random_password`], générez un mot de passe sécurisé pour votre utilisateur en lecture seule. Puis, ajustez votre code Terraform pour utiliser ce mot de passe plutôt que de le générer vous-même.]

#utils.consigne[Faites de la `connection_string` un secret Scaleway via Terraform. Pour cela, créez un fichier `secrets.tf` et ajoutez-y la configuration nécessaire (ressources #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/secret")[`scaleway_secret`] et #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/secret_version")[`scaleway_secret_version`]). Enfin, ajustez le code Terraform de votre conteneur pour ne plus utiliser les variables d'environnement en clair (voir attribut `secret_environment_variables`).]

#utils.question(num: 10)[Quel est l'identifiant Scaleway du secret contenant la `connection_string` ?]

Terraform a cependant ses limites : il stocke en clair toutes les données qu'il utilise, et notamment les secrets. C'est un problème difficile à éviter, et c'est souvent pour cela que l'on utilise des espaces de stockage du `state` sécurisés (S3, PostgreSQL).

#utils.question(num: 11)[Quel est le mot de passe de l'utilisateur en lecture seule ? Allez chercher celui-ci dans le fichier `terraform.tfstate`. Indiquez son chemin en norme #link("https://jsonpath.com/")[JSONPath].]


#pagebreak()