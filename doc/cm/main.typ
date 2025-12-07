#import "templates.typ":*

// Configuration de la page (Format 16:9)
#set page(
  paper: "presentation-16-9",
  margin: 0cm,
  fill: bg-color,
  footer: footer-content(text-color.lighten(40%)),
  footer-descent: 0em,
)

// Configuration du texte
#set text(
  font: ("Roboto", "Arial", "Helvetica"),
  size: 20pt,
  fill: text-color,
)

// ==========================================
// CONTENU DU COURS
// ==========================================

#title-slide(
  title: "Architecture Cloud",
  subtitle: "Module R5.02 - IUT de Bordeaux",
  author: "Paul BRETON"
)

#include "parts/1_fondamentals.typ"
#include "parts/2_as-a-Service.typ"