terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
}

locals {
  students = { for v in csvdecode(file(var.file)) : v["mail"] => v }
}

resource "scaleway_iam_group" "students" {
  name = "${var.year}_students"

  lifecycle {
    ignore_changes = [user_ids]
  }
}

resource "random_password" "password" {
  length = 24
}

resource "scaleway_iam_user" "students" {
  for_each            = local.students
  email               = each.key
  username            = each.value.username
  first_name          = each.value.first_name
  last_name           = each.value.last_name
  password            = random_password.password.result
  send_password_email = true
}

resource "scaleway_iam_group_membership" "students" {
  for_each = scaleway_iam_user.students

  group_id = scaleway_iam_group.students.id
  user_id  = each.value.id
}

resource "scaleway_iam_policy" "students" {
  name = "students_${var.year}"
  rule {
    project_ids          = [var.project_id]
    permission_set_names = ["AllProductsReadOnly", "ContainersFullAccess", "FunctionsFullAccess", "ObjectStorageFullAccess", "ObjectStorageBucketPolicyFullAccess", "SecretManagerSecretAccess", "SecretManagerSecretCreate", "SecretManagerSecretWrite", "RelationalDatabasesFullAccess", "ContainerRegistryFullAccess"]
  }

  rule {
    project_ids          = [var.global_project_id]
    permission_set_names = ["ObjectStorageReadOnly"]
  }

  group_id = scaleway_iam_group.students.id
}
