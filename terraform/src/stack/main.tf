terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
}

provider "scaleway" {
  zone   = "fr-par-1"
  region = "fr-par"
  access_key = "SCW50G329HJJS3PY9ZSD"
  secret_key = "359a7fba-bad7-4f1b-a666-20ebc7a233d2"
  organization_id = "fd75f101-5f73-4d50-a582-8e24b6852972"
  project_id = "fd75f101-5f73-4d50-a582-8e24b6852972"
}

resource "scaleway_account_project" "project_2025" {
  name = "2025"
}