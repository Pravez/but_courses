resource "scaleway_container_namespace" "namespace" {
  project_id = scaleway_account_project.project_2025.id
  name       = "${local.resources_prefix}-students-namespace"
}
