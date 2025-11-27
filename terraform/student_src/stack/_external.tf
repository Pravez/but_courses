data "terraform_remote_state" "global" {
  backend = "s3"
  workspace = "2025"
  config = {
    bucket     = var.remote_state.bucket
    key        = var.remote_state.key
    region     = var.remote_state.region
    endpoint   = var.remote_state.endpoint
    access_key = var.configuration.access_key
    secret_key = var.configuration.secret_key
    skip_credentials_validation = true
    force_path_style            = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
  }
}
