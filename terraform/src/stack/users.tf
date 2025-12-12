module "students" {
  source            = "../modules/students"
  file              = "${path.module}/students/test.csv"
  project_id        = scaleway_account_project.project_2025.id
  global_project_id = data.scaleway_account_project.global.id
  year              = terraform.workspace
}

# module "students_s5a" {
#   source            = "../modules/students"
#   file              = "${path.module}/students/2025_s5a.csv"
#   project_id        = scaleway_account_project.project_2025.id
#   global_project_id = data.scaleway_account_project.global.id
#   year              = terraform.workspace
# }
