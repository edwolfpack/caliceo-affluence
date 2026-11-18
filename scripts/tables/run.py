import sys; sys.argv=['x']
exec(open('build.py').read())
NOTE_COMMON="Les « meilleurs créneaux » excluent la dernière heure avant la fermeture (22h dim-jeu, 23h ven-sam). "
MATIN="Avant le correctif du 10/11, aucun relevé n'était pris avant 12h-15h : les cases du matin sont vides, ce n'est pas une absence de clients."
# T7
build(7,
 "Semaine du jeudi 05/11 au mercredi 11/11/2026, hors vacances scolaires (une seule grille : aucun jour de vacances cette semaine). Mercredi 11/11 est férié (Armistice). Chaque case = moyenne des relevés valides de cette heure.",
 "<b>Matinées manquantes.</b> 123 relevés, 121 valides (attendu ≈ 158 au maximum réaliste). Du jeudi 05/11 au lundi 09/11, premier relevé entre 12h55 et 15h19 : trou le matin. Correctif de la collecte le mardi 10/11 à 12h25 ; le mercredi 11/11 est le premier jour relevé dès 10h37, mais il manque 16h et 17h (aucun relevé entre 15h37 et 18h07). Relevés valides par jour sous chaque colonne, sur le maximum réaliste : <b>22</b> (dim→jeu) ou <b>24</b> (ven, sam). L'objectif initial était 28.",
 [('hv_','Hors vacances','Jeudi 05/11 → mercredi 11/11 (7 jours). Mercredi 11/11 férié : comparer avec prudence.',
   ['2026-11-05','2026-11-06','2026-11-07','2026-11-08','2026-11-09','2026-11-10','2026-11-11'],
   NOTE_COMMON+MATIN+" Mercredi 11/11 est un jour férié, son affluence ressemble plutôt à un week-end.")],
 'table7.html')
# T6
build(6,
 "Semaine du jeudi 29/10 au mercredi 04/11/2026, présentée en deux grilles : vacances de la Toussaint (jeu 29/10 → dim 01/11) et hors vacances (lun 02 → mer 04/11). Chaque case = moyenne des relevés valides de cette heure.",
 "<b>Matinées manquantes.</b> 130 relevés, 126 valides (attendu ≈ 158 au maximum réaliste). Aucun relevé avant 12h12 : GitHub retardait les lancements de plusieurs heures (corrigé le 10/11). Relevés valides par jour sous chaque colonne, sur le maximum réaliste : <b>22</b> (dim→jeu) ou <b>24</b> (ven, sam). L'objectif initial était 28.",
 [('va_','Vacances de la Toussaint','Jeudi 29/10 → dimanche 01/11. Lundi, mardi et mercredi sont hors période (grisés).',
   ['2026-10-29','2026-10-30','2026-10-31','2026-11-01'], NOTE_COMMON+MATIN+" Dimanche 01/11 (Toussaint) est férié."),
  ('hv_','Hors vacances','Lundi 02/11 → mercredi 04/11. Jeudi à dimanche sont hors période (grisés).',
   ['2026-11-02','2026-11-03','2026-11-04'], NOTE_COMMON+MATIN)],
 'table6.html')
