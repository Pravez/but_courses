#import "../utils.typ"

== Self-Service BI

Maintenant que vous avez résolu le problème de sécurité, c'est le moment de profiter de votre MCP pour obtenir quelques statistiques sur votre base de données. Cela s'appelle du Self-Service BI (Business Intelligence) : vous pouvez obtenir des informations sur votre base de données, sans avoir besoin de vous soucier de la façon dont elle est stockée ou organisée. 

Les questions qui vont suivre sont purement du bonus. Vous pouvez donc les ignorer si vous le souhaitez. Indiquez les requêtes SQL écrites par le LLM dans le document de réponses, ainsi que la réponse qu'il a réussi à obtenir. Demandez-lui de formatter chaque résultat en CSV.

#utils.encart(title: "Un coup de pouce", type: "info")[Certaines requêtes sont plus complexes que d'autres. Le LLM risque d'avoir peut être un peu de mal dans certains cas (encore plus sur la version gratuite de Mistral) : n'hésitez pas à l'aider en lui donnant des indications sur la requête à écrire.]

#utils.question(num: 12, bonus: true)[Quel est le nombre d'étudiants par classe ?]
#utils.question(num: 13, bonus: true)[Quel est le GPA moyen par classe ?]
#utils.question(num: 14, bonus: true)[Quels sont les 5 cours les plus populaires ?]