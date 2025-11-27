variable "configuration" {
  type = object({
    access_key = string
    secret_key = string
    organization_id = string
    project_id = string
  })
}

variable "remote_state" {
  type = object({
    bucket = string
    key    = string
    region = string
    endpoint = string
  })
}