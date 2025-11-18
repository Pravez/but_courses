#!/usr/bin/env nu

def main [year: string] {
    open $"raw/($year).csv" --raw
    | from csv --separator ";"
    | select "E-mail" "Nom"
    | rename "mail" "name"
    | insert "username" {|row|
        let words = ($row.name | split row " ")
        let last_word = ($words | last)
        let other_words = ($words | drop)

        # Get first letter of last word in lowercase
        let first_letter = ($last_word | str substring 0..0 | str downcase)

        # Get all other words, keep only letters, and convert to lowercase
        let other_part = ($other_words
            | str join ""
            | str replace --all --regex '[^a-zA-Z]' ''
            | str downcase)

        # Combine them
        $"($first_letter)($other_part)"
    }
    | insert "first_name" {|row| $row.name | split row " " | last}
    | insert "last_name" {|row| $row.name | split row " " | drop | str join " " }
    | to csv
    | save $"($year).csv"
}
