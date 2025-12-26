# module "students" {
#   source            = "../modules/students"
#   file              = "${path.module}/students/test.csv"
#   project_id        = scaleway_account_project.project_2025.id
#   global_project_id = data.scaleway_account_project.global.id
#   year              = terraform.workspace
# }

resource "scaleway_iam_group" "students_2025" {
  name = "2025_students"

  lifecycle {
    ignore_changes = [user_ids]
  }
}

resource "scaleway_iam_policy" "students_2025" {
  name = "students_2025"
  rule {
    project_ids          = [scaleway_account_project.project_2025.id]
    permission_set_names = ["AllProductsReadOnly", "ContainersFullAccess", "FunctionsFullAccess", "ObjectStorageFullAccess", "ObjectStorageBucketPolicyFullAccess", "SecretManagerSecretAccess", "SecretManagerSecretCreate", "SecretManagerSecretWrite", "SecretManagerSecretDelete", "RelationalDatabasesFullAccess", "ContainerRegistryFullAccess"]
  }

  rule {
    project_ids          = [data.scaleway_account_project.global.id]
    permission_set_names = ["ObjectStorageReadOnly"]
  }

  group_id = scaleway_iam_group.students_2025.id
}

module "students_s5a" {
  source            = "../modules/students"
  file              = "${path.module}/students/2025_s5a.csv"
  project_id        = scaleway_account_project.project_2025.id
  global_project_id = data.scaleway_account_project.global.id
  year              = terraform.workspace
  group_id          = scaleway_iam_group.students_2025.id
}

module "students_s5c" {
  source            = "../modules/students"
  file              = "${path.module}/students/2025_s5c.csv"
  project_id        = scaleway_account_project.project_2025.id
  global_project_id = data.scaleway_account_project.global.id
  year              = terraform.workspace
  group_id          = scaleway_iam_group.students_2025.id
}
