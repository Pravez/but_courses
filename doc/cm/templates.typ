// ==========================================
// CONFIGURATION & THÈME
// ==========================================

// Palette de couleurs
#let bg-color = rgb("#FAF9F6")      // Beige clair / Coquille d'œuf
#let text-color = rgb("#2A2638")    // Gris très foncé légèrement violet
#let primary = rgb("#5E35B1")       // Violet profond
#let secondary = rgb("#9575CD")     // Violet clair
#let accent = rgb("#D1C4E9")        // Violet très pâle (pour les liens/fonds)
#let link-color = rgb("#7E57C2")    // Couleur des liens/réseaux

// État pour le fil d'ariane
#let current-section = state("current-section", none)

// Fonction de contenu du pied de page
#let footer-content(color) = context {
  let i = counter(page).get().first()
  if i > 1 {
    let sec = current-section.get()
    [
      #if sec != none {
        place(bottom + center, dy: -0.5cm)[
          #text(size: 14pt, fill: color, smallcaps(sec))
        ]
      }
      #place(bottom + right, dx: -0.5cm, dy: -0.5cm)[
        #text(size: 16pt, fill: color, [#i])
      ]
    ]
  }
}



// ==========================================
// ÉLÉMENTS GRAPHIQUES (RÉSEAU)
// ==========================================

// Fonction pour dessiner un "noeud" de réseau
#let node(x, y, r: 4pt, fill: primary) = place(top + left, dx: x - r, dy: y - r, circle(radius: r, fill: fill))

// Fonction pour dessiner une connexion
#let edge(x1, y1, x2, y2, stroke: 1pt + link-color) = place(top + left, line(start: (x1, y1), end: (x2, y2), stroke: stroke))

// Motif de fond "Réseau" (Coin haut droit et bas gauche)
#let network-decoration() = {
  // Coin haut droit
  let ox = 100%
  let oy = 0%
  place(top + right, dx: 0cm, dy: 0cm, box(width: 30%, height: 30%, clip: false)[
    #edge(80%, 10%, 60%, 40%)
    #edge(60%, 40%, 90%, 70%)
    #edge(60%, 40%, 30%, 20%)
    
    #node(80%, 10%, r: 5pt, fill: secondary)
    #node(60%, 40%, r: 8pt, fill: primary)
    #node(90%, 70%, r: 4pt, fill: accent)
    #node(30%, 20%, r: 3pt, fill: secondary)
  ])
  
  // Coin bas gauche
  place(bottom + left, dx: 0cm, dy: 0cm, box(width: 20%, height: 20%, clip: false)[
    #edge(20%, 80%, 50%, 50%)
    #node(20%, 80%, r: 6pt, fill: secondary)
    #node(50%, 50%, r: 3pt, fill: accent)
  ])
}

// ==========================================
// TYPES DE DIAPOSITIVES
// ==========================================

// 1. Diapositive de Grand Titre (Titre du Cours)
#let title-slide(title: "", subtitle: "", author: "") = {
  page(margin: 2cm)[
    #network-decoration()
    #align(center + horizon)[
      #box(inset: 20pt, stroke: (bottom: 2pt + primary))[
        #text(size: 2em, weight: "bold", fill: primary, title)
      ]
      #v(1em)
      #text(size: 1.2em, weight: "regular", fill: text-color.lighten(20%), subtitle)
      #v(2em)
      #text(size: 0.8em, style: "italic", author)
    ]
  ]
}

// 2. Diapositive de Titre de Partie (Section)
#let section-slide(number, title) = {
  current-section.update(title)
  page(fill: primary, margin: 2cm, footer: footer-content(white.transparentize(30%)))[
    // Réseau en version "négatif" (blanc sur violet)
    #let node-w(x, y, r: 4pt) = place(top + left, dx: x, dy: y, circle(radius: r, fill: white.transparentize(50%)))
    #let edge-w(x1, y1, x2, y2) = place(top + left, line(start: (x1, y1), end: (x2, y2), stroke: 1pt + white.transparentize(70%)))
    
    #box(width: 100%, height: 100%, inset: 0pt)[
      #edge-w(10%, 50%, 30%, 20%)
      #edge-w(30%, 20%, 70%, 80%)
      #edge-w(70%, 80%, 90%, 50%)
      #node-w(8.5%, 48%, r: 10pt)
      #node-w(29.2%, 19.%, r: 6pt)
      #node-w(69.2%, 78%, r: 8pt)
      #node-w(89.3%, 49.3%, r: 5pt)
      
      #align(center + horizon)[
        #text(size: 3em, weight: "bold", fill: white, number)
        #v(-1.5em)
        #text(size: 2.5em, weight: "bold", fill: white, title)
      ]
    ]
  ]
}

// 3. Diapositive standard (Contenu centré)
#let centered-slide(title: none, subtitle: none, body) = {
  page(margin: (top: 2.5cm, bottom: 1cm, x: 1.5cm))[
    #place(top + left, dy: -1.5cm)[
      #text(size: 1.2em, weight: "bold", fill: primary, title)
      #if subtitle != none {
        v(-0.5em)
        text(size: 0.85em, weight: "regular", fill: secondary.lighten(10%), subtitle)
        v(-0.2em)
        line(start: (0pt, 0pt), end: (100%, 0pt), stroke: 1pt + secondary)
      } else {
        v(-0.2em)
        line(start: (0pt, 0pt), end: (100%, 0pt), stroke: 1pt + secondary)
      }
    ]
    #align(center + horizon)[
      #set text(size: 1.1em)
      #body
    ]
    #place(bottom + right)[
      #circle(radius: 20pt, fill: accent.transparentize(80%))
    ]
  ]
}

// 4. Diapositive 2 colonnes (Texte + Image/Code)
#let dual-slide(title: none, subtitle: none, center-content, left-content, right-content) = {
  page(margin: (top: 2.5cm, bottom: 1cm, x: 1.5cm))[
    #place(top + left, dy: -1.5cm)[
      #text(size: 1.2em, weight: "bold", fill: primary, title)
      #if subtitle != none {
        v(-0.5em)
        text(size: 0.85em, weight: "regular", fill: secondary.lighten(10%), subtitle)
        v(-0.2em)
        line(start: (0pt, 0pt), end: (100%, 0pt), stroke: 1pt + secondary)
      } else {
        v(-0.2em)
        line(start: (0pt, 0pt), end: (100%, 0pt), stroke: 1pt + secondary)
      }
    ]
    #v(1.5cm)
    #if center-content != none {
      text(size: 1.1em)[#center-content]
    }
    #grid(
      columns: (1fr, 1fr),
      gutter: 1cm,
      align(left)[
        #if left-content != none {
          left-content
        }
        ],
      align(left)[
        #if right-content != none {
          right-content
        }
      ]
    )
  ]
}
