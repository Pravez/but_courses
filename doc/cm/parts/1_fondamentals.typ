#import "../templates.typ"

#templates.section-slide("I.", "Les Fondamentaux de l'économie du cloud")

#templates.centered-slide(title: "Introduction", subtitle: "Rappels")[
  Le *Cloud Computing* #text(size: 0.8em)[(ou infonuagique pour nos amis les québécois)] est la mise à disposition de ressources informatiques à la demande (puissance de calcul, stockage) via Internet, avec une tarification à l'usage.

  #v(1em)

  _« Il n'y a pas de Cloud, c'est juste l'ordinateur de quelqu'un d'autre. »_
]

#templates.dual-slide(title: "Introduction", subtitle: "Rappels")[
  Le web et ses applicatifs sont globalement divisés en deux parties distinctes :
][][]

#templates.dual-slide(title: "Introduction", subtitle: "Rappels")[
  Le web et ses applicatifs sont globalement divisés en deux parties distinctes :
][
  #v(0.5em)
  #align(center)[
    Le *Frontend*
    #v(0.1em)
    Tout ce avec quoi l'utilisateur va interagir
  ]
][
  #align(center)[
    Le *Backend*
  ]
]

#templates.dual-slide(title: "Modèles de Service")[][
  Il existe trois modèles principaux :

  - *IaaS* : Infrastructure as a Service
  - *PaaS* : Platform as a Service
  - *SaaS* : Software as a Service

  Chacun offre un niveau d'abstraction différent.
][
  #align(center)[
    #scale(120%)[
      #emoji.computer #h(5pt) *IaaS* \
      #v(5pt)
      #emoji.gear #h(5pt) *PaaS* \
      #v(5pt)
      #emoji.cloud #h(5pt) *SaaS*
    ]
  ]
]

