resource "random_password" "password" {
  length      = 32
  special     = true
  upper       = true
  lower       = true
  numeric     = true
  min_upper   = 1
  min_lower   = 1
  min_numeric = 1
  min_special = 1
  # Exclude characters that might cause issues in some contexts
  override_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
}

resource "scaleway_rdb_instance" "instance" {
  project_id = scaleway_account_project.project_2025.id

  node_type          = "DB-DEV-S"
  engine             = "PostgreSQL-17"
  name               = "${local.resources_prefix}-db"
  is_ha_cluster      = false
  user_name          = "admin"
  password           = random_password.password.result
  encryption_at_rest = false
  disable_backup     = true
}

resource "scaleway_rdb_database" "db" {
  name        = "but_classes"
  instance_id = scaleway_rdb_instance.instance.id
}

resource "scaleway_secret" "database_secret" {
  project_id = scaleway_account_project.project_2025.id

  name = "${local.resources_prefix}-db-admin-password"
}

resource "scaleway_secret_version" "database_secret_version" {
  secret_id = scaleway_secret.database_secret.id
  data      = random_password.password.result
}

resource "scaleway_rdb_privilege" "privilege" {
  instance_id   = scaleway_rdb_instance.instance.id
  user_name     = scaleway_rdb_instance.instance.user_name
  database_name = scaleway_rdb_database.db.name
  permission    = "all"
}
