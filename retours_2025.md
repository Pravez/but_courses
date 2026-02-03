# Retours 2025

- faire attention aux mots de passe générés. L'attribut "override_special" veut en fait dire que ça va UNIQUEMENT prendre ces caractères là. Il faut exclure les ":#/\!?@*".
- ajouter la notion de terraform import quelque part.
- faire attention, quand la donnée est stockée dans un secret, il faut penser à faire un base64decode() quand le secret est récupéré
- mettre plus d'explications dans le TP de pourquoi Terraform, avantages/désavantages et enjeux.