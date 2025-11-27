data "scaleway_rdb_instance" "instance" {
  instance_id = data.terraform_remote_state.global.outputs.rdb_instance.id
}

data "scaleway_rdb_database" "db" {
  name        = data.terraform_remote_state.global.outputs.rdb_instance.database_name
  instance_id = data.scaleway_rdb_instance.instance.id
}

resource "scaleway_rdb_user" "user" {
  instance_id = data.scaleway_rdb_instance.instance.id
  name        = "pbreton"
  password    = "Testtest123!"
  is_admin    = true
}

resource "scaleway_rdb_privilege" "privilege" {
  instance_id   = data.scaleway_rdb_instance.instance.id
  database_name = data.scaleway_rdb_database.db.name
  user_name     = scaleway_rdb_user.user.name
  permission    = "all"
}

resource "random_password" "password" {
  length           = 16
  special          = true
  upper            = true
  min_lower        = 1
  min_special      = 1
  min_upper        = 1
  override_special = "_%@"
}

resource "scaleway_rdb_user" "readonly" {
  instance_id = data.scaleway_rdb_instance.instance.id
  name        = "readonly"
  password    = random_password.password.result
}

resource "scaleway_rdb_privilege" "readonly_privilege" {
  instance_id   = data.scaleway_rdb_instance.instance.id
  database_name = data.scaleway_rdb_database.db.name
  user_name     = scaleway_rdb_user.readonly.name
  permission    = "readonly"
}
