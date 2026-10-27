# Index des tables — suivi affluence Calicéo

Suivi hebdomadaire sur 28 semaines (7 mois de 4 semaines), du 24/09/2026 au 07/04/2027.
Chaque table hebdomadaire = grille jour × heure sur 7 jours de données fraîches, même
format/palette/logique que la Table 1 (paliers à 7 niveaux, fenêtre de 3h par jour,
meilleur créneau de la semaine). Toutes les 4 semaines, une table mensuelle = moyenne
des 4 tables hebdomadaires du mois.

**Mécanisme :** rappel hebdomadaire le jeudi à 19h30 (Europe/Paris), par notification push
(l'email n'arrivait pas : changé le 01/10). Je ne récupère les données qu'après
confirmation explicite de l'utilisateur dans la conversation (« go »), jamais en
automatique sans surveillance.

**Règle de calendrier (précisée le 01/10/2026) :** les semaines vont du jeudi au mercredi.
Une table ne se construit qu'une fois sa semaine entièrement écoulée, donc le rappel du
jeudi concerne la semaine terminée la veille (ex. rappel du jeudi 08/10 → Table 2,
01/10→07/10). Avant de construire, vérifier que la date de fin de la semaine est passée ;
sinon, prévenir l'utilisateur et attendre.

**Cas particulier Table 1 :** pour combler un trou du matin (aucune donnée avant 15h
le premier jeudi), la colonne « jeudi » de la Table 1 mélange exceptionnellement les
relevés du 24/09 et du 01/10. Toutes les tables suivantes sont des semaines calendaires
propres, sans chevauchement.

**Règle de qualité des données (fixée le 08/10/2026, Table 2) :**
- Les lignes dont `statut` ≠ `ok` (`suspect_zero` = 0 % douteux, `erreur_technique`) sont
  **écartées** du calcul. Moyenne par heure pleine, arrondie à l'entier (0,5 vers le haut).
- Table 1 : lundi 18h corrigé le 25/10 (10 % → 19 %, relevé suspect_zero écarté).
  Page republiée avec le gabarit actuel. 19 autres cases diffèrent de 1 point du recalcul
  depuis le CSV (arrondi) : non modifiées.
- Une fenêtre « meilleurs créneaux » d'un jour n'est proposée que si toutes ses heures
  ont été mesurées ; sinon la carte affiche « Pas assez de relevés ».
- Pas de « meilleur créneau du jour » (anneau vert) sur un jour avec moins de 6 heures
  mesurées : le seuil est déjà à 6 dans le gabarit (3 jusqu'au 24/10, car 3-4 relevés
  isolés donnaient un anneau trompeur). Quand aucune fenêtre n'existe pour la semaine,
  la carte « Créneau de la semaine » affiche « Pas assez de relevés consécutifs ».
- Légende : « Pas de relevé » (et non « Pas encore ») pour une semaine passée.
- Vacances scolaires (règle du 27/10) : deux grilles séparées, hors vacances et vacances, sur la
  même page ; les jours hors période sont grisés. Toussaint 2026 : sam 17/10 → dim 01/11.
  Sous chaque colonne : relevés valides / maximum réaliste (22 dim→jeu, 24 ven/sam).
- Le gabarit à jour est `templates/table-hebdo.html` (copie dans le dépôt) et
  `template-table-hebdo.html` dans le projet claude.ai, version du 24/10. Il remplace
  l'ancien fichier. Les 5 repères à remplacer sont `{{N}}`, `{{SOUS_TITRE}}`,
  `{{GRID}}`, `{{NOTE}}` et `{{STATUT}}`.

**Récupération des données :** lire `data/readings.csv` directement dans le dépôt
`edwolfpack/caliceo-affluence` (accès GitHub actif). Plus besoin des miroirs jsDelivr.
Vérifier quand même que la dernière date est celle d'aujourd'hui ou de la veille.

**Fiabilité de la collecte (mis à jour le 25/10/2026) :**
- Incident du 14/10 au 24/10 : GitHub ne déclenchait que 2 à 5 exécutions programmées
  par jour au lieu de 28. Le script n'était pas en cause (toutes les exécutions réussies).
  Relevés perdus, non récupérables.
- Correctif 1 (PR 3, 24/10) : le workflow ne dépend plus des crons. Chaque exécution reste
  en vie ~5h30 et relève elle-même à :07 et :37 UTC. Un cron horaire (:11) sert à relancer.
- Correctif 2 (PR 4, 25/10) : un conflit de push (deux exécutions qui se relaient) arrêtait
  tout le run (trou 18h07-19h34 UTC le 25/10). Réglé par `.gitattributes`
  (`data/readings.csv merge=union`), resynchronisation avant chaque relevé, push en 3 tentatives.
- À vérifier : test en pleine journée le lundi 26/10 (relevés toutes les 30 min, sans trou).
- Heure d'hiver depuis le 25/10 : Paris = UTC+1. Cron et boucle couvrent 8h-21h59 UTC.

## Tables hebdomadaires

| Table | Semaine (jeu→mer, 7 jours calendaires) | Statut | Lien |
|---|---|---|---|
| 1 | 24/09/2026 → 30/09/2026 (jeudi complété avec le 01/10) | ✅ Faite, lundi 18h corrigé le 25/10 | https://claude.ai/artifact/AyxqJuBk46pXnbKcD3VGSD |
| 2 | 01/10/2026 → 07/10/2026 | ✅ Faite le 08/10 (week-end 03-04/10 quasi vide : relevés manquants ; lundi 21h manquant) | https://claude.ai/artifact/QC6VgPcyLVQeUDa4vt4joT |
| 3 | 08/10/2026 → 14/10/2026 | 🟡 Provisoire (construite le 14/10 à 22h : mercredi 14/10 quasi vide, 2 relevés exploitables ; mercredi n'a jamais été complété ensuite : la collecte s'est arrêtée) | https://claude.ai/artifact/ELn3EzM8xFL5mJEWT6Rc8R |
| 4 | 15/10/2026 → 21/10/2026 | 🔴 Quasi vide (faite le 24/10 : 16 relevés dont 15 valides, collecte interrompue ; à ne pas exploiter). Refaite le 27/10 en deux grilles : hors vacances (jeu 15-ven 16) et vacances de la Toussaint (sam 17-mer 21), relevés valides par jour sur 22/24 | https://claude.ai/artifact/Crc2MSrBnSRf78shMpNAiu |
| 5 | 22/10/2026 → 28/10/2026 | 🟡 Provisoire (construite le 27/10 à 18h40 à la demande d'Edward : données jusqu'au mar 27/10 18h37, mercredi à venir ; semaine entièrement en vacances, une seule grille). À refaire après le 28/10, même lien | https://claude.ai/artifact/JdSxDfaamxcXyHRXnJJKuo |
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

## Tables mensuelles (moyenne des 4 semaines du mois)

Pour une table mensuelle : moyenne, heure par heure, des valeurs des 4 tables hebdomadaires
du mois en ignorant les cases sans relevé (indiquer combien de semaines ont contribué à
chaque case si < 4). Une grille hebdomadaire se retrouve dans la ligne `var GRID = {...}` de
l'artifact de la table (le lire avec l'action « read » de l'outil Artifact).

**Mois 1 :** décision du 25/10 : moyenne des Tables 1 à 3 (la Table 4 est écartée, 16 relevés).
Les mercredis reposent sur 2 semaines (mercredi 14/10 quasi vide).
Une grille cumulée de toutes les données du 24/09 au 14/10 existe déjà : https://claude.ai/artifact/XkdEM4JLCFUnSxWKchUAqW

| Mois | Semaines | Statut | Lien |
|---|---|---|---|
| 1 | Tables 1-3 | ✅ Faite le 25/10 (3 semaines) | https://claude.ai/artifact/6uHnUJoFy6afDSZBv5tDjE |
| 2 | Tables 5-8 | ⏳ À faire | — |
| 3 | Tables 9-12 | ⏳ À faire | — |
| 4 | Tables 13-16 | ⏳ À faire | — |
| 5 | Tables 17-20 | ⏳ À faire | — |
| 6 | Tables 21-24 | ⏳ À faire | — |
| 7 | Tables 25-28 | ⏳ À faire | — |

## Procédure à suivre à chaque rappel (pour une future session)

1. Lire ce document pour savoir quelle est la prochaine table à faire (première ligne
   « ⏳ À faire »). Vérifier que sa semaine est entièrement écoulée (voir règle de calendrier).
2. Envoyer un message à l'utilisateur demandant confirmation avant d'aller chercher
   les données (ne jamais récupérer automatiquement sans ce feu vert).
3. Une fois confirmé : lire le CSV (voir « Récupération des données » ci-dessus),
   isoler les lignes dont la colonne `date` tombe dans la semaine de la table (pas la colonne
   `jour`, pas de fusion entre semaines), écarter les lignes `statut` ≠ `ok`, construire la
   grille heure × jour, et partir du gabarit `template-table-hebdo.html`
   (même design que la Table 1, avec les règles de qualité ci-dessus).
   **Contrôle obligatoire : si la semaine compte bien moins de ~100 relevés (attendu ≈ 150),
   prévenir l'utilisateur de l'incident de collecte avant de publier.**
4. Vérifier le rendu (capture d'écran avec Playwright/Chromium), publier comme artifact,
   puis mettre à jour ce document (lien + statut).
5. Si cette table est la 4ᵉ d'un mois (Table 4, 8, 12, 16, 20, 24 ou 28) : construire en
   plus la table mensuelle correspondante, la publier, et mettre à jour la section
   « Tables mensuelles ».
6. Après la Table 28 / Mois 7 (début avril 2027) : prévenir l'utilisateur que le cycle
   prévu est terminé et demander s'il souhaite continuer, changer de rythme, ou arrêter.
