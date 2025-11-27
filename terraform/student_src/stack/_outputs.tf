output "database" {
  value = {
    host = data.scaleway_rdb_instance.instance.endpoint_ip
    port = data.scaleway_rdb_instance.instance.endpoint_port
    database = data.terraform_remote_state.global.outputs.rdb_instance.database_name
  }
}

output "container_url" {
  value = "https://${scaleway_container.mcp.domain_name}/sse"
}