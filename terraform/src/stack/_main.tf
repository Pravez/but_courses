terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }

  backend "s3" {
    bucket                      = "but-tp-terraform-states"
    key                         = "terraform.tfstate"
    region                      = "fr-par"
    endpoint                    = "https://s3.fr-par.scw.cloud"
    access_key                  = "SCW50G329HJJS3PY9ZSD"
    secret_key                  = "359a7fba-bad7-4f1b-a666-20ebc7a233d2"
    skip_credentials_validation = true
    force_path_style            = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
  }
}

provider "scaleway" {
  zone            = "fr-par-1"
  region          = "fr-par"
  access_key      = "SCW50G329HJJS3PY9ZSD"
  secret_key      = "359a7fba-bad7-4f1b-a666-20ebc7a233d2"
  organization_id = "fd75f101-5f73-4d50-a582-8e24b6852972"
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
