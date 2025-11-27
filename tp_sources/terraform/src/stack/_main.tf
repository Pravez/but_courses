terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
}

provider "scaleway" {
  zone            = "fr-par-1"
  region          = "fr-par"
  access_key      = var.configuration.access_key
  secret_key      = var.configuration.secret_key
  organization_id = var.configuration.organization_id
  project_id      = var.configuration.project_id
}

data "scaleway_account_project" "project" {
  project_id = var.configuration.project_id
}

locals {
  resources_prefix = "[YOUR_USERNAME]-tp"
}