// Utilitaires (macros encart & question)
#import "utils.typ"

#let tp_titre = "TP Cloud" // Grand titre du TP
#let auteur = "BRETON Paul" // Votre nom et prénom
#let classe = "BUT Informatique" // Classe / groupe
#let annee = "2025–2026" // Année scolaire
#let etab = "IUT de Bordeaux" // Établissement

#set document(title: tp_titre, author: auteur)

// Palette & typo de base
#let primary = rgb(13, 71, 161)
#let accent = rgb(21, 101, 192)
#let neutral = rgb(38, 50, 56)
#set text(size: 11pt, fill: neutral)
#set par(justify: true)

// Mise en page avec en-tête et pied de page numéroté
#set page(margin: 2cm, numbering: "1", header: [
  #set text(size: 9pt, fill: rgb(96, 125, 139))
  #align(center)[#emph(tp_titre)]
], footer: context[
  #set text(size: 9pt, fill: rgb(96, 125, 139))
  #align(center)[— #counter(page).display("1") —]
])

#show link: it => [
  #set text(fill: rgb(96, 125, 139), style: "italic")
  #it
]

#show heading.where(level: 1): it => [
  #set text(size: 18pt, fill: primary)
  #it
  #v(4pt)
]
#show heading.where(level: 2): it => [
  #set text(size: 14pt, fill: accent)
  #it
  #v(4pt)
]

// Page de titre
#align(center)[
  #set text(size: 26pt)
  #strong(tp_titre)

  #v(8pt)
  #set text(size: 12pt)
  #emph(auteur)
  #linebreak()
  #classe · #annee · #etab
]

#v(20pt)
#include "parts/1_introduction.typ"
#include "parts/2_configuration.typ"
#include "parts/3_deployment.typ"
#include "parts/4_database.typ"
#include "parts/5_llm.typ"
#include "parts/6_bonus.typ"