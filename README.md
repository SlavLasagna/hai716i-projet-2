# HAI716I - Projet 2

## Lancement

### Dépendances

Python 3.10+

### Commandes

```bash
python main.py [-options]
```

Options disponibles:

- `-r <n>` ou `--rounds <n>` pour changer le nombre de tours par partie à `n`.
- `-g <n>` ou `--games <n>` pour changer le nombre de parties par groupe à `n`.
- `-t <n>` ou `--tournaments <n>` pour changer le nombre de tournois à `n`.
- `-s <n>` ou `--seed <n>` pour surcharger la seed du générateur aléatoire à `n`.
- `-n <f>` ou `--noise <f>` pour que le bruit par coup soit de `f`%.
- `-z <w>` ou `--horizon <w>` pour que les parties aient `w`% de chance de se terminer avant le nombre de tours.   
- `-p <point_matrix>` ou `--points <point_matrix>` pour surcharger le tableau des points par `point_matrix`, sous le format `C,C:C,D:D,C:D,D`.
- `-v <level>` ou `--verbose <level>` pour activer l'affichage du déroulé des parties.

L'option `verbose` possède actuellement 3 niveaux:
- `0`: par défaut, affiche seulement les résultats finaux, c'est-à-dire le score moyen par tour par partie.
- `1`: affiche les résultats de chaque partie groupée par groupe de tournoi.
- `2`: affiche les scores pour chaque tour de chaque partie de chaque groupe.

## Journal de bord

### Protocole

#### Format du tournoi :

| Paramètre         | Valeur                                                             | Raison                                                                                                          |
|-------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Parties par paire | 5                                                                  | format imposé par l'énoncé                                                                                      |
| Tours par partie  | 200                                                                | format imposé par l'énoncé                                                                                      |
| Gains             | C,C = 3,3; C,D = 0,5; D,C = 5,0; D,D = 2,2                         | matrice du cours                                                                                                |
| Auto-match        | non                                                                | l'énoncé demande « chaque stratégie contre chaque autre »                                                       |
| Graine            | Vide (paramétrable)                                                | résultats rejouables à l'identique                                                                              |
| Score affiché     | moyenne de points par tour : `score / (parties × tours × (n − 1))` | comparable entre populations de tailles différentes ; même ordre que le score total tant que l'horizon est fixe |

#### Modifications 

### Stratégies

- All-D:
  - Règle : toujours D.
  - Origine : stratégie « rationnelle » de la récurrence à rebours.
  - Bien contre : les naïfs (All-C : 5 par tour, Random : 3,5, TF2T pendant ses deux premiers tours).
  - Mal contre : personne en particulier, elle fait au pire 2 par tour (D, D) ; elle ne rapporte jamais plus que ça contre une stratégie qui riposte.

- Random:
  - Règle : C ou D avec une chance sur deux.
  - Origine : témoin du tournoi d'Axelrod.
  - Bien contre : All-C (4 par tour, car elle trahit la moitié du temps sans être punie).
  - Mal contre : All-D (1 par tour).

- Tit-For-Tat (TFT):
- Règle : C au premier tour, puis rejoue le dernier coup de l'adversaire.
- Origine : Anatol Rapoport, gagnante du tournoi de 1980.
- Bien contre : les stratégies coopératives (3 points par tour avec All-C, TF2T, Tester une fois que celui-ci a riposté).
- Mal contre : All-D (perd 0 contre 5 au premier tour, puis 2 contre 2). Contre Joss, un D isolé de Joss déclenche un écho de représailles qui finit en défection mutuelle. TFT ne bat jamais son adversaire en duel.

- Tester:
- Règle : D en premier. Si l'adversaire riposte (joue D à partir du tour 1), s'excuse en jouant C une fois puis joue TFT pour toujours ; sinon répète C, C, D (à partir du tour 1).
- Origine : tournoi d'Axelrod (soumission de David Gladstein)..
- Bien contre : les adversaires qui ne ripostent jamais (All-C, TF2T) : le motif C, C, D lui rapporte (5+3+3)/3 ~= 3,67 par tour contre 2 pour eux.
- Mal contre : All-D (devient TFT, donc ~= 2/2), Joss (écho de représailles).

- Joss:
- Règle : TFT, mais chaque C est remplacé par D avec probabilité de 10%.
- Origine : soumission au tournoi d'Axelrod (TFT sournoise).
- Bien contre : les stratégies qui pardonnent ou ne ripostent pas (All-C).
- Mal contre : TFT et Tester : un D de Joss déclenche un écho de représailles qui finit en défection mutuelle (2 par tour) ; en pratique elle se punit elle-même.

- All-C, ajoutée à l'étape 2:
- Règle : toujours C.
- Origine : stratégie « All-C » classique de la littérature, utilisée comme témoin naïf.
- Bien contre : TFT et TF2T (3 par tour, coopération).
- Mal contre : tout ce qui trahit : ALL-D (0 par tour), Tester, Random, Joss. Elle ne punit jamais.

- TF2T (Tit-for-2-tats), ajoutée à l'étape 2:
- Règle : C, sauf si l'adversaire a joué D aux deux derniers tours.
- Origine : stratégie classique de la littérature.
- Bien contre : les stratégies qui ripostent tout de suite (TFT, Joss) : un D isolé ne la fait pas entrer dans un écho.
- Mal contre : Tester, dont le motif C, C, D ne produit jamais deux D de suite : elle est exploitée tout le long de la partie.


### Observations et prédictions

Les scores sont des points moyens par tour. Pour chaque expérience : le résultat à la graine par défaut (`main.py`) et la moyenne sur 200 graines avec le nombre de victoires (`robustness.py`). Seule la seconde permet de conclure. Les scores par paire cités plus bas ont été mesurés séparément (300 parties par paire).
 
#### Étape 1
 
Résultat (5 stratégies, graine par défaut, puis 200 graines) :
 
| Rang | Graine par défaut | Moyenne sur 200 graines | Victoires sur 200 |
|---|---|---|---|
| 1 | AllD 2,386 | TFT 2,391 | TFT 77 |
| 2 | Tester 2,386 | AllD 2,389 | AllD 73 |
| 3 | TFT 2,382 | Tester 2,388 | Tester 50 |
| 4 | Joss 2,191 | Joss 2,202 | 0 |
| 5 | Random 2,102 | Random 2,094 | 0 |
 
TIT-FOR-TAT gagne-t-il chez moi ? Pas clairement. À la graine par défaut, TFT est troisième, à 0,004 point d'AllD et de Tester (ex æquo à 3 décimales). Sur 200 graines, TFT gagne le plus souvent (77 fois, 38 %), mais devant AllD (73) et Tester (50), avec des moyennes quasi identiques (2,391 / 2,389 / 2,388). Ces trois stratégies sont à égalité statistique : TFT n'est pas la gagnante de ce tournoi.
 
Pourquoi le résultat diffère de 1980. Le tournoi d'Axelrod réunissait une quinzaine de programmes, presque tous « gentils » (ils ne trahissent pas en premier). TFT y prospérait en coopérant avec eux. Ici, sur 4 adversaires, un seul coopère vraiment avec TFT. Scores par paire mesurés (points par tour de TFT) :
 
- contre Tester : 3,00 (seule vraie coopération, après la riposte de Tester) ;
- contre Random : ~= 2,5 ;
- contre Joss : 2,10 (un D de Joss lance un écho qui s'enferme en défection mutuelle) ;
- contre AllD : 1,99.
La moyenne vaut (3,00 + 2,5 + 2,10 + 1,99) / 4 ~= 2,40, ce qui correspond au 2,39 observé. TFT ne bat jamais personne en duel (diapo 67) : il ne gagne que s'il rencontre assez de partenaires coopératifs. AllD obtient le même score autrement : 3,5 contre Random et ~= 2 contre les trois autres.
 
#### Étape 2
 
Résultat (7 stratégies) :
 
| Rang | Graine par défaut | Moyenne sur 200 graines | Victoires sur 200 |
|---|---|---|---|
| 1 | Tester 2,813 | Tester 2,815 | Tester 200 |
| 2 | AllD 2,763 | AllD 2,765 | 0 |
| 3 | TFT 2,606 | Random 2,606 | 0 |
| 4 | Random 2,598 | TFT 2,594 | 0 |
| 5 | Joss 2,536 | Joss 2,514 | 0 |
| 6 | TF2T 2,446 | TF2T 2,434 | 0 |
| 7 | AllC 2,049 | AllC 2,033 | 0 |
 
Comparaison avec l'étape 1 (rang des stratégies du cours, graine par défaut) : AllD 1 -> 2, Tester 2 -> 1, TFT 3 -> 3, Joss 4 -> 5, Random 5 -> 4. Les deux nouvelles stratégies finissent 6ème (TF2T) et 7ème (All-C).
 
Explication. All-C et TF2T ne ripostent presque jamais, ce sont des proies. Tester en profite le plus : son motif C, C, D lui rapporte 3,67 par tour contre l'une comme contre l'autre (2,00 pour elles). All-D ne tire parti que d'All-C (5,00) : contre TF2T il ne fait que ~= 2,03, car TF2T finit par riposter. Tester passe de 2e à 1er (200 victoires sur 200). TFT ne gagne rien à cet élargissement : ses nouveaux partenaires lui rapportent 3 par tour, alors que Tester en tire 3,67.
 
#### Étape 3
 
Les prédictions ci-dessous ont été écrites avant de lancer la moindre modification. Référence : le classement de l'étape 2 (estimation faite avant les lancements par calcul des scores par paire : Tester ~= 2,8 ; All-D ~= 2,75 ; Random ~= 2,6 ; TFT ~= 2,6 ; Joss ~= 2,5 ; TF2T ~= 2,4 ; All-C ~= 2,0).
 
##### Bruit (5 %)
 
Deux stratégies qui ripostent (TFT contre TFT, par exemple) entrent en écho après une erreur : un D isolé en provoque un autre, puis encore un autre. Avec 5 % de bruit, un calcul de chaîne de Markov donne pour deux TFT : 25 % du temps (C, C), 25 % (D, D), 50 % en écho (C, D) / (D, C), soit une moyenne de ~= 2,5 par tour au lieu de 3.
 
1. TFT baisse d'environ 0,1 (~= 2,6 -> ~= 2,5), à cause des échos avec Tester et Joss.
2. Tester perd sa première place et baisse le plus (~= 2,8 -> ~= 2,55). Son avantage vient de proies qui ne jouent jamais D (All-C, TF2T) ; avec 5 % de bruit, elles jouent D tôt ou tard (en moyenne vers le 20ᵉ tour), Tester prend cela pour une riposte et passe en TFT définitivement.
3. All-D est presque inchangé (~= 2,75) et devient premier.
4. TF2T monte (~= 2,4 -> ~= 2,5) : elle ne tombe pas dans l'écho et n'est plus exploitée durablement par Tester.
5. All-C reste dernière (~= 2,0). Random est quasi inchangée.
6. Les stratégies du milieu (Random, TFT, TF2T, Joss, Tester) se resserrent à environ 0,1 d'écart ; leur ordre ne sera pas fiable avec seulement 5 parties par paire.
7. TFT ne gagnera pas.
Résultat :
 
| Rang | Graine par défaut | Moyenne sur 200 graines | Victoires sur 200 |
|---|---|---|---|
| 1 | AllD 2,836 | AllD 2,846 | AllD 200 |
| 2 | Joss 2,616 | Joss 2,614 | 0 |
| 3 | Random 2,584 | Random 2,596 | 0 |
| 4 | Tester 2,571 | Tester 2,573 | 0 |
| 5 | TFT 2,529 | TFT 2,558 | 0 |
| 6 | TF2T 2,490 | TF2T 2,490 | 0 |
| 7 | AllC 2,151 | AllC 2,151 | 0 |
 
Variation par rapport à l'étape 2 (moyennes sur 200 graines) : AllD +0,081 ; Joss +0,100 ; Random −0,010 ; Tester −0,242 ; TFT −0,036 ; TF2T +0,056 ; All-C +0,118.
 
Écart et explication.
 
- Confirmé : (2) Tester perd la première place et baisse le plus (−0,24). Le mécanisme annoncé est mesuré : contre All-C, Tester passe de 3,67 / 2,00 à 3,09 / 2,73, et contre TF2T de 3,67 / 2,00 à 3,06 / 2,75 (une erreur de la proie lui fait quitter son motif d'exploitation). (3) All-D est premier à 200 victoires sur 200. (5) All-C reste dernière et Random est stable. (6) Joss, Random, Tester et TFT sont à 0,06 les uns des autres. (7) TFT ne gagne pas.
- Magnitude moins forte que prévu : (1) TFT baisse de 0,036 (−0,077 à la graine par défaut) au lieu de 0,1. L'écho existe bien : TFT–Tester passe de 3,00 à 2,53, valeur proche des 2,5 du calcul de Markov. Mais TFT–Joss monte de 2,08 à 2,32 et compense en partie (voir plus bas). (4) TF2T gagne 0,056 au lieu de 0,1.
- Écart sur All-D : (3) il n'est pas « presque inchangé » mais gagne 0,08. Les erreurs de ses adversaires lui donnent T=5 au lieu de P=2 : AllD–TFT passe de 2,02 à 2,20. Je n'avais compté que les erreurs d'All-D lui-même.
- Non prédit : Joss monte de 0,10 et finit 2ᵉ. Sans bruit, la défection mutuelle est un état absorbant pour les paires Joss–TFT et Joss–Tester (2,10 par tour). Avec du bruit, une erreur peut rouvrir la coopération : Joss–TFT passe de 2,10 / 2,08 à 2,40 / 2,32 et Joss–Tester de 2,11 / 2,09 à 2,40 / 2,32.
- Non prédit : All-C gagne 0,12 (2,03 -> 2,15), pour la même raison que le recul de Tester : elle n'est plus exploitée durablement (Tester–All-C : 2,00 -> 2,73 pour All-C).
##### Horizon inconnu
 
Plus w est petit, plus le premier tour pèse. Les stratégies qui trahissent d'entrée (All-D, Tester) en profitent ; celles qui commencent par C et ripostent ensuite (TFT) ont besoin de plusieurs tours. Résultat théorique de référence : TFT contre TFT résiste à All-D si w ≥ (T−R)/(T−P) = 2/3 et w ≥ (T−R)/(R−S) = 2/3.
 
1. À w = 0,995 (~= 200 tours en moyenne), le classement ressemble à la référence : Tester et All-D en tête.
2. All-D est premier pour les petits w (0,5 à 0,8). Son score par tour est alors élevé (~= 3,4 à w = 0,5) et décroît quand w augmente (~= 2,75 à 0,995).
3. Tester dépasse All-D quelque part entre w = 0,8 et w = 0,95.
4. Le score de TFT augmente avec w (~= 2,0 à w = 0,5, ~= 2,6 à w = 0,995), mais TFT ne devient jamais première : la population contient des proies (All-C, TF2T) qui profitent surtout à All-D et à Tester. Je ne m'attends donc pas à un basculement net du classement en faveur de TFT au seuil théorique w = 2/3.
5. La dispersion d'une graine à l'autre est grande pour les petits w (parties de 1 à 3 tours) : il faudra plusieurs graines.
Résultat (moyenne de points par tour sur 200 graines ; `-r 10000`) :
 
| `-z` (h) | 50 % | 20 % | 10 % | 5 % | 1 % | 0,5 % |
|---|---|---|---|---|---|---|
| w | 0,5 | 0,8 | 0,9 | 0,95 | 0,99 | 0,995 |
| Longueur moyenne | 2 | 5 | 10 | 20 | 100 | 200 |
| AllD | 3,806 | 3,283 | 3,032 | 2,901 | 2,790 | 2,785 |
| Tester | 3,090 | 2,827 | 2,817 | 2,851 | 2,821 | 2,819 |
| Random | 2,894 | 2,794 | 2,714 | 2,657 | 2,619 | 2,609 |
| Joss | 2,475 | 2,679 | 2,691 | 2,666 | 2,548 | 2,495 |
| TFT | 2,280 | 2,547 | 2,603 | 2,624 | 2,602 | 2,598 |
| TF2T | 2,016 | 2,255 | 2,345 | 2,400 | 2,431 | 2,424 |
| AllC | 1,920 | 1,986 | 2,016 | 2,020 | 2,026 | 2,013 |
 
En gras : le premier de chaque colonne (moyenne la plus haute).
 
Victoires sur 200 : w = 0,5 : AllD 199 ; w = 0,8 : AllD 192, Random 5, Tester 3 ; w = 0,9 : AllD 158, Tester 26, Random 14, Joss 2 ; w = 0,95 : AllD 104, Tester 73, Random 19, Joss 4 ; w = 0,99 : Tester 96, AllD 82, Random 21, TFT 1 ; w = 0,995 : Tester 101, AllD 75, Random 18, TFT 6.
 
Écart et explication.
 
- Confirmé : (2) All-D est premier de w = 0,5 à 0,9 et son score décroît de façon continue avec w (3,81 -> 2,79). (4) Le score de TFT augmente avec w jusqu'à w = 0,95 puis se stabilise (2,60), et TFT ne passe jamais devant All-D ni Tester : 5ᵉ à w = 0,5 et 0,8, 4ᵉ ou 5ᵉ ensuite. Il n'y a pas de basculement au seuil théorique 2/3. (5) La dispersion est forte pour les petits w : à w = 0,9, All-D fait 3,703 à la graine par défaut contre 3,032 en moyenne sur 200 graines. À cet horizon, un seul tournoi n'est pas interprétable.
- (1) en partie : à w = 0,995, Tester et All-D sont bien en tête et leurs moyennes sont celles de l'étape 2 (2,819 / 2,785 contre 2,815 / 2,765). Mais Tester gagne 101 fois sur 200 au lieu de 200 sur 200 : des parties de longueur variable ajoutent du hasard qui n'existe pas à 200 tours fixes.
- (3) manqué : le dépassement a lieu plus tard que prévu. All-D reste devant jusqu'à w = 0,95 (2,901 contre 2,851 pour Tester) et Tester passe devant à w = 0,99. Explication mesurée : le gain d'All-D est une prime unique du premier tour (5 au lieu de 2 contre ceux qui ripostent), qui se dilue en 1/longueur. All-D contre TFT : 2,31 à w = 0,9 contre 2,02 à w = 0,995, soit ~= 3/10 de prime sur 10 tours. Les gains de Tester, eux, ne dépendent presque pas de la longueur : 2,93 / 2,88 contre TFT à w = 0,9 et 3,67 contre les proies. À w = 0,95, la prime d'All-D est encore de ~= 0,1 sur la moyenne, ce qui suffit à le garder devant.
- Magnitudes : All-D fait 3,81 à w = 0,5 au lieu des ~= 3,4 prévus (j'ai sous-estimé le poids du premier tour sur des parties de 2 tours). TFT fait 2,28 à w = 0,5 au lieu de ~= 2,0 prévu.
- Non prédit : Joss atteint son maximum à w = 0,9 (2,69) puis redescend à 2,50. Hypothèse, non vérifiée : le blocage en défection mutuelle avec TFT et Tester met une dizaine de tours à s'installer, donc les parties courtes l'épargnent.
##### Autres gains
 
Prédictions.
 
(a) Chasse au cerf (R=4, S=0, T=3, P=1). La coopération (4) bat la trahison réussie (3) : trahir ne rapporte presque rien.
 
1. All-D est dernier (~= 1,5).
2. Les stratégies coopératives sont groupées en tête, entre 2,7 et 2,9 environ : TF2T, TFT, All-C, Tester.
3. All-C n'est plus dernière (~= 2,7).
4. Random ~= 2,1 et Joss ~= 2,35 sont derrière le groupe de tête.
5. TFT dans les 3 premières.
(b) Poule mouillée (R=3, S=1, T=5, P=0). Ici la pire issue est la défection mutuelle (0), pire que d'être le pigeon (1) : céder vaut mieux que se battre.
 
1. All-D est dernier (~= 1,3) : il tombe sur (D, D) = 0 contre tout ce qui riposte.
2. Joss est avant-dernier (~= 1,6) : ses paires avec TFT et Tester finissent en défection mutuelle, qui vaut 0 ici.
3. Les stratégies qui cèdent sont en haut : Random ~= 2,4, All-C ~= 2,35, TF2T ~= 2,2, Tester ~= 2,2.
4. All-C passe de dernière à parmi les meilleures.
5. TFT au milieu (~= 1,9) : elle riposte, donc elle s'enferme dans (D, D) contre Joss et All-D.
Résultat (moyenne sur 200 graines, victoires entre parenthèses ; la graine par défaut donne le même ordre sauf mention) :
 
| Rang | Chasse au cerf | Poule mouillée |
|---|---|---|
| 1 | TF2T 2,831 (196) | Random 2,374 (166) |
| 2 | AllC 2,710 (3) | AllC 2,355 (34) |
| 3 | TFT 2,692 (1) | Tester 2,171 |
| 4 | Tester 2,578 | TF2T 2,170 |
| 5 | Joss 2,146 | TFT 1,947 |
| 6 | Random 2,107 | Joss 1,547 |
| 7 | AllD 1,510 | AllD 1,274 |
 
Avec la graine `0xDEADBEEF`, Tester (2,148) et TF2T (2,213) sont inversés (3ᵉ/4ᵉ) en poule mouillée : les deux sont à égalité statistique (2,171 contre 2,170).
 
Écart et explication.
 
- Poule mouillée : toutes les prédictions sont confirmées, y compris les ordres de grandeur (All-D 1,27 ; Joss 1,55 ; Random 2,37 ; All-C 2,36 ; TF2T 2,17 ; Tester 2,17 ; TFT 1,95). Mécanismes mesurés : AllD–TFT = 0,03 / 0,01 et TFT–Joss = 0,41 / 0,43 (la défection mutuelle vaut 0 et s'installe) ; All-C contre All-D fait 1 par tour (S=1 > P=0), d'où sa remontée de dernière à 2ᵉ.
- Chasse au cerf : confirmé : (1) All-D dernier (1,51). (3) All-C est 2ᵉ (2,71). (5) TFT est 3ᵉ. (2) Le groupe de tête TF2T / All-C / TFT est bien entre 2,69 et 2,87. Cependant All-D ne gagne que 3,00 contre All-C (au lieu de 5), ce qui explique sa dernière place.
- Écarts chasse au cerf : Tester (2,58) est un peu sous la fourchette 2,7-2,9 annoncée, et Joss (2,15) est sous les ~= 2,35 annoncés. Joss–TFT ne fait que 1,17 / 1,19 (blocage en (D, D) = 1). En revanche, TF2T–Joss fait 3,27 / 3,53 : TF2T évite le blocage que subit TFT, ce qui explique que TF2T gagne 196 fois sur 200. Dans mes prédictions TF2T figurait en tête de liste sans que j'annonce un tel écart sur TFT.

### Impasses

1. `Tester` ne tenait pas sa règle.
   - Symptôme : contre TFT, la partie finissait en défection mutuelle (`DCDCDDDD…` contre `CDCDCDDD…`) alors que Tester doit finir en coopération.
   - Cause : le programme ne retenait pas que l'adversaire avait riposté, donc il continuait d'insérer un D tous les 3 appels (`repeat % 3`) même après être passé en TFT. De plus le compteur incluait le tour 0, ce qui décalait le motif (`DCDCCD…` au lieu de `DCCDCCD…`).
   - Correction : un drapeau `retaliated` ; une fois la riposte vue, Tester joue TFT définitivement ; le motif C, C, D est calculé avec `(round_n − 1) % 3`.
2. `Joss` était déterministe. Le premier code remplaçait un C par D toutes les 10 coopérations (périodicité de 11 tours en pratique) et la graine n'avait aucun effet sur lui. La règle du cours est « une fois sur dix » : remplacé par un tirage à 10 %. Fréquence de D mesurée sur 20 000 tours : 10,2 %.
3. Graine non fixée par défaut (`--seed` valait `None`) alors que le protocole annonce `0xDEADBEEF` : résultats non rejouables, ce que l'énoncé interdit. La valeur par défaut est maintenant fixée à `0xDEADBEEF`.
4. Population non paramétrable. Les stratégies ajoutées à l'étape 2 étaient mélangées au tournoi de l'étape 1. Ajout de l'option `-P course|extended`.
5. Le bruit n'avait aucun effet.
   - Symptôme : avec 50 % de bruit, All-C contre All-C faisait encore exactement 600 / 600 points.
   - Cause : `Game.play_round` ignorait la valeur renvoyée par `apply`, qui contient le coup bruité. Les gains et l'adversaire utilisaient `last_move`, qui garde le coup voulu.
   - Correction : les stratégies ne renvoient plus le coup bruité mais l'assignent à `self.last_move`, et `Game` lit l'attribut. Après correction, 482 / 507 points avec 50 % de bruit. Toute observation sur le bruit faite avant cette correction est donc invalide.
6. Horizon : parties vides et score faussé.
   - Symptôme : avec un horizon de 50 %, 985 parties sur 2 000 duraient 0 tour.
   - Cause : le test d'arrêt avait lieu avant le tour 0.
   - Correction : le test a lieu après chaque tour, donc au moins un tour est joué. De plus, `results()` divisait par le nombre nominal de tours (`parties × tours × (n − 1)`), ce qui sous-estime les scores dès que les parties sont raccourcies. Le programme divise maintenant par les tours réellement joués. Longueur moyenne vérifiée : 201 tours pour `-z 0.5` (attendu 200).

## Arborescence du projet

```
Projet 2/
├── game.py
├── main.py         point d'entrée
├── README.md       README + Journal de bord
├── strategy.py
├── tournament.py
└── utils.py        fonctions seed et random
```
