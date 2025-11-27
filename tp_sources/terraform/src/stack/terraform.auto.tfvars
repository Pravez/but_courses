configuration = {
  access_key      = "[YOUR_ACCESS_KEY]"
  secret_key      = "[YOUR_SECRET_KEY]"
  organization_id = "fd75f101-5f73-4d50-a582-8e24b6852972"
  project_id      = "b939fdd8-c43d-415c-a09b-1ee2144e72de"
}

remote_state = {
  bucket   = "but-tp-terraform-states"
  key      = "terraform.tfstate"
  region   = "fr-par"
  endpoint = "https://s3.fr-par.scw.cloud"
}
