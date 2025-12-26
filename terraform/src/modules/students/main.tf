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

  group_id = var.group_id
  user_id  = each.value.id
}
