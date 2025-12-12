variable "scaleway" {
  type = object({
    secret_key      = string
    access_key      = string
    organization_id = string
  })
}
