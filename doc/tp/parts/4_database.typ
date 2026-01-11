 #import "../utils.typ"

= Provisionnement de votre base de données

Votre MCP est maintenant déployé, mais ne démarre pas correctement. En effet, il n'a pas accès à votre base de données. La base de données est déjà provisionnée via le Terraform partagé, il vous faut donc créer un accès pour votre utilisateur MCP.

== Création d'un utilisateur en base

Vous allez avoir besoin d'un fichier `terraform/src/stack/database.tf` regroupant ces opérations sur la base.

#utils.consigne[À l'aide du `remote state`, créez un `data` pour récupérer l'#link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/data-sources/rdb_instance")[instance de base de données]. Puis, créez une #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/rdb_user")[`resource` pour votre utilisateur] en base de données. Attention à faire en sorte que celui-ci ait un nommage unique, et soit un utilisateur administrateur.]

Vous avez votre utilisateur, et vous lui avez donné un mot de passe, parfait ! Si vous le désirez, vous pouvez vous connecter à la base de données et voir son contenu via votre outil de management de base de données (pgAdmin, DBeaver, DataGrip, ...). Cela dit, il vous manque l'URL ! Pour la visualiser, il vous suffit de créer un fichier `terraform/src/stack/_outputs.tf` et d'y ajouter un `output` comme suivant (à adapter à votre code) :

```terraform
output "database" {
  value = {
    host = data.scaleway_rdb_instance.instance.endpoint_ip
    port = data.scaleway_rdb_instance.instance.endpoint_port
    database = data.terraform_remote_state.global.outputs.rdb_instance.database_name
  }
}
```

Un `terraform apply`, et vos outputs s'affichent désormais en sortie.

#figure(
  image("../images/terraform_output.png", width: 80%),
  caption: [Sortie de Terraform avec les outputs]
)

#utils.question(num: 7)[Avec votre outil de management de base de données, connectez-vous à votre base de données et vérifiez que vous pouvez y accéder. Y arrivez-vous ? Tentez maintenant avec la base "postgres". Y arrivez-vous ? Pourquoi n'avez-vous pas les droits (petit coup d'oeil sur la #link("https://www.postgresql.org/docs/current/ddl-priv.html")[documentation PostgreSQL]) ?]

#utils.consigne[Ajoutez une ressource de type #link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/resources/rdb_privilege")[`rdb_privilege`] pour accorder les droits nécessaires à votre utilisateur pour accéder à la base de données, puis retentez de vous y connecter. N'hésitez pas à créer un `data` dédié à la base de données (#link("https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/data-sources/rdb_database")[`rdb_database`] dérivé de votre `remote_state`) pour exploiter plus d'informations que simplement le nom de celle-ci.]

== Forger votre _connection_string_

Votre MCP prend en variable d'environnement une _connection_string_ pour se connecter à la base de données. Celle-ci doit être formatée comme suit :

```
postgres://<username>:<password>@<host>:<port>/<database>
```

#utils.consigne[Dans un bloc #link("https://developer.hashicorp.com/terraform/language/block/locals")[`locals`], créez une variable `database_url` avec la valeur de votre _connection_string_. Faites en sorte que chaque composante de cette variable (username, password, ...) soit extraite depuis vos ressources Terraform (donc rien en dur). Puis, ajustez les variables d'environnement de votre conteneur via Terraform, et relancez votre conteneur grâce au `terraform apply`.]

Votre MCP est maintenant en mesure de se connecter à la base, et est 100% opérationnel ! Pour regarder les `tools` qu'il expose, vous pouvez utiliser l'outil dédié #link("https://github.com/modelcontextprotocol/inspector")[MCP Inspector]. Pour le lancer, rien de plus simple : ouvrez un terminal et lancez la commande (attention à avoir installé `npm` et `node`):
```bash
> npx @modelcontextprotocol/inspector
```
Tout comme pour la base de données, pour connaître l'URL de votre MCP, il vous faut ajouter un nouvel `output` dans votre fichier `terraform/src/stack/_outputs.tf` permettant d'exporter l'attribut `domain_name` de votre conteneur. L'URL de votre MCP est :
```
https://<domain_name>/sse
```

Vous pouvez ensuite ouvrir votre MCP Inspector et y entrer l'URL de votre MCP. Vous devriez voir les `tools` qu'il expose, et pouvoir les utiliser.

#figure(
  image("../images/mcp_inspector.png", width: 110%),
  caption: [MCP Inspector avec l'URL de votre MCP]
)

Par exemple, vous pouvez utiliser le `tool` `execute_query` pour exécuter une requête SQL dans votre base de données en direct.

#figure(
  image("../images/database_exec_query.png", width: 100%),
  caption: [Exécution d'une requête SQL dans votre base de données]
)

#pagebreak()