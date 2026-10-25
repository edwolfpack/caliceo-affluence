# Index des tables — suivi affluence Calicéo

Suivi hebdomadaire sur 28 semaines (7 mois de 4 semaines), du 24/09/2026 au 07/04/2027.
Chaque table hebdomadaire = grille jour × heure sur 7 jours de données, construite avec le
gabarit `templates/table-hebdo.html` (à jour au 24/10/2026). Toutes les 4 semaines, une table
mensuelle = moyenne des tables hebdomadaires du mois.

**Mécanisme :** rappel hebdomadaire le jeudi à 19h30 (Europe/Paris), notification push.
Les données ne sont récupérées qu'après un « go » explicite de l'utilisateur.

**Calendrier :** semaines du jeudi au mercredi. Une table ne se construit qu'une fois sa semaine
entièrement écoulée. Le rappel du jeudi concerne la semaine terminée la veille.
Table 1 : sa colonne « jeudi » mélange les relevés du 24/09 et du 01/10 (trou du matin).

**Règles de qualité des données :**
- Lignes dont `statut` ≠ `ok` écartées (`suspect_zero`, `erreur_technique`). Moyenne par heure
  pleine, arrondie à l'entier (0,5 vers le haut).
- « Meilleur créneau du jour » (anneau vert) seulement si le jour compte au moins 6 heures
  mesurées (seuil passé de 3 à 6 le 24/10).
- Fenêtre « meilleurs créneaux » d'un jour : seulement si toutes ses heures sont mesurées, sinon
  « Pas assez de relevés ». Sans fenêtre pour la semaine : « Pas assez de relevés consécutifs ».
- Légende : « Pas de relevé » (et non « Pas encore »).
- Table 1 : lundi 18h corrigé le 25/10 (10 % → 19 %, relevé suspect_zero écarté). Page republiée
  avec le gabarit actuel. 19 autres cases diffèrent de 1 point du recalcul depuis le CSV
  (arrondi) : non modifiées.

**Récupération des données :** lire `data/readings.csv` directement dans le dépôt
`edwolfpack/caliceo-affluence`. Vérifier que la dernière date est celle d'aujourd'hui ou de la veille.
Filtrer sur la colonne `date` (pas `jour`) et contrôler le nombre de lignes par date avant de calculer.

**Fiabilité de la collecte (mis à jour le 25/10/2026) :**
- Incident du 14/10 au 24/10 : GitHub ne déclenchait que 2 à 5 exécutions programmées par jour au
  lieu de 28. Le script n'était pas en cause (toutes les exécutions réussies). Relevés perdus,
  non récupérables.
- Correctif 1 (PR 3, 24/10) : le workflow ne dépend plus des crons. Chaque exécution reste en vie
  ~5h30 et relève elle-même à :07 et :37 UTC. Un cron horaire (:11) sert à relancer.
- Correctif 2 (PR 4, 25/10) : un conflit de push (deux exécutions qui se relaient) arrêtait tout le
  run (trou 18h07-19h34 UTC le 25/10). Réglé par `.gitattributes` (`data/readings.csv merge=union`),
  resynchronisation avant chaque relevé, push en 3 tentatives.
- À vérifier : test en pleine journée le lundi 26/10 (relevés toutes les 30 min, sans trou).
- Heure d'hiver depuis le 25/10 : Paris = UTC+1. Cron et boucle couvrent 8h-21h59 UTC.
- Valeurs plus hautes depuis le 17/10 en semaine (27 à 43 % vers 20h contre ~20 %) : vacances de la
  Toussaint possibles (zone C), non confirmé.

## Tables hebdomadaires

| Table | Semaine (jeu→mer) | Statut | Lien |
|---|---|---|---|
| 1 | 24/09/2026 → 30/09/2026 (jeudi complété avec le 01/10) | ✅ Faite, lundi 18h corrigé le 25/10 | https://claude.ai/artifact/AyxqJuBk46pXnbKcD3VGSD |
| 2 | 01/10/2026 → 07/10/2026 | ✅ Faite le 08/10 (week-end 03-04/10 quasi vide) | https://claude.ai/artifact/QC6VgPcyLVQeUDa4vt4joT |
| 3 | 08/10/2026 → 14/10/2026 | 🟡 Provisoire (mercredi 14/10 quasi vide) | https://claude.ai/artifact/ELn3EzM8xFL5mJEWT6Rc8R |
| 4 | 15/10/2026 → 21/10/2026 | 🔴 Quasi vide (16 relevés), à ne pas exploiter | https://claude.ai/artifact/Crc2MSrBnSRf78shMpNAiu |
| 5 | 22/10/2026 → 28/10/2026 | ⏳ À faire | — |
| 6 | 29/10/2026 → 04/11/2026 | ⏳ À faire | — |
| 7 | 05/11/2026 → 11/11/2026 | ⏳ À faire | — |
| 8 | 12/11/2026 → 18/11/2026 | ⏳ À faire | — |
| 9 | 19/11/2026 → 25/11/2026 | ⏳ À faire | — |
| 10 | 26/11/2026 → 02/12/2026 | ⏳ À faire | — |
| 11 | 03/12/2026 → 09/12/2026 | ⏳ À faire | — |
| 12 | 10/12/2026 → 16/12/2026 | ⏳ À faire | — |
| 13 | 17/12/2026 → 23/12/2026 | ⏳ À faire | — |
| 14 | 24/12/2026 → 30/12/2026 | ⏳ À faire | — |
| 15 | 31/12/2026 → 06/01/2027 | ⏳ À faire | — |
| 16 | 07/01/2027 → 13/01/2027 | ⏳ À faire | — |
| 17 | 14/01/2027 → 20/01/2027 | ⏳ À faire | — |
| 18 | 21/01/2027 → 27/01/2027 | ⏳ À faire | — |
| 19 | 28/01/2027 → 03/02/2027 | ⏳ À faire | — |
| 20 | 04/02/2027 → 10/02/2027 | ⏳ À faire | — |
| 21 | 11/02/2027 → 17/02/2027 | ⏳ À faire | — |
| 22 | 18/02/2027 → 24/02/2027 | ⏳ À faire | — |
| 23 | 25/02/2027 → 03/03/2027 | ⏳ À faire | — |
| 24 | 04/03/2027 → 10/03/2027 | ⏳ À faire | — |
| 25 | 11/03/2027 → 17/03/2027 | ⏳ À faire | — |
| 26 | 18/03/2027 → 24/03/2027 | ⏳ À faire | — |
| 27 | 25/03/2027 → 31/03/2027 | ⏳ À faire | — |
| 28 | 01/04/2027 → 07/04/2027 | ⏳ À faire | — |

La Table 5 (22/10 → 28/10) sera partielle : la collecte n'a repris que le 24/10.

## Tables mensuelles

Moyenne, heure par heure, des grilles hebdomadaires du mois en ignorant les cases sans relevé
(indiquer le nombre de semaines contributrices si < 4). Une grille se lit dans la ligne
`var GRID = {...}` de la page de la table.

**Mois 1 :** décision du 25/10 : moyenne des Tables 1 à 3 (Table 4 écartée, 16 relevés).
Les mercredis reposent sur 2 semaines (mercredi 14/10 quasi vide).

| Mois | Semaines | Statut | Lien |
|---|---|---|---|
| 1 | Tables 1-3 | ✅ Faite le 25/10 (3 semaines) | https://claude.ai/artifact/6uHnUJoFy6afDSZBv5tDjE |
| 2 | Tables 5-8 | ⏳ À faire | — |
| 3 | Tables 9-12 | ⏳ À faire | — |
| 4 | Tables 13-16 | ⏳ À faire | — |
| 5 | Tables 17-20 | ⏳ À faire | — |
| 6 | Tables 21-24 | ⏳ À faire | — |
| 7 | Tables 25-28 | ⏳ À faire | — |

Autres pages : grille cumulée 24/09→14/10 https://claude.ai/artifact/XkdEM4JLCFUnSxWKchUAqW

## Procédure à chaque table hebdomadaire

1. Trouver la prochaine table « ⏳ À faire » et vérifier que sa semaine est entièrement écoulée.
2. Demander le « go » de l'utilisateur avant de lire les données.
3. Lire `data/readings.csv`, filtrer sur `date`, écarter `statut` ≠ `ok`, construire la grille.
   Si la semaine compte bien moins de ~100 relevés (attendu ≈ 150), prévenir l'utilisateur de
   l'incident de collecte avant de publier.
4. Remplir `templates/table-hebdo.html` (5 repères : `{N}`, `{SOUS_TITRE}`, `{GRID}`,
   `{NOTE}`, `{STATUT}`), vérifier le rendu, publier, puis mettre à jour ce document.
5. Après les Tables 4, 8, 12, 16, 20, 24 et 28 : construire aussi la table mensuelle.
6. Après la Table 28 (début avril 2027) : prévenir que le cycle est terminé et demander la suite.
