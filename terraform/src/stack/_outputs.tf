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
