resource "scaleway_secret" "db_password" {
  project_id = data.scaleway_account_project.project.project_id
  name = "${local.resources_prefix}-db-password"
}

resource "scaleway_secret_version" "db_password_version" {
  secret_id = scaleway_secret.db_password.id
  data = local.database_url
}