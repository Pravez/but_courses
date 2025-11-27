locals {
  database_url = "postgres://${scaleway_rdb_user.readonly.name}:${scaleway_rdb_user.readonly.password}@${data.scaleway_rdb_instance.instance.endpoint_ip}:${data.scaleway_rdb_instance.instance.endpoint_port}/${data.scaleway_rdb_database.db.name}"
}

data "scaleway_container_namespace" "namespace" {
  project_id   = data.scaleway_account_project.project.project_id
  namespace_id = data.terraform_remote_state.global.outputs.container_namespace_id
}

data "scaleway_registry_image" "image" {
  name         = "pbreton"
  namespace_id = data.scaleway_container_namespace.namespace.registry_namespace_id
}

resource "scaleway_container" "mcp" {
  name           = "${local.resources_prefix}-mcp"
  namespace_id   = data.scaleway_container_namespace.namespace.id
  registry_image = "${data.scaleway_container_namespace.namespace.registry_endpoint}/${data.scaleway_registry_image.image.name}:latest"
  port           = 8000
  cpu_limit      = 100
  memory_limit   = 256
  min_scale      = 1
  max_scale      = 1

  secret_environment_variables = {
    DATABASE_URL = local.database_url
  }
}
