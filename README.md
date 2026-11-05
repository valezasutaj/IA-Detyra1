# Detyra e parë semestrale – Teknikat e painformuara të kërkimit

Lënda: Inteligjenca Artificiale
Studentja: Valëza Sutaj

Të gjitha programet janë në Python 3 (i kam testuar me 3.12) dhe nuk përdorin asnjë librari
jashtë standardit. Çdo detyrë ka skedarin e vet:

| Detyra | Skedari | Si ekzekutohet |
|---|---|---|
| 1. Social Golfers | `social_golfers.py` | `python social_golfers.py` (instanca 8x4, provon w = 1, 2, ...), `python social_golfers.py 4 3 4` (instancë konkrete g p w), `python social_golfers.py landscape` |
| 2. Sudoku | `sudoku.py` | `python sudoku.py` (të tri nivelet), `python sudoku.py hard`, `python sudoku.py landscape` |
| 3. Latin Square | `latin_square.py` | `python latin_square.py 5`, `python latin_square.py 5 full`, `python latin_square.py landscape` |
| 4. Search Trees | `search_trees.py` | `python search_trees.py` ose `python search_trees.py mc 3` |

Të gjitha rezultatet më poshtë janë të marra nga ekzekutimi i këtyre programeve në laptopin tim,
kohët janë përafërsisht.

---

## 1. Social Golfers Problem

### Modelimi

Kemi n = g · p lojtarë (në instancën e detyrës g = 8 grupe, p = 4 lojtarë, pra n = 32). Çdo javë
lojtarët ndahen në g grupe me nga p lojtarë. Kërkohet një orar për w javë ku asnjë çift lojtarësh
nuk bie në të njëjtin grup më shumë se një herë.

Para se të kërkojmë diçka vlen të shihet sa javë janë fare të mundshme. Çdo javë një lojtar
takon p − 1 = 3 lojtarë të rinj, dhe gjithsej ka n − 1 = 31 lojtarë të tjerë, pra

    w ≤ (n − 1) / (p − 1) = 31 / 3 = 10.33  →  maksimumi 10 javë.

Dihet nga literatura se orari me 10 javë ekziston për 32 lojtarë, por ai është gjetur me metoda
shumë më të fuqishme se DFS-ja e thjeshtë (me symmetry breaking të avancuar dhe constraint
programming). Në pjesën e rezultateve shihet se ku arrin programi im.

### Reprezentimi

- **Variablat:** për çdo javë w dhe çdo lojtar i, x<sub>w,i</sub> = grupi në të cilin luan lojtari i
  në javën w. Gjithsej w · n variabla (për 10 javë: 320).
- **Domeni:** x<sub>w,i</sub> ∈ {0, 1, ..., g − 1}.
- **Kufizimet (hard constraints):**
  1. çdo grup ka saktësisht p lojtarë: |{ i : x<sub>w,i</sub> = k }| = p për çdo javë w dhe grup k
  2. dy lojtarë luajnë bashkë më së shumti një herë: për çdo çift i < j,
     |{ w : x<sub>w,i</sub> = x<sub>w,j</sub> }| ≤ 1

Në program nuk e mbaj matricën x drejtpërdrejt, por listën e grupeve për çdo javë
(`schedule[w][k]` = lista e lojtarëve), sepse kështu kufizimi 1 plotësohet automatikisht gjatë
ndërtimit. Përveç kësaj mbaj një matricë `met[i][j]` (a kanë luajtur i dhe j bashkë deri tani) që
kufizimi 2 të kontrollohet në O(p) kur shtohet një lojtar në grup.

### Objective function

    f(S) = Σ_{i<j} max(0, takime(i, j) − 1)  +  Σ_{w,k} | |G_{w,k}| − p |

ku takime(i, j) është numri i javëve kur i dhe j janë në të njëjtin grup dhe G<sub>w,k</sub> grupi k i
javës w. Termi i parë numëron sa herë "tepër" janë takuar çiftet, i dyti shkeljet e madhësisë së
grupeve. Orari është valid kur f(S) = 0, pra ky është problem kënaqshmërie (satisfaction) dhe f
përdoret vetëm për të matur sa larg jemi nga zgjidhja. Në DFS termi i dytë është gjithmonë 0 sepse
grupet ndërtohen me saktësisht p lojtarë.

### Landscape

Hapësira e kërkimit: në një javë n lojtarë ndahen në g grupe nga p lojtarë (grupet nuk kanë
renditje), pra

    N_javë = n! / ((p!)^g · g!)

dhe për w javë N<sub>javë</sub><sup>w</sup>. Për instancën e detyrës:

| | |
|---|---|
| ndarje të mundshme për një javë (32 lojtarë, 8 grupe nga 4) | 59 287 247 761 257 140 625 ≈ 5.9 · 10<sup>19</sup> |
| w = 2 | ≈ 3.5 · 10<sup>39</sup> |
| w = 5 | ≈ 7.3 · 10<sup>98</sup> |
| w = 10 | ≈ 5.4 · 10<sup>197</sup> |

Për instancat e mëdha nuk mund të llogaritet asgjë tjetër përveç madhësisë, prandaj landscape-in e
kam llogaritur plotësisht për disa instanca të vogla (`python social_golfers.py landscape`), duke
i numëruar të gjitha gjendjet dhe vlerën e f për secilën:

```
======================================================================
LANDSCAPE  g = 3 grupe, p = 2 lojtare/grup, w = 3 jave  (n = 6 lojtare)
======================================================================
  ndarje te mundshme per nje jave   : 15
  gjendje gjithsej (15^3)           : 3375

    f   | gjendje  |   %
  ------+----------+--------
     0  |      480 |  14.22   <- zgjidhjet
     1  |     1080 |  32.00
     2  |     1170 |  34.67
     3  |      360 |  10.67
     4  |      270 |   8.00
     6  |       15 |   0.44

======================================================================
LANDSCAPE  g = 3 grupe, p = 2 lojtare/grup, w = 4 jave  (n = 6 lojtare)
======================================================================
  ndarje te mundshme per nje jave   : 15
  gjendje gjithsej (15^4)           : 50625

    f   | gjendje  |   %
  ------+----------+--------
     0  |      720 |   1.42   <- zgjidhjet
     1  |     4320 |   8.53
     2  |     9720 |  19.20
     3  |    18720 |  36.98
     4  |     8640 |  17.07
     5  |     7020 |  13.87
     6  |      840 |   1.66
     7  |      630 |   1.24
     9  |       15 |   0.03
```

Vërehet që me rritjen e w pjesa e zgjidhjeve bie shumë shpejt (14.2% për w=3, 1.4% për w=4, për w=5
në këtë instancë mbesin vetëm 720 zgjidhje nga 759 375 gjendje, ~0.1%). Shumica e gjendjeve kanë f
të vogël (1–3), pra landscape-i është shumë "i rrafshët" – ka plato të mëdha me të njëjtën vlerë
të f dhe pak vlera të ndryshme, që do ta bënte të vështirë edhe një local search.

### DFS me backtracking

Pema e kërkimit ndërtohet lojtar pas lojtari: java 0 grupi 0 vendi 0, pastaj vendi 1, ..., pastaj
grupi 1, dhe kur mbushet java kalohet në javën tjetër. Një nyje e pemës është orari i pjesshëm
deri në atë moment. Në çdo nyje provohen lojtarët që janë ende të lirë atë javë; ata që kanë
luajtur me ndonjë nga lojtarët e grupit aktual priten menjëherë (pruning) dhe nuk zgjerohen.
Kur për një vend nuk mbetet asnjë lojtar i pranueshëm kthehemi prapa (backtracking) te vendi i
mëparshëm dhe provojmë lojtarin tjetër.

Pa asgjë tjetër pema do të ishte e padurueshme, sepse e njëjta javë mund të shkruhet në shumë
mënyra (renditja e lojtarëve në grup, renditja e grupeve, renditja e javëve). Prandaj kam përdorur
disa rregulla të thjeshta për thyerjen e simetrisë:

- lojtarët brenda grupit mbahen në rend rritës (provohen vetëm lojtarë më të mëdhenj se i fundit),
- grupi i ri fillon gjithmonë me lojtarin më të vogël që ka mbetur pa grup atë javë (kështu
  grupet e një jave dalin të renditura sipas lojtarit të parë),
- java e parë fiksohet: {0,1,2,3}, {4,5,6,7}, ..., {28,29,30,31}.

### Rezultatet

`python social_golfers.py` e provon instancën 8 × 4 për w = 1, 2, 3, ... me limit 60 sekonda për
secilën:

```
======================================================================
SOCIAL GOLFERS  32 lojtare, 8 grupe x 4 lojtare  (DFS me backtracking)
======================================================================
  Provohen w = 1, 2, 3, ... jave, me se shumti 60 s per secilen.

   jave | rezultati          |      nyje |    koha
  ------+--------------------+-----------+---------
      1 | OK                 |         0 |   0.00 s
      2 | OK                 |        24 |   0.00 s
      3 | OK                 |        48 |   0.00 s
      4 | OK                 |        72 |   0.00 s
      5 | OK                 |        96 |   0.00 s
      6 | kohe e tejkaluar   |   2819378 |  60.00 s

  Kufiri teorik: cdo jave nje lojtar takon 3 lojtare te rinj nga 31 gjithsej,
  pra me se shumti 10 jave.

======================================================================
ORARI ME I GJATE I GJETUR: 5 jave
======================================================================
          Grupi 1        Grupi 2        Grupi 3        Grupi 4        Grupi 5        Grupi 6        Grupi 7        Grupi 8
  Java  1  [ 0, 1, 2, 3]  [ 4, 5, 6, 7]  [ 8, 9,10,11]  [12,13,14,15]  [16,17,18,19]  [20,21,22,23]  [24,25,26,27]  [28,29,30,31]
  Java  2  [ 0, 4, 8,12]  [ 1, 5, 9,13]  [ 2, 6,10,14]  [ 3, 7,11,15]  [16,20,24,28]  [17,21,25,29]  [18,22,26,30]  [19,23,27,31]
  Java  3  [ 0, 5,10,15]  [ 1, 4,11,14]  [ 2, 7, 8,13]  [ 3, 6, 9,12]  [16,21,26,31]  [17,20,27,30]  [18,23,24,29]  [19,22,25,28]
  Java  4  [ 0, 6,11,13]  [ 1, 7,10,12]  [ 2, 4, 9,15]  [ 3, 5, 8,14]  [16,22,27,29]  [17,23,26,28]  [18,20,25,31]  [19,21,24,30]
  Java  5  [ 0, 7, 9,14]  [ 1, 6, 8,15]  [ 2, 5,11,12]  [ 3, 4,10,13]  [16,23,25,30]  [17,22,24,31]  [18,21,27,28]  [19,20,26,29]

  Kontrolli: f = 0  ->  asnje cift lojtaresh nuk luan dy here ne te njejtin grup
```

Deri në 5 javë zgjidhja gjendet menjëherë dhe pa asnjë kthim prapa – 24 nyje për javë janë
saktësisht 8 grupe × 3 vende (vendi i parë i grupit është i detyruar), pra zgjedhja e parë e
lejuar ka qenë gjithmonë e mirë. Për w = 6 programi nuk mbaron: me 60 s i viziton rreth 3 milionë
nyje (numri ndryshon pak nga ekzekutimi në ekzekutim varësisht sa i zënë është kompjuteri), dhe e
lashë edhe 9 minuta (33.6 milionë nyje) pa rezultat.

Arsyeja shihet nga orari i mësipërm: DFS-ja, duke marrë gjithmonë lojtarin më të vogël, i ndan
lojtarët në dy gjysma (0–15 dhe 16–31) që nuk përzihen asnjëherë. Brenda 16 lojtarëve me grupe nga
4 mund të luhen maksimumi 15 / 3 = 5 javë, pra pas javës 5 ky orar nuk mund të zgjatet dhe gabimi
është bërë qysh në javën 2. Backtracking-u kronologjik i DFS-së i prish së pari vendimet e fundit
(të gjitha kombinimet e javëve 5, 4 dhe 3) para se të prekë javën 2, dhe kjo nënpemë është
gjigante. Kjo është pikërisht dobësia e njohur e DFS-së: shkon shumë thellë në një degë të gabuar
dhe nuk ka asnjë informatë që ta nxjerrë prej aty.

Pra përgjigja praktike e programit tim për pyetjen "për sa javë mund të luajnë" është 5 javë me
DFS të thjeshtë, kufiri teorik është 10 dhe dihet se 10 arrihet. Për instanca më të vogla DFS-ja
e gjen edhe orarin maksimal, p.sh. `python social_golfers.py 3 2 5` (6 lojtarë në çifte, 5 javë =
maksimumi) ose `4 3 4` (12 lojtarë në treshe, 4 javë = maksimumi) zgjidhen me 15 dhe 295 nyje.

---

## 2. Sudoku Solver

### Modelimi

Tabela 9 × 9 ndahet në 9 rreshta, 9 kolona dhe 9 blloqe 3 × 3 (gjithsej 27 "njësi"). Disa qeli
janë të dhëna, të tjerat duhet të mbushen me shifra 1–9 ashtu që në asnjë njësi të mos përsëritet
ndonjë shifër. Programi ka tri enigma të vendosura brenda (`PUZZLES`): easy me 32 të dhëna,
medium me 28 dhe hard me 21 (kjo e fundit është një nga enigmat që qarkullon si "më e vështira").

### Reprezentimi

- **Variablat:** x<sub>r,c</sub> për r, c ∈ {0..8}, gjithsej 81 variabla. Në program tabela është
  listë me 81 elemente, indeksi i = 9r + c, 0 do të thotë qeli e zbrazët.
- **Domeni:** {1, ..., 9}; për qelitë e dhëna domeni ka vetëm një vlerë.
- **Kufizimet:** all-different për çdo rresht, kolonë dhe bllok. Si kufizime binare: çdo qeli ka
  20 "fqinjë" (8 në rresht, 8 në kolonë, 4 të tjera në bllok), pra 81 · 20 / 2 = 810 kufizime
  x<sub>i</sub> ≠ x<sub>j</sub>.

### Objective function

    f(x) = Σ_{njësi u} ( numri i qelive të mbushura në u − numri i vlerave të ndryshme në u )

pra numri i konflikteve (vlerave të përsëritura) nëpër rreshta, kolona dhe blloqe. Zgjidhja:
të gjitha 81 qelitë të mbushura dhe f(x) = 0. Në kod është funksioni `objective(board)` dhe
përdoret për goal test dhe për landscape.

### Landscape

Nëse e qelitë janë të zbrazëta, hapësira e kërkimit është 9<sup>e</sup>:

| niveli | të dhëna | të zbrazëta | hapësira |
|---|---|---|---|
| easy | 32 | 49 | 9<sup>49</sup> ≈ 5.7 · 10<sup>46</sup> |
| medium | 28 | 53 | 9<sup>53</sup> ≈ 3.8 · 10<sup>50</sup> |
| hard | 21 | 60 | 9<sup>60</sup> ≈ 1.8 · 10<sup>57</sup> |

Secila nga këto enigma ka saktësisht një zgjidhje, pra një gjendje me f = 0 në gjithë atë
hapësirë. (Për krahasim, tabela e zbrazët ka 9<sup>81</sup> ≈ 2 · 10<sup>77</sup> mbushje nga të cilat
rreth 6.7 · 10<sup>21</sup> janë sudoku valide.)

Meqë nuk numërohen dot të gjitha, landscape-in e kam vlerësuar me mostër: qelitë e zbrazëta
mbushen me vlera të rastit 100 000 herë dhe shikohet shpërndarja e f
(`python sudoku.py landscape`):

| niveli | f minimal | f maksimal | f mesatar | vlerat më të shpeshta |
|---|---|---|---|---|
| easy | 51 | 101 | 74.8 | 73–77 (rreth 7% secila) |
| medium | 53 | 99 | 77.2 | 75–79 |
| hard | 59 | 103 | 81.3 | 79–83 |

Një mbushje e rastësishme ka mesatarisht 75–80 konflikte dhe në 100 000 mostra asnjëherë nuk zbret
nën 50, kurse zgjidhja e vetme ka 0. Landscape-i i plotë është pra shumë i ashpër me një "pus"
të vetëm. Megjithatë për kërkimin në pemë kjo nuk ka rëndësi, sepse pema ndërtohet vetëm me
caktime konsistente (f = 0 në çdo nyje) dhe thjesht thellohet derisa mbushet tabela.

### BFS me backtracking

- **Nyja** e pemës = tabelë pjesërisht e mbushur. Rrënja = enigma. Niveli d i pemës përmban
  tabelat ku kërkimi ka mbushur d qeli, pra zgjidhja është gjithmonë në nivelin e (numri i qelive
  të zbrazëta).
- **Fëmijët** e një nyje: zgjedhet një qeli e zbrazët dhe për çdo vlerë që nuk bie në konflikt me
  rreshtin, kolonën dhe bllokun krijohet një tabelë e re. Vlerat në konflikt priten që në gjenerim.
  Nëse qelia e zgjedhur nuk ka asnjë vlerë të mundshme nyja është dead end dhe hidhet.
- **BFS**: nyjet mbahen në radhë FIFO (`deque`), merret gjithmonë e para, fëmijët shtohen në fund.
  Kështu pema zgjerohet nivel pas niveli. "Backtracking" në BFS nuk është kthim prapa në kuptimin
  klasik (nuk ka asnjë rrugë aktive), por prerja e degëve joproduktive – dega vdes dhe nuk zgjerohet
  më, kurse degët tjera të të njëjtit nivel vazhdojnë.

Një gjë që më duhej ta ndryshoja: në fillim e zgjidhja thjesht qelinë e parë të zbrazët, dhe te
niveli hard radha rritej aq shumë sa mbaronte memoria (BFS-ja e mban gjithë nivelin në memorie).
Prandaj zgjedh qelinë me më pak kandidatë (nëse ka qeli me 1 kandidat, ajo merret direkt). Kjo nuk
e ndryshon faktin që kërkimi është i painformuar – nuk ka asnjë vlerësim se cila tabelë është
"më afër" zgjidhjes – vetëm e bën pemën shumë më të ngushtë.

### Rezultatet

`python sudoku.py`:

```
=== EASY ===                          === MEDIUM ===                        === HARD ===
. . 3 | . 2 . | 6 . .                 . . . | . . . | 9 . 7                 8 . . | . . . | . . .
9 . . | 3 . 5 | . . 1                 . . . | 4 2 . | 1 8 .                 . . 3 | 6 . . | . . .
. . 1 | 8 . 6 | 4 . .                 . . . | 7 . 5 | . 2 6                 . 7 . | . 9 . | 2 . .
------+-------+------                 ------+-------+------                 ------+-------+------
. . 8 | 1 . 2 | 9 . .                 1 . . | 9 . 4 | . . .                 . 5 . | . . 7 | . . .
7 . . | . . . | . . 8                 . 5 . | . . . | . 4 .                 . . . | . 4 5 | 7 . .
. . 6 | 7 . 8 | 2 . .                 . . . | 5 . 7 | . . 9                 . . . | 1 . . | . 3 .
------+-------+------                 ------+-------+------                 ------+-------+------
. . 2 | 6 . 9 | 5 . .                 9 2 . | 1 . 8 | . . .                 . . 1 | . . . | . 6 8
8 . . | 2 . 3 | . . 9                 . 3 4 | . 5 9 | . . .                 . . 8 | 5 . . | . 1 .
. . 5 | . 1 . | 3 . .                 5 . 7 | . . . | . . .                 . 9 . | . . . | 4 . .

4 8 3 | 9 2 1 | 6 5 7                 4 6 2 | 8 3 1 | 9 5 7                 8 1 2 | 7 5 3 | 6 4 9
9 6 7 | 3 4 5 | 8 2 1                 7 9 5 | 4 2 6 | 1 8 3                 9 4 3 | 6 8 2 | 1 7 5
2 5 1 | 8 7 6 | 4 9 3                 3 8 1 | 7 9 5 | 4 2 6                 6 7 5 | 4 9 1 | 2 8 3
------+-------+------                 ------+-------+------                 ------+-------+------
5 4 8 | 1 3 2 | 9 7 6                 1 7 3 | 9 8 4 | 2 6 5                 1 5 4 | 2 3 7 | 8 9 6
7 2 9 | 5 6 4 | 1 3 8                 6 5 9 | 3 1 2 | 7 4 8                 3 6 9 | 8 4 5 | 7 2 1
1 3 6 | 7 9 8 | 2 4 5                 2 4 8 | 5 6 7 | 3 1 9                 2 8 7 | 1 6 9 | 5 3 4
------+-------+------                 ------+-------+------                 ------+-------+------
3 7 2 | 6 8 9 | 5 1 4                 9 2 6 | 1 7 8 | 5 3 4                 5 2 1 | 9 7 4 | 3 6 8
8 1 4 | 2 5 3 | 7 6 9                 8 3 4 | 2 5 9 | 6 7 1                 4 3 8 | 5 2 6 | 9 1 7
6 9 5 | 4 1 7 | 3 8 2                 5 1 7 | 6 4 3 | 8 9 2                 7 9 6 | 3 1 8 | 4 5 2
```

| niveli | nyje të zgjeruara | radha max | thellësia e zgjidhjes | koha |
|---|---|---|---|---|
| easy | 50 | 1 | 49 | 0.002 s |
| medium | 206 | 9 | 53 | 0.007 s |
| hard | 24 881 | 1 003 | 60 | 1.2 s |

Te easy në çdo nivel ka pasur saktësisht një nyje – gjithmonë ekzistonte një qeli me një kandidat
të vetëm, pra enigma zgjidhet pa asnjë degëzim. Te medium pema ka maksimum 9 nyje në një nivel.
Te hard pema zgjerohet vërtet: numri i nyjeve për nivel rritet deri te ~1000 rreth nivelit 27 dhe
pastaj bie (degët vdesin), dhe në nivelin 60 mbetet një nyje e vetme, zgjidhja:

```
  Nyje per nivel te pemes (nivel = sa qeli ka mbushur kerkimi):
    nivel  0- 9:     1     2     4     8    12    19    32    56    90   130
    nivel 10-19:   165   218   278   339   412   507   587   655   738   791
    nivel 20-29:   841   874   932   940   963   957   966  1003   995  1000
    nivel 30-39:   959   933   930   865   814   786   716   627   535   477
    nivel 40-49:   427   374   324   288   255   228   189   161   129    95
    nivel 50-59:    82    57    45    31    24     8     3     1     1     1
    nivel 60-60:     1
```

Meqë zgjidhja është gjithmonë në nivelin më të thellë, BFS-ja në fakt e viziton gjithë pemën
(24 881 nyje) para se ta gjejë. Një DFS me të njëjtën prerje do të kishte në memorie vetëm rrugën
aktuale (60 nyje) dhe shpesh do ta gjente zgjidhjen më herët. Avantazhi i BFS-së – që e gjen
zgjidhjen më të cekët – këtu nuk vlen asgjë sepse të gjitha zgjidhjet janë në të njëjtën thellësi.

---

## 3. Latin Square

### Modelimi

Katrori latin i rendit n: grid n × n me vlerat 1..n, çdo vlerë saktësisht një herë në çdo rresht
dhe çdo kolonë. Praktikisht është një Sudoku pa blloqe dhe pa qeli të dhëna.

### Reprezentimi

- **Variablat:** x<sub>r,c</sub>, r, c ∈ {0..n−1}, gjithsej n² variabla.
- **Domeni:** {1, ..., n}.
- **Kufizimet:** all-different për çdo rresht dhe çdo kolonë (2n kufizime all-different, ose
  n² · (n − 1) kufizime binare ≠).

### Objective function

    f(x) = Σ_r (qeli të mbushura në rreshtin r − vlera të ndryshme në rreshtin r)
         + Σ_c (qeli të mbushura në kolonën c − vlera të ndryshme në kolonën c)

d.m.th. numri i vlerave të përsëritura nëpër rreshta dhe kolona. f = 0 me të gjitha qelitë e
mbushura ⇔ katror latin.

### Landscape

Hapësira e kërkimit është n<sup>n²</sup> (n = 5: 5<sup>25</sup> ≈ 3 · 10<sup>17</sup>, n = 7: 7<sup>49</sup> ≈ 2.6 · 10<sup>41</sup>).
Numri i katrorëve latinë (zgjidhjeve) është i njohur: L(3) = 12, L(4) = 576, L(5) = 161 280,
L(6) = 812 851 200, L(7) ≈ 6.1 · 10<sup>13</sup>. Për n = 2 dhe n = 3 i kam numëruar të gjitha gjendjet
(`python latin_square.py landscape`):

```
======================================================================
LANDSCAPE  n = 2  (2^4 = 16 mbushje te plota)
======================================================================
    f   | gjendje  |   %
  ------+----------+--------
     0  |        2 |  12.50   <- katroret latine
     2  |       12 |  75.00
     4  |        2 |  12.50

======================================================================
LANDSCAPE  n = 3  (3^9 = 19683 mbushje te plota)
======================================================================
    f   | gjendje  |   %
  ------+----------+--------
     0  |       12 |   0.06   <- katroret latine
     2  |      540 |   2.74
     3  |      936 |   4.76
     4  |     4050 |  20.58
     5  |     4752 |  24.14
     6  |     6006 |  30.51
     7  |     2268 |  11.52
     8  |      918 |   4.66
     9  |      144 |   0.73
    10  |       54 |   0.27
    12  |        3 |   0.02
```

Vlera f = 1 nuk shfaqet fare: nëse një vlerë përsëritet në një rresht, atëherë një vlerë tjetër
mungon në atë rresht dhe duhet të jetë e përsëritur diku në një kolonë – konfliktet vijnë gjithmonë
së paku në çifte. Zgjidhjet janë 12 nga 19 683 (0.06%) dhe shumica e gjendjeve janë rreth f = 5–6.

### IDDFS dhe backtracking

Qelitë mbushen me radhë rresht pas rreshti, thellësia e nyjes = numri i qelive të mbushura, në
çdo qeli provohen vlerat 1..n që nuk janë në rreshtin/kolonën përkatëse (vlerat e përdorura mbahen
si bitmask për çdo rresht dhe kolonë).

**Backtracking (DFS):** kur për një qeli asnjë vlerë nuk është e lejuar, kthehemi te qelia e
mëparshme dhe provojmë vlerën tjetër. Mbaron kur mbushen të gjitha n² qelitë.

**IDDFS:** depth-limited search `dls(depth, limit)` që mbush më së shumti `limit` qeli; kur
`depth == limit` kthen cutoff, kur `depth == n²` bën goal test (f = 0). Pastaj `iddfs()` e thërret
me limit = 0, 1, 2, ..., n². Rezultati i vërtetë (katrori) del vetëm në iteracionin limit = n².

### Rezultatet

`python latin_square.py 5`:

```
======================================================================
LATIN SQUARE  n = 5   (hapesira e kerkimit 5^25 ~ 2.98e+17)
======================================================================

  1) Backtracking (DFS)

      1  2  3  4  5
      2  1  4  5  3
      3  4  5  1  2
      4  5  2  3  1
      5  3  1  2  4

  Kontrolli : f = 0  (katror latin valid)
  nyje      : 37
  koha      : 0.001 s

  2) IDDFS - rreshti dhe kolona e pare te fiksuara ne 1..n

      1  2  3  4  5
      2  1  4  5  3
      3  4  5  1  2
      4  5  2  3  1
      5  3  1  2  4

  Kontrolli : f = 0  (katror latin valid)
  iteracione: 26  (limit = 0 .. 25)
  nyje      : 5805 gjithsej
  koha      : 0.026 s

  Nyje te vizituara ne cdo iteracion (limit -> nyje):
     0 ->        0   1 ->        0   2 ->        0   3 ->        0   4 ->        0   5 ->        0   6 ->        0
     7 ->        4   8 ->       13   9 ->       27  10 ->       38  11 ->       38  12 ->       63  13 ->      124
    14 ->      200  15 ->      246  16 ->      246  17 ->      322  18 ->      432  19 ->      568  20 ->      624
    21 ->      624  22 ->      680  23 ->      736  24 ->      792  25 ->       28
```

Katrori që del nuk është i njëjti me shembullin e detyrës (ai është zhvendosja ciklike), por është
katrori latin leksikografikisht i pari – programi e gjen të parin që e lejon kërkimi, dhe të dy janë
valide. Shembulli i detyrës do të mund të prodhohej edhe direkt me formulën x<sub>r,c</sub> = ((c − r) mod n) + 1,
por atëherë s'do të kishte kërkim fare.

Krahasimi i dy metodave (nyjet e vizituara):

| n | backtracking | IDDFS (pa fiksim) | IDDFS (rreshti + kolona e parë fiks) |
|---|---|---|---|
| 4 | 16 | 24 844 (0.05 s) | – |
| 5 | 37 | 13 505 897 (53 s) | 5 805 (0.015 s) |
| 6 | 62 | – | 1 367 450 (4.3 s) |
| 7 | 131 | – | kohë e tejkaluar (2 min, 25.6 milionë nyje, arriti vetëm te limit = 29 nga 49) |

Backtracking-u i thjeshtë e gjen katrorin pothuajse pa kthim prapa (n = 5: 25 qeli, 37 nyje). IDDFS
është katastrofë për këtë problem dhe kjo është pak a shumë e pritur: të gjitha zgjidhjet janë në
thellësinë n² dhe ne e dimë këtë paraprakisht, prandaj iteracionet me limit < n² s'mund të gjejnë
kurrë asgjë – ato thjesht e eksplorojnë gjithë pemën deri në atë thellësi (çdo mbushje e pjesshme
pa konflikt) dhe pastaj e përsërisin punën në iteracionin tjetër. Numri i mbushjeve të pjesshme
rritet eksponencialisht me limitin (shih kolonën "nyje per iteracion"), dhe iteracioni i fundit,
i vetmi i dobishëm, ka vetëm 28–37 nyje. IDDFS ka kuptim kur thellësia e zgjidhjes nuk dihet dhe
duam memorien e DFS-së me garancinë e BFS-së për zgjidhjen më të cekët – asnjëra nga këto nuk vlen
te katrori latin.

Që IDDFS të punojë së paku për n = 5 dhe 6 në kohë të arsyeshme, në versionin default e fiksoj
rreshtin dhe kolonën e parë në 1..n (katror latin i reduktuar). Çdo katror latin mund të sillet
në këtë formë me riemërtim të vlerave dhe permutim të rreshtave, pra nuk humbet asnjë zgjidhje,
vetëm pema zvogëlohet shumë. Me `python latin_square.py 5 full` ekzekutohet IDDFS-ja pa këtë
fiksim (53 sekonda për n = 5).

---

## 4. Search Trees

Pemët i kam ndërtuar me programin `search_trees.py` i cili për secilin problem ka funksionin e
gjendjes pasardhëse dhe e printon pemën deri në një thellësi të dhënë. Gjendjet jovalide shënohen me
`X` dhe gjendjet që janë shfaqur më herët në të njëjtën rrugë shënohen `(perseritje)`; asnjëra nuk
zgjerohet më tej. Numrat "nyje per nivel" i numërojnë edhe këto.

### 4.1 8-Puzzle

- **Gjendja:** vektor me 9 vlera (pozita e 8 pllakave dhe e vendit të zbrazët `_`).
- **Veprimet:** lëvizja e vendit të zbrazët lart/poshtë/majtas/djathtas (U/D/L/R). Në cep ka 2
  veprime, në mes të anës 3, në qendër 4 – faktori i degëzimit është 2–4 (mesatarisht rreth 2.67).
- **Hapësira e gjendjeve:** 9! = 362 880 renditje, por vetëm gjysma, 181 440, arrihen nga një
  gjendje fillestare (paritet).
- **Gjendja fillestare** e marrë: `1 2 3 / 4 _ 6 / 7 5 8`, goal `1 2 3 / 4 5 6 / 7 8 _`.

Pema deri në thellësi 2 (`python search_trees.py puzzle 2`):

```
1 2 3
4 _ 6
7 5 8
|-- U: 1 _ 3
|   4 2 6
|   7 5 8
|   |-- D: 1 2 3  (perseritje)
|   |   4 _ 6
|   |   7 5 8
|   |-- L: _ 1 3
|   |   4 2 6
|   |   7 5 8
|   `-- R: 1 3 _
|       4 2 6
|       7 5 8
|-- D: 1 2 3
|   4 5 6
|   7 _ 8
|   |-- U: 1 2 3  (perseritje)
|   |   4 _ 6
|   |   7 5 8
|   |-- L: 1 2 3
|   |   4 5 6
|   |   _ 7 8
|   `-- R: 1 2 3  <-- GOAL
|       4 5 6
|       7 8 _
|-- L: 1 2 3
|   _ 4 6
|   7 5 8
|   |-- U: _ 2 3
|   |   1 4 6
|   |   7 5 8
|   |-- D: 1 2 3
|   |   7 4 6
|   |   _ 5 8
|   `-- R: 1 2 3  (perseritje)
|       4 _ 6
|       7 5 8
`-- R: 1 2 3
    4 6 _
    7 5 8
    |-- U: 1 2 _
    |   4 6 3
    |   7 5 8
    |-- D: 1 2 3
    |   4 6 8
    |   7 5 _
    `-- L: 1 2 3  (perseritje)
        4 _ 6
        7 5 8

  Nyje per nivel: thellesia 0: 1, thellesia 1: 4, thellesia 2: 12   (gjithsej 17)
```

Nga rrënja ka 4 veprime, dhe çdo fëmijë ka 3 ose 4 fëmijë nga të cilët një është gjithmonë kthimi
në gjendjen e prindit (përsëritje). Zgjidhja është në thellësi 2 (D pastaj R): BFS-ja do ta gjente
sapo të zgjeronte nyjen D (pas rrënjës dhe nyjes U), kurse DFS-ja me renditjen U, D, L, R do të
humbej në degën U dhe pa kontrollin e përsëritjeve nuk do të kthehej kurrë.

### 4.2 Missionaries and Cannibals

- **Gjendja:** (M, C, B) – sa misionarë dhe sa kanibalë janë në bregun e majtë dhe në cilën anë
  është barka. Fillimi (3, 3, majtas), goal (0, 0, djathtas).
- **Veprimet:** barka bart 1 ose 2 persona: 1M, 2M, 1C, 2C, 1M1C – 5 veprime në çdo gjendje.
- **Kufizimi:** në asnjë breg kanibalët nuk guxojnë të jenë më shumë se misionarët nëse aty ka
  misionarë. Nga 4 · 4 · 2 = 32 kombinime vetëm 20 janë gjendje valide.

Pema deri në thellësi 3 (`python search_trees.py mc 3`):

```
(3M,3C,majtas)
|-- 1M0C: (2M,3C,djathtas)  X (jovalide)
|-- 2M0C: (1M,3C,djathtas)  X (jovalide)
|-- 0M1C: (3M,2C,djathtas)
|   `-- 0M1C: (3M,3C,majtas)  (perseritje)
|-- 0M2C: (3M,1C,djathtas)
|   |-- 0M1C: (3M,2C,majtas)
|   |   |-- 1M0C: (2M,2C,djathtas)
|   |   |-- 2M0C: (1M,2C,djathtas)  X (jovalide)
|   |   |-- 0M1C: (3M,1C,djathtas)  (perseritje)
|   |   |-- 0M2C: (3M,0C,djathtas)
|   |   `-- 1M1C: (2M,1C,djathtas)  X (jovalide)
|   `-- 0M2C: (3M,3C,majtas)  (perseritje)
`-- 1M1C: (2M,2C,djathtas)
    |-- 1M0C: (3M,2C,majtas)
    |   |-- 1M0C: (2M,2C,djathtas)  (perseritje)
    |   |-- 2M0C: (1M,2C,djathtas)  X (jovalide)
    |   |-- 0M1C: (3M,1C,djathtas)
    |   |-- 0M2C: (3M,0C,djathtas)
    |   `-- 1M1C: (2M,1C,djathtas)  X (jovalide)
    |-- 0M1C: (2M,3C,majtas)  X (jovalide)
    `-- 1M1C: (3M,3C,majtas)  (perseritje)

  Nyje per nivel: thellesia 0: 1, thellesia 1: 5, thellesia 2: 6, thellesia 3: 10   (gjithsej 22)
```

Veprimet që do të nxirrnin më shumë persona se sa ka në breg nuk shfaqen fare (p.sh. nga
(3,2,djathtas) në bregun e djathtë ka vetëm 1 kanibal, pra 2C dhe 1M1C nuk ekzistojnë). Vërehet se
sa shumë prej pemës priten nga kufizimi dhe nga përsëritjet: nga 5 degët e rrënjës dy janë
jovalide, dhe në çdo nivel njëra nga lëvizjet e kthen barkën me të njëjtët persona (përsëritje).
Zgjidhja më e shkurtër ka 11 hapa (e gjetur me BFS në program):

```
    hapi  1: (3M,3C,majtas)     --0M2C-->  (3M,1C,djathtas)
    hapi  2: (3M,1C,djathtas)   --0M1C-->  (3M,2C,majtas)
    hapi  3: (3M,2C,majtas)     --0M2C-->  (3M,0C,djathtas)
    hapi  4: (3M,0C,djathtas)   --0M1C-->  (3M,1C,majtas)
    hapi  5: (3M,1C,majtas)     --2M0C-->  (1M,1C,djathtas)
    hapi  6: (1M,1C,djathtas)   --1M1C-->  (2M,2C,majtas)
    hapi  7: (2M,2C,majtas)     --2M0C-->  (0M,2C,djathtas)
    hapi  8: (0M,2C,djathtas)   --0M1C-->  (0M,3C,majtas)
    hapi  9: (0M,3C,majtas)     --0M2C-->  (0M,1C,djathtas)
    hapi 10: (0M,1C,djathtas)   --1M0C-->  (1M,1C,majtas)
    hapi 11: (1M,1C,majtas)     --1M1C-->  (0M,0C,djathtas)
```

### 4.3 Rotating Workforce Scheduling

Problemi: n punëtorë, një periudhë planifikimi prej 7 ditësh, dhe shifts të ndryshme (p.sh. D =
dita, N = nata, `-` = pushim). Orari është rrotullues: ndërtohet një cikël i vetëm prej n javësh,
punëtori 1 e ndjek nga java 1, punëtori 2 fillon nga java 2 e kështu me radhë, pra pas n javësh të
gjithë e kanë kaluar të njëjtin orar. Kërkohet që çdo ditë të mbulohen kërkesat (sa punëtorë për
çdo shift) dhe të respektohen kufizimet mbi sekuencat e shifts.

Instanca që kam marrë (e vogël që pema të vizatohet):

- 4 punëtorë → cikli ka 4 · 7 = 28 pozita
- shifts: D, N, `-`
- kërkesa: çdo ditë të javës saktësisht 1 D dhe 1 N (pra 2 punëtorë pushojnë)
- kufizimet: N nuk guxon të pasohet nga D; më së shumti 5 ditë pune rresht; pushimi zgjat së paku
  2 dhe më së shumti 4 ditë rresht (kufizimet vlejnë edhe në kalimin nga fundi i ciklit në fillim)

(Fillimisht e kisha provuar me 3 punëtorë, por me këto kufizime nuk ka zgjidhje fare – 7 ditët e
pushimit duhet të bien në ditë të ndryshme të javës dhe në blloqe nga ≥ 2, dhe kjo nuk del me
14 ditë pune në blloqe ≤ 5.)

- **Gjendja:** stringu i shifts të caktuara deri tani për pozitat 0, 1, 2, ... të ciklit.
- **Veprimi:** caktimi i shift-it për pozitën e radhës (3 veprime, faktori i degëzimit 3).
- **Hapësira:** 3<sup>28</sup> ≈ 2.3 · 10<sup>13</sup> cikle të mundshme.
- Kërkesa ditore kontrollohet që në caktimet e pjesshme: pozitat d, d+7, d+14, d+21 i takojnë të
  njëjtës ditë të javës, pra sapo dy prej tyre kanë D (ose N, ose tre kanë pushim) dega pritet.

Pema deri në thellësi 3 (`python search_trees.py rws 3`):

```
(zbrazet)
|-- D: "D"
|   |-- D: "DD"
|   |   |-- D: "DDD"
|   |   |-- N: "DDN"
|   |   `-- -: "DD-"
|   |-- N: "DN"
|   |   |-- D: "DND"  X (jovalide)
|   |   |-- N: "DNN"
|   |   `-- -: "DN-"
|   `-- -: "D-"
|       |-- D: "D-D"  X (jovalide)
|       |-- N: "D-N"  X (jovalide)
|       `-- -: "D--"
|-- N: "N"
|   |-- D: "ND"  X (jovalide)
|   |-- N: "NN"
|   |   |-- D: "NND"  X (jovalide)
|   |   |-- N: "NNN"
|   |   `-- -: "NN-"
|   `-- -: "N-"
|       |-- D: "N-D"  X (jovalide)
|       |-- N: "N-N"  X (jovalide)
|       `-- -: "N--"
`-- -: "-"
    |-- D: "-D"
    |   |-- D: "-DD"
    |   |-- N: "-DN"
    |   `-- -: "-D-"
    |-- N: "-N"
    |   |-- D: "-ND"  X (jovalide)
    |   |-- N: "-NN"
    |   `-- -: "-N-"
    `-- -: "--"
        |-- D: "--D"
        |-- N: "--N"
        `-- -: "---"

  Nyje per nivel: thellesia 0: 1, thellesia 1: 3, thellesia 2: 9, thellesia 3: 24   (gjithsej 37)
```

Në tri nivelet e para priten 8 nyje: ato me sekuencën e ndaluar ND dhe ato ku pushimi zgjat vetëm
një ditë (D-D, D-N, N-D, N-N). Kufizimet e kërkesës ditore fillojnë të ndikojnë nga pozita 7 e
tutje. Pema e plotë ka 28 nivele; DFS-ja me backtracking në program e gjen një cikël të plotë pas
93 nyjeve:

```
    "DDDDD--NNN--DD----NNN---N---"

            Hen Mar Mer Enj Pre Sht Die
  Java 1:     D   D   D   D   D   -   -
  Java 2:     N   N   N   -   -   D   D
  Java 3:     -   -   -   -   N   N   N
  Java 4:     -   -   -   N   -   -   -
```

Në çdo kolonë (ditë të javës) ka saktësisht një D dhe një N, nuk ka ND askund (as në kalimin nga
java 4 te java 1), blloqet e punës janë ≤ 5 dhe pushimet 2–4 ditë. Punëtori 1 e punon javën 1 të
tabelës, javën tjetër javën 2, etj.
