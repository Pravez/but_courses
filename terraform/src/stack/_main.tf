terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  backend "s3" {
    key                         = "terraform.tfstate"
    region                      = "fr-par"
    endpoint                    = "https://s3.fr-par.scw.cloud"
    skip_credentials_validation = true
    force_path_style            = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
  }
}

provider "scaleway" {
  zone            = "fr-par-1"
  region          = "fr-par"
  access_key      = var.scaleway.access_key
  secret_key      = var.scaleway.secret_key
  organization_id = var.scaleway.organization_id
}

resource "scaleway_account_project" "project_2025" {
  name = terraform.workspace
}

data "scaleway_account_project" "global" {
  project_id = "fd75f101-5f73-4d50-a582-8e24b6852972"
}

locals {
  resources_prefix = "but-info-tp-${terraform.workspace}"
}
