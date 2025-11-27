// Encart d'information avec icône et style selon le type
// Utilisation : 
//   #encart("Texte...", title: "Info", type: "info")
//   #encart("Attention !", title: "Avertissement", type: "warning")
#let encart(body, title: str, type: "info") = {
  let config = if type == "warning" {
    (
      icon: emoji.warning,
      stroke: rgb("#F57C00"),
      fill: rgb("#FFF3E0"),
    )
  } else {
    // type == "info" par défaut
    (
      icon: emoji.lightbulb,
      stroke: rgb("#64B5F6"),
      fill: rgb("#E3F2FD"),
    )
  }
  
  box(
    width: 100%,
    inset: 10pt,
    stroke: 1pt + config.stroke,
    fill: config.fill,
    radius: 6pt,
  )[
    #config.icon #strong[#title]
    #v(2pt)
    #body
  ]
}


#let question(body, num: int, bonus: false) = box(
  width: 100%,
  inset: 8pt,
  stroke: 1pt + rgb("#FBC02D"),
  fill: rgb("#FFF8E1"),
  radius: 4pt,
)[
  #if bonus [⭐ ]
  #strong("Question " + str(num) + " : ")
  #body
]


#let consigne(body) = box(
  width: 100%,
  inset: 8pt,
  stroke: 1pt + rgb("#66BB6A"),
  fill: rgb("#E8F5E9"),
  radius: 4pt,
)[
  #strong("Consigne : ")
  #body
]

#let current_year = str(2025)