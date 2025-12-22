# 📊 Application de Gestion FCP - Documentation Complète

Application web interactive pour l'analyse et la gestion de Fonds Communs de Placement (FCP), développée avec Streamlit.

## 📑 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Installation et Utilisation](#installation-et-utilisation)
3. [Documentation des Onglets](#documentation-des-onglets)
   - [Page d'Accueil](#page-daccueil)
   - [Valeurs Liquidatives](#1-valeurs-liquidatives)
   - [Souscriptions & Rachats](#2-souscriptions--rachats)
   - [Actifs Nets](#3-actifs-nets)
   - [À Propos](#4-à-propos)
4. [Formules et Méthodes de Calcul](#formules-et-méthodes-de-calcul)
5. [Guide Décisionnel](#guide-décisionnel)
6. [Technologies Utilisées](#technologies-utilisées)

---

## 🎯 Vue d'Ensemble

Cette application offre une plateforme complète pour analyser les performances des FCP, gérer les souscriptions/rachats, suivre les actifs nets et générer des rapports détaillés avec visualisations avancées. Elle permet aux gestionnaires de portefeuille, gestionnaires de risque et équipes commerciales de prendre des décisions éclairées basées sur des analyses quantitatives rigoureuses.

### Objectifs Principaux

- **Analyse de Performance** : Évaluer les rendements et la volatilité des fonds
- **Gestion des Risques** : Identifier et quantifier les risques (volatilité, drawdown, VaR)
- **Suivi des Flux** : Analyser les souscriptions et rachats par type de client
- **Suivi des Actifs** : Monitorer l'évolution des actifs nets sous gestion
- **Aide à la Décision** : Fournir des recommandations basées sur des métriques quantitatives

---

## 💻 Installation et Utilisation

### Prérequis

- Python 3.8 ou supérieur
- Fichier de données FCP au format **CSV** ou **Excel (XLSX)**

### Installation

```bash
# Cloner le repository
git clone <repository-url>
cd Application-FCP

# Installer les dépendances
pip install streamlit pandas numpy plotly scikit-learn scipy openpyxl
```

### Démarrage

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Configuration du Fichier de Données

**Format par défaut** : `data_fcp.xlsx`

Pour spécifier un fichier personnalisé :
```bash
# Windows
set FCP_DATA_FILE=chemin/vers/votre/fichier.xlsx

# Linux/Mac
export FCP_DATA_FILE=chemin/vers/votre/fichier.xlsx
```

**Structure attendue du fichier Excel** :
- **Feuille "Valeurs Liquidatives"** : Date, FCP1, FCP2, ...
- **Feuille "Souscriptions Rachats"** : Date, FCP, Opérations, Montant, Type de Client
- **Feuille "Actifs Nets"** : Date, FCP, Montant

---

## 📊 Documentation des Onglets

### Page d'Accueil

La page d'accueil fournit un aperçu général des données et permet de naviguer vers les différentes sections d'analyse.

**Fonctionnalités** :
- Aperçu des données chargées (toutes les feuilles Excel)
- Statistiques globales (nombre de FCP, période couverte)
- Navigation rapide vers les pages d'analyse

---

## 1. 📈 Valeurs Liquidatives

### Vue d'Ensemble

Cette page analyse en profondeur les valeurs liquidatives (VL) des FCP pour évaluer leur performance et leur profil de risque. Elle constitue l'outil principal pour l'analyse quantitative des fonds.

### Sous-Sections

#### 1.1 Performances Calendaires

**Description** : Calcule les performances sur des périodes calendaires standardisées.

**Périodes Calculées** :
- **WTD (Week To Date)** : Performance depuis le début de la semaine en cours
- **MTD (Month To Date)** : Performance depuis le début du mois en cours
- **QTD (Quarter To Date)** : Performance depuis le début du trimestre
- **STD (Semester To Date)** : Performance depuis le début du semestre
- **YTD (Year To Date)** : Performance depuis le début de l'année

**Formule** :
```
Performance(%) = ((VL_fin / VL_début) - 1) × 100
```

**Interprétation** :
- **Positif** : Le fonds a généré un gain sur la période
- **Négatif** : Le fonds a subi une perte sur la période
- **Comparaison** : Permet de comparer les performances entre fonds sur des périodes identiques

**Guide Décisionnel** :
- ✅ Performance > 5% (YTD) : Excellent
- ⚠️ Performance entre 0% et 5% : Satisfaisant
- ❌ Performance < 0% : Attention requise

**Visualisation** : Tableau avec formatage conditionnel (vert pour positif, rouge pour négatif)

#### 1.2 Performances Glissantes

**Description** : Calcule les performances sur des périodes glissantes à partir de la date la plus récente.

**Périodes Calculées** :
- **1M** : Performance sur le dernier mois
- **3M** : Performance sur les 3 derniers mois
- **6M** : Performance sur les 6 derniers mois
- **1Y** : Performance sur la dernière année
- **3Y** : Performance sur les 3 dernières années (annualisée)
- **5Y** : Performance sur les 5 dernières années (annualisée)
- **Origine** : Performance depuis l'origine des données

**Formule pour performances annualisées** :
```
Performance_annualisée(%) = ((VL_fin / VL_début)^(252/n_jours) - 1) × 100
```
où n_jours = nombre de jours de bourse sur la période (252 jours/an)

**Interprétation** :
- Les performances glissantes permettent d'évaluer la consistance dans le temps
- Une performance décroissante sur plusieurs horizons indique une tendance baissière
- Comparer les performances court terme (1M, 3M) vs long terme (3Y, 5Y) révèle la stabilité

**Guide Décisionnel** :
- Performance constamment positive sur tous les horizons → Fonds robuste
- Performance volatile entre périodes → Risque élevé, révision nécessaire
- Performance long terme > court terme → Possibilité de rebond

#### 1.3 Évolution Temporelle

**Description** : Graphique interactif montrant l'évolution des VL dans le temps.

**Fonctionnalités** :
- Sélection multiple de FCP pour comparaison
- Zoom et navigation temporelle
- Rebaser à 100 pour comparaison relative

**Interprétation** :
- **Pente ascendante** : Croissance du fonds
- **Volatilité visuelle** : Amplitude des fluctuations indique le risque
- **Corrélation visuelle** : Fonds qui évoluent ensemble suggèrent une exposition similaire

**Guide Décisionnel** :
- Évolution parallèle entre fonds → Diversification insuffisante
- Tendance à la hausse stable → Candidat pour allocation importante
- Drawdowns fréquents → Limiter l'exposition

#### 1.4 Distributions, Statistiques et Corrélations

##### Distribution des Rendements

**Description** : Histogramme et statistiques des rendements quotidiens.

**Métriques Calculées** :

1. **Moyenne** : Rendement moyen quotidien
   ```
   μ = (1/n) × Σ(rendements)
   ```

2. **Écart-type (Volatilité)** : Mesure de dispersion des rendements
   ```
   σ = √[(1/n) × Σ(rendement - μ)²]
   Volatilité_annualisée = σ × √252
   ```

3. **Skewness (Asymétrie)** : Mesure de l'asymétrie de la distribution
   ```
   Skewness = (1/n) × Σ[(rendement - μ)/σ]³
   ```
   - **> 0** : Queue droite (gains extrêmes plus probables)
   - **= 0** : Distribution symétrique
   - **< 0** : Queue gauche (pertes extrêmes plus probables, risque)

4. **Kurtosis (Aplatissement)** : Mesure de l'épaisseur des queues
   ```
   Kurtosis_excess = [(1/n) × Σ[(rendement - μ)/σ]⁴] - 3
   ```
   - **> 0** : Queues épaisses (événements extrêmes fréquents)
   - **= 0** : Distribution normale
   - **< 0** : Queues fines

**Interprétation** :
- **Skewness positif + Kurtosis faible** : Profil idéal (gains asymétriques, événements extrêmes rares)
- **Skewness négatif + Kurtosis élevé** : Profil risqué (pertes asymétriques, crashs fréquents)

**Guide Décisionnel** :
- Skewness < -0.5 → ⚠️ Attention au risque de queue gauche
- Kurtosis > 3 → ⚠️ Événements extrêmes fréquents, gestion active requise
- Distribution normale → Modèles statistiques classiques applicables

##### Matrice de Corrélation

**Description** : Corrélation entre les rendements des différents FCP.

**Formule** :
```
Corrélation(A, B) = Cov(A, B) / (σ_A × σ_B)
```

**Interprétation** :
- **Proche de 1** : Fonds fortement corrélés (évoluent ensemble)
- **Proche de 0** : Fonds indépendants
- **Proche de -1** : Fonds inversement corrélés (couverture potentielle)

**Guide Décisionnel** :
- Corrélation > 0.8 entre fonds du portefeuille → Redondance, diversification insuffisante
- Corrélation entre 0.3 et 0.6 → Diversification optimale
- Corrélation < 0 → Opportunité de hedging

##### Quartiles et Box Plot

**Description** : Visualisation de la distribution des rendements par quartiles.

**Quartiles** :
- **Q1 (25%)** : 25% des rendements sont inférieurs à cette valeur
- **Q2 (50%, Médiane)** : Point milieu de la distribution
- **Q3 (75%)** : 75% des rendements sont inférieurs à cette valeur
- **IQR (Interquartile Range)** : Q3 - Q1 (dispersion centrale)

**Interprétation** :
- Médiane > Moyenne → Distribution asymétrique vers la gauche (prudence)
- IQR large → Forte dispersion, volatilité élevée
- Outliers fréquents → Événements extrêmes

#### 1.5 Indicateurs de Risque

##### 1.5.1 Volatilité Annualisée

**Formule** :
```
σ_annualisée = σ_quotidienne × √252
```

**Interprétation** :
- **< 5%** : Très faible volatilité (fonds monétaire, obligataire court terme)
- **5-10%** : Faible volatilité (obligataire, diversifié prudent)
- **10-15%** : Volatilité modérée (mixte, diversifié équilibré)
- **15-20%** : Volatilité élevée (actions, marchés émergents)
- **> 20%** : Très forte volatilité (secteurs spécifiques, leviers)

**Guide Décisionnel** :
- Profil conservateur → Privilégier volatilité < 10%
- Profil équilibré → Accepter volatilité 10-15%
- Profil dynamique → Tolérer volatilité > 15%

##### 1.5.2 Value at Risk (VaR)

**Description** : Perte maximale attendue avec un niveau de confiance donné (95% ou 99%).

**Formule (méthode paramétrique)** :
```
VaR_95% = μ - 1.645 × σ
VaR_99% = μ - 2.326 × σ
```

**Interprétation** :
- VaR 95% = -2% signifie : "Il y a 5% de chance de perdre plus de 2% en une journée"

**Guide Décisionnel** :
- |VaR| < 1% → Risque faible acceptable
- |VaR| entre 1% et 3% → Risque modéré, surveillance requise
- |VaR| > 3% → Risque élevé, limiter l'exposition

##### 1.5.3 Conditional VaR (CVaR ou Expected Shortfall)

**Description** : Perte moyenne attendue dans les pires scénarios (au-delà du VaR).

**Formule** :
```
CVaR_95% = Moyenne(rendements) pour rendements < VaR_95%
```

**Interprétation** :
- Plus conservateur que VaR (prend en compte l'ampleur des pertes extrêmes)
- CVaR >> VaR indique des queues épaisses (événements extrêmes sévères)

**Guide Décisionnel** :
- Ratio CVaR/VaR > 1.5 → Risque de queue significatif, prudence

##### 1.5.4 Ratio de Sharpe

**Description** : Mesure du rendement ajusté au risque (excès de rendement par unité de risque).

**Formule** :
```
Sharpe = (Rendement_moyen - Taux_sans_risque) / σ_rendements
```

**Interprétation** :
- **< 0** : Performance inférieure au taux sans risque
- **0 à 1** : Performance acceptable mais faible rapport risque/rendement
- **1 à 2** : Bon rapport risque/rendement
- **> 2** : Excellent rapport risque/rendement

**Guide Décisionnel** :
- Comparer les fonds : privilégier Sharpe le plus élevé à volatilité équivalente
- Sharpe < 0.5 → Remettre en question l'allocation
- Sharpe > 1.5 → Candidat prioritaire pour allocation

##### 1.5.5 Maximum Drawdown (MDD)

**Description** : Perte maximale depuis un sommet historique (peak-to-trough).

**Formule** :
```
Drawdown(t) = (VL(t) / VL_max_précédent) - 1
MDD = min(Drawdown(t)) pour tout t
```

**Interprétation** :
- MDD = -20% signifie : "Le fonds a perdu au maximum 20% depuis son plus haut"
- Mesure de la pire expérience historique pour l'investisseur

**Guide Décisionnel** :
- |MDD| < 10% → Fonds résilient, risque maîtrisé
- |MDD| entre 10% et 20% → Risque modéré acceptable
- |MDD| > 20% → Risque élevé, tolérance importante requise

##### 1.5.6 Pain Ratio

**Description** : Ratio de la performance totale sur la "douleur" accumulée (somme des drawdowns).

**Formule** :
```
Pain_Index = Σ|Drawdown(t)| / n
Pain_Ratio = Rendement_total / Pain_Index
```

**Interprétation** :
- Mesure l'expérience psychologique de l'investisseur
- Pain Ratio élevé = gains compensent largement l'inconfort des baisses

**Guide Décisionnel** :
- Pain Ratio > 2 → Excellente expérience investisseur
- Pain Ratio entre 1 et 2 → Acceptable
- Pain Ratio < 1 → Expérience douloureuse, révision nécessaire

##### 1.5.7 Ulcer Index

**Description** : Mesure de la profondeur et de la durée des drawdowns.

**Formule** :
```
Ulcer_Index = √[Σ(Drawdown²(t)) / n]
```

**Interprétation** :
- Pénalise à la fois les drawdowns profonds et prolongés
- Plus sensible que le MDD aux périodes de faiblesse

**Guide Décisionnel** :
- Complémentaire au MDD pour évaluer le stress investisseur
- Ulcer Index élevé → Périodes de drawdown longues, patience requise

#### 1.6 Profil de Risque Multi-Dimensionnel (Risk Fingerprint)

**Description** : Analyse radar sur 7 dimensions normalisées à l'échelle [0, 100].

**Dimensions Évaluées** :

1. **Volatilité** : Stabilité des rendements (score inversé : faible volatilité = score élevé)
2. **Max Drawdown** : Résilience (score inversé : faible MDD = score élevé)
3. **Pain Ratio** : Expérience investisseur
4. **Ulcer Index** : Confort psychologique (score inversé)
5. **Ratio de Sharpe** : Efficience risque-rendement
6. **Skewness** : Asymétrie des rendements (positif favorisé)
7. **VaR** : Risque extrême (score inversé : faible VaR = score élevé)

**Normalisation** :
Chaque métrique est transformée pour que :
- Score 0 = Pire performance observée dans l'univers
- Score 100 = Meilleure performance observée dans l'univers
- Score 50 = Performance médiane

**Interprétation** :
- **Score Global > 70** : Profil de risque excellent, fonds de qualité supérieure
- **Score Global 50-70** : Profil de risque satisfaisant, équilibré
- **Score Global < 50** : Profil de risque préoccupant, vigilance accrue

**Graphique Radar** : Visualise instantanément les forces et faiblesses du fonds.

**Guide Décisionnel** :
- Profil équilibré (toutes dimensions > 50) → Allocation significative possible (15-25%)
- Une dimension < 30 → Point de vigilance, analyse approfondie requise
- Plusieurs dimensions < 40 → Allocation limitée (< 10%), profil agressif uniquement

#### 1.7 Analyse de Volatilité

##### 1.7.1 Clustering par Volatilité (K-Means)

**Description** : Regroupement automatique des FCP en clusters de volatilité similaire.

**Méthode** :
- Algorithme K-Means (3 clusters par défaut : faible, moyenne, forte volatilité)
- Basé sur la volatilité annualisée des rendements

**Visualisation** :
- Scatter plot : chaque point = un FCP
- Couleurs : cluster d'appartenance
- Axes : volatilité vs rendement moyen

**Interprétation** :
- **Cluster 1 (faible volatilité)** : Fonds défensifs, préservation du capital
- **Cluster 2 (moyenne volatilité)** : Fonds équilibrés
- **Cluster 3 (forte volatilité)** : Fonds dynamiques, recherche de performance

**Guide Décisionnel** :
- Diversifier entre clusters pour un portefeuille équilibré
- Cluster faible volatilité pour allocation de base (core)
- Cluster forte volatilité pour allocation satellite (tactique)

##### 1.7.2 Régimes de Volatilité

**Description** : Identification des périodes de volatilité normale vs élevée.

**Méthode** :
- Calcul de la volatilité glissante (fenêtre paramétrable, défaut 21 jours)
- Seuil : volatilité moyenne + écart-type

**Visualisation** :
- Graphique temporel avec zones colorées (vert = normal, rouge = élevé)

**Interprétation** :
- Périodes rouges = stress de marché, crises
- Transition normal → élevé = signal d'alerte
- Retour élevé → normal = normalisation

**Guide Décisionnel** :
- En régime de volatilité élevée → Réduire l'exposition, privilégier liquidité
- Sortie de régime élevé → Opportunité de réallocation

##### 1.7.3 Indicateurs de Risque Glissants

**Description** : Évolution temporelle du Sharpe Ratio, MDD et Ulcer Index.

**Utilité** :
- Détecter la dégradation/amélioration du profil de risque dans le temps
- Identifier les tendances (amélioration continue vs détérioration)

**Interprétation** :
- Sharpe en hausse → Amélioration de l'efficience
- MDD/Ulcer en hausse → Dégradation du risque

**Guide Décisionnel** :
- Tendance de dégradation sur 6 mois → Réévaluer l'allocation
- Amélioration continue → Conforter l'allocation

#### 1.8 Analyse de Drawdown

**Graphique** : Évolution du drawdown dans le temps pour chaque FCP.

**Interprétation** :
- Zone en dessous de 0 = période de drawdown (sous le pic précédent)
- Retour à 0 = nouveau sommet atteint (recovery)

**Métriques** :
- **Durée maximale de drawdown** : Temps le plus long sous l'eau
- **Fréquence des drawdowns** : Nombre de périodes de baisse

**Guide Décisionnel** :
- Drawdown actuel proche du MDD historique → Possibilité de rebond
- Recovery rapide (< 3 mois) → Bonne résilience
- Recovery lente (> 12 mois) → Prudence sur allocations futures

#### 1.9 Probabilités de Perte

**Description** : Probabilité de subir une perte sur différents horizons temporels.

**Méthode** :
- Simulation Monte Carlo ou approche empirique historique
- Horizons : 1 jour, 1 semaine, 1 mois, 3 mois, 1 an

**Formule (approche normale)** :
```
P(Perte) = P(Rendement < 0) = Φ(-μ/σ)
```
où Φ est la fonction de répartition de la loi normale.

**Interprétation** :
- Probabilité élevée (> 40%) sur 1 mois → Volatilité importante
- Probabilité faible (< 10%) sur 1 an → Tendance haussière forte

**Guide Décisionnel** :
- Horizon court avec P(Perte) élevée → Éviter timing de marché
- Horizon long avec P(Perte) faible → Stratégie buy & hold appropriée

#### 1.10 Capture Ratios

##### Upside Capture Ratio

**Description** : Pourcentage de la hausse du benchmark capturé par le fonds.

**Formule** :
```
Upside_Capture = Rendement_fonds_périodes_haussières / Rendement_benchmark_périodes_haussières
```

**Interprétation** :
- **> 100%** : Le fonds surperforme le benchmark en hausse
- **= 100%** : Le fonds réplique le benchmark
- **< 100%** : Le fonds sous-performe en hausse

##### Downside Capture Ratio

**Description** : Pourcentage de la baisse du benchmark subie par le fonds.

**Formule** :
```
Downside_Capture = Rendement_fonds_périodes_baissières / Rendement_benchmark_périodes_baissières
```

**Interprétation** :
- **< 100%** : Le fonds protège mieux que le benchmark (souhaitable)
- **= 100%** : Le fonds suit le benchmark
- **> 100%** : Le fonds amplifie les baisses (indésirable)

**Guide Décisionnel** :
- Profil idéal : Upside > 100% et Downside < 100%
- Downside > 100% → Risque excessif, réévaluation nécessaire
- Upside faible mais Downside très faible → Fonds défensif, utile en diversification

#### 1.11 Récit Narratif Automatique

**Description** : Génération automatique d'une analyse textuelle professionnelle basée sur les métriques calculées.

**Contenu** :
- Synthèse du profil de risque global
- Analyse des forces et faiblesses
- Recommandation d'allocation
- Synthèse décisionnelle

**Utilité** :
- Facilite la communication avec les clients
- Prêt pour comité d'investissement
- Résumé actionnable des analyses quantitatives

---

## 2. 💰 Souscriptions & Rachats

### Vue d'Ensemble

Cette page analyse les flux de souscriptions et rachats pour comprendre l'attractivité des fonds et le comportement des investisseurs.

### Sous-Sections

#### 2.1 Indicateurs Clés de Performance

**Métriques Calculées** :

1. **Total Souscriptions** : Somme de tous les montants de souscription sur la période
   ```
   Total_Souscriptions = Σ(Montants où Opération = "Souscription")
   ```

2. **Total Rachats** : Somme de tous les montants de rachat
   ```
   Total_Rachats = Σ(Montants où Opération = "Rachat")
   ```

3. **Flux Net** : Différence entre souscriptions et rachats
   ```
   Flux_Net = Total_Souscriptions - Total_Rachats
   ```

4. **Ratio Souscriptions/Rachats** : Indicateur de l'attractivité relative
   ```
   Ratio_S/R = Total_Souscriptions / Total_Rachats
   ```

**Interprétation** :
- **Flux Net > 0** : Le fonds collecte (attractif)
- **Flux Net < 0** : Le fonds décollecte (rachats > souscriptions)
- **Ratio S/R > 1** : Plus de souscriptions que de rachats (positif)
- **Ratio S/R < 1** : Plus de rachats (vigilance)

**Guide Décisionnel** :
- Flux net négatif persistant (> 3 mois) → Investiguer les causes (sous-performance, problème commercial)
- Flux net positif croissant → Fonds en phase de développement, augmenter support commercial
- Ratio S/R < 0.8 → Alerte, risque de fermeture ou fusion

#### 2.2 Évolution Temporelle

**Graphiques** :
- Évolution des souscriptions dans le temps
- Évolution des rachats dans le temps
- Évolution du flux net

**Analyse** :
- **Tendance** : Identifier si les flux sont croissants, stables ou décroissants
- **Saisonnalité** : Détecter des patterns récurrents (fin de trimestre, fin d'année)
- **Volatilité** : Mesurer la stabilité des flux

**Interprétation** :
- Pics de souscription après bonnes performances → Comportement pro-cyclique (attention au timing)
- Pics de rachats après sous-performance → Investisseurs peu patients
- Flux stable → Base d'investisseurs fidèles

**Guide Décisionnel** :
- Comportement pro-cyclique marqué → Éduquer les investisseurs (acheter bas, vendre haut)
- Pics de rachats massifs → Risque de liquidité, renforcer réserves de cash
- Flux réguliers → Fonds mature, base solide

#### 2.3 Analyse par Type de Client

**Segmentation** :
- Institutionnels
- Retail (particuliers)
- Professionnels
- Autres

**Métriques par Segment** :
- Volume de souscriptions
- Volume de rachats
- Flux net
- Part relative dans le total

**Visualisations** :
- Graphiques en barres empilées
- Camembert de répartition
- Heatmap temporelle par segment

**Interprétation** :
- **Institutionnels** : Tickets larges, moins volatils, base stable
- **Retail** : Plus volatils, réactifs aux performances court terme
- Concentration sur un segment → Risque de concentration

**Guide Décisionnel** :
- > 70% d'un seul segment → Diversifier la base de clientèle
- Retail en décollecte mais Institutionnels en collecte → Fonds devient plus institutionnel (normal pour fonds matures)
- Tous segments en décollecte → Problème structurel (performance, frais, distribution)

#### 2.4 Heatmap de Corrélation

**Description** : Corrélation entre les flux nets des différents FCP.

**Interprétation** :
- Corrélation élevée → Flux synchronisés (mêmes clients, mêmes canaux de distribution)
- Corrélation faible → Clientèles distinctes, bon pour diversification des risques commerciaux

**Guide Décisionnel** :
- Corrélation > 0.8 entre fonds similaires → Normal
- Corrélation > 0.8 entre fonds différents → Analyser les raisons (clients common, recommandations communes)

#### 2.5 Analyses Avancées

##### Saisonnalité des Flux

**Méthode** : Décomposition temporelle (tendance, saisonnalité, résidus).

**Interprétation** :
- Identifier les mois/trimestres propices à la collecte
- Anticiper les périodes de rachats

**Guide Décisionnel** :
- Adapter les campagnes commerciales aux périodes favorables
- Prévoir la liquidité pour les périodes de rachats historiquement élevés

##### Volatilité des Flux

**Formule** :
```
Volatilité_Flux = σ(Flux_Net_t)
```

**Interprétation** :
- Volatilité élevée → Flux imprévisibles, gestion complexe
- Volatilité faible → Flux stables, prévisibles

**Guide Décisionnel** :
- Volatilité élevée → Constituer un coussin de liquidité important
- Volatilité faible → Optimiser l'investissement (moins de cash requis)

##### Corrélation Flux-Performance

**Description** : Corrélation entre les flux nets et la performance du fonds.

**Formule** :
```
Corrélation(Flux_Net, Performance)
```

**Interprétation** :
- **Corrélation positive** : Investisseurs achètent après bonne performance (comportement pro-cyclique, négatif)
- **Corrélation négative** : Investisseurs achètent après baisse (contrarian, positif)
- **Corrélation proche de 0** : Flux indépendants de la performance (clientèle fidèle ou allocation stratégique)

**Guide Décisionnel** :
- Corrélation positive forte (> 0.5) → Risque de flux sortants en cas de sous-performance
- Corrélation négative → Base d'investisseurs sophistiqués, stable
- Éduquer clients pour réduire comportement pro-cyclique

#### 2.6 Classements et Performances

**Classements** :
- Top FCP par souscriptions
- Top FCP par rachats
- Top FCP par flux net

**Utilité** :
- Identifier les fonds stars (forte collecte)
- Identifier les fonds en difficulté (forte décollecte)

**Guide Décisionnel** :
- Fonds en tête de collecte → Renforcer les ressources (gestion, communication)
- Fonds en tête de décollecte → Analyser les causes, plan d'action correctif ou fermeture

---

## 3. 💼 Actifs Nets

### Vue d'Ensemble

Cette page suit l'évolution des actifs nets sous gestion (AUM) et analyse leur composition et dynamique.

### Sous-Sections

#### 3.1 Indicateurs Clés de Performance

**Métriques** :

1. **Total Actifs Nets** : Somme des actifs nets de tous les FCP
2. **Actifs Nets Moyens** : Moyenne des actifs nets sur la période
3. **Évolution (%)** : Variation des actifs nets entre début et fin de période
   ```
   Évolution(%) = ((AN_fin - AN_début) / AN_début) × 100
   ```
4. **CAGR (Compound Annual Growth Rate)** : Taux de croissance annuel composé
   ```
   CAGR = ((AN_fin / AN_début)^(1/n_années) - 1) × 100
   ```

**Interprétation** :
- Évolution positive → Croissance des actifs (collecte nette positive et/ou performance positive)
- CAGR élevé → Croissance forte et soutenue
- CAGR négatif → Décollecte et/ou sous-performance

**Guide Décisionnel** :
- CAGR > 10% → Croissance forte, fonds attractif
- CAGR entre 0% et 10% → Croissance modérée, satisfaisant
- CAGR < 0% → Décroissance, actions correctives nécessaires

#### 3.2 Évolution Temporelle des Actifs Nets

**Graphique** : Évolution des actifs nets de chaque FCP dans le temps.

**Interprétation** :
- Croissance continue → Combinaison de performance et collecte
- Stagnation → Équilibre entre collecte/décollecte et performance/perte
- Décroissance → Problème structurel

**Décomposition** :
L'évolution des actifs nets résulte de deux facteurs :
```
ΔAN = Effet_VL + Effet_Flux
```
- **Effet VL** : Variation due à la performance (VL)
- **Effet Flux** : Variation due aux souscriptions/rachats nets

**Guide Décisionnel** :
- Croissance tirée par la performance → Fonds performant, communiquer
- Croissance tirée par les flux → Fonds attractif commercialement
- Décroissance malgré bonne performance → Problème de distribution/commercialisation
- Décroissance due à sous-performance → Améliorer la gestion

#### 3.3 Répartition des Actifs Nets par FCP

**Visualisations** :
- Graphique en barres : actifs nets par FCP
- Camembert : part relative de chaque FCP dans le total

**Métriques** :
- **Concentration** : Part du plus gros FCP dans le total
- **Top 3** : Part cumulée des 3 plus gros FCP

**Interprétation** :
- Concentration élevée (> 50% sur un FCP) → Risque de concentration
- Répartition équilibrée → Diversification des sources de revenus

**Guide Décisionnel** :
- Concentration > 60% → Développer d'autres fonds pour réduire la dépendance
- Distribution très dispersée → Fermer les petits fonds non rentables

#### 3.4 Analyses Avancées

##### Taux de Croissance Temporel

**Description** : Évolution du taux de croissance des actifs nets dans le temps.

**Formule** :
```
Taux_croissance(t) = (AN(t) - AN(t-1)) / AN(t-1)
```

**Interprétation** :
- Accélération de la croissance → Dynamique positive
- Décélération → Attention, risque de retournement

##### Corrélation Actifs Nets - Flux

**Description** : Mesure dans quelle proportion l'évolution des actifs nets est expliquée par les flux de souscription/rachat.

**Formule** :
```
Corrélation(ΔAN, Flux_Net)
```

**Interprétation** :
- Corrélation forte → Actifs nets pilotés par les flux commerciaux
- Corrélation faible → Actifs nets pilotés par la performance

##### Décomposition VL vs Flux

**Description** : Attribuer la variation des actifs nets entre effet performance (VL) et effet flux.

**Formule** :
```
ΔAN_total = ΔAN_VL + ΔAN_Flux

Contribution_VL(%) = ΔAN_VL / ΔAN_total × 100
Contribution_Flux(%) = ΔAN_Flux / ΔAN_total × 100
```

**Interprétation** :
- Contribution VL dominante → Performance moteur principal
- Contribution Flux dominante → Collecte moteur principal
- Contributions opposées → Compensation (ex: bonne performance mais décollecte)

**Guide Décisionnel** :
- Contribution VL > 70% → Communiquer sur la performance, attirer nouveaux clients
- Contribution Flux > 70% → Fonds commercialement attractif mais performance à surveiller
- Contributions négatives croisées → Situation critique (sous-performance + décollecte)

##### Classement par Taille et Croissance

**Matrices** :
- Taille (actifs nets actuels) vs Croissance (CAGR ou évolution récente)

**Quadrants** :
- **Stars** : Gros et en croissance → Fonds phares, maximiser l'exposition
- **Cash Cows** : Gros mais stagnants → Optimiser la rentabilité, pas de nouveaux investissements
- **Question Marks** : Petits mais en croissance → Investir pour développer
- **Dogs** : Petits et stagnants/décroissants → Fermeture ou fusion à considérer

---

## 4. ℹ️ À Propos

### Vue d'Ensemble

Cette page fournit une documentation complète des concepts, formules et méthodologies utilisées dans l'application.

### Contenu

#### 4.1 Notions Fondamentales

- Valeur Liquidative (VL)
- Actifs Nets
- Souscription / Rachat
- Parts du fonds
- Rendement

#### 4.2 Indicateurs de Performance

- Performances calendaires et glissantes
- Rendement annualisé
- Rendement moyen et géométrique

#### 4.3 Mesures de Risque

- Volatilité
- VaR et CVaR
- Maximum Drawdown
- Ulcer Index
- Ratios (Sharpe, Sortino, Calmar, Pain)

#### 4.4 Analyse Avancée

- Corrélations
- Clustering (K-Means)
- Régimes de volatilité
- Distribution des rendements (Skewness, Kurtosis)

#### 4.5 Interprétation des Résultats

- Guide de lecture des graphiques
- Seuils d'alerte
- Recommandations pratiques

#### 4.6 Glossaire

Définitions des termes techniques utilisés dans l'application.

---

## 📐 Formules et Méthodes de Calcul

### Rendements

**Rendement simple** :
```
R_t = (VL_t / VL_{t-1}) - 1
```

**Rendement logarithmique** :
```
r_t = ln(VL_t / VL_{t-1})
```

**Rendement sur période** :
```
R_période = (VL_fin / VL_début) - 1
```

**Rendement annualisé** :
```
R_annualisé = (1 + R_total)^(252/n_jours) - 1
```

### Volatilité

**Volatilité quotidienne** :
```
σ_quotidienne = √[Σ(R_t - μ)² / (n-1)]
```

**Volatilité annualisée** :
```
σ_annualisée = σ_quotidienne × √252
```

### Ratios

**Ratio de Sharpe** :
```
Sharpe = (R_moyen - R_f) / σ
```
où R_f = taux sans risque (souvent 0 en approximation)

**Ratio de Sortino** :
```
Sortino = (R_moyen - R_f) / σ_downside
```
où σ_downside = écart-type des rendements négatifs uniquement

**Ratio de Calmar** :
```
Calmar = R_annualisé / |MDD|
```

**Pain Ratio** :
```
Pain = R_total / Pain_Index
Pain_Index = Σ|Drawdown_t| / n
```

### Drawdown

**Drawdown à l'instant t** :
```
DD_t = (VL_t / max(VL_0, ..., VL_{t-1})) - 1
```

**Maximum Drawdown** :
```
MDD = min(DD_t) pour tout t
```

### Statistiques Distributionnelles

**Skewness (Asymétrie)** :
```
Skewness = [n / ((n-1)(n-2))] × Σ[(R_t - μ) / σ]³
```

**Kurtosis Excess** :
```
Kurtosis_excess = [n(n+1) / ((n-1)(n-2)(n-3))] × Σ[(R_t - μ) / σ]⁴ - 3(n-1)² / ((n-2)(n-3))
```

### Corrélation

**Coefficient de corrélation de Pearson** :
```
ρ(X,Y) = Cov(X,Y) / (σ_X × σ_Y)
Cov(X,Y) = Σ[(X_t - μ_X)(Y_t - μ_Y)] / (n-1)
```

### CAGR (Taux de Croissance Annuel Composé)

```
CAGR = (Valeur_fin / Valeur_début)^(1/n_années) - 1
```

---

## 🎯 Guide Décisionnel

### Profil Investisseur

#### Conservateur
- **Objectif** : Préservation du capital, rendement modeste
- **Tolérance au risque** : Très faible
- **Critères de sélection** :
  - Volatilité < 5%
  - |MDD| < 5%
  - Sharpe > 1
  - Skewness > 0 (si possible)
- **Allocation** : Privilégier fonds obligataires, monétaires

#### Équilibré
- **Objectif** : Croissance modérée avec risque maîtrisé
- **Tolérance au risque** : Moyenne
- **Critères de sélection** :
  - Volatilité 5-15%
  - |MDD| < 15%
  - Sharpe > 0.7
  - Profil de risque global > 50
- **Allocation** : Mixte actions/obligations (30-70% actions)

#### Dynamique
- **Objectif** : Forte croissance, acceptation de la volatilité
- **Tolérance au risque** : Élevée
- **Critères de sélection** :
  - Volatilité jusqu'à 25%
  - Sharpe > 0.5
  - Historique de rebond après drawdowns
- **Allocation** : Actions, marchés émergents, sectoriels

### Matrice de Décision

| Métrique | Excellent | Satisfaisant | Préoccupant |
|----------|-----------|--------------|-------------|
| Sharpe Ratio | > 1.5 | 0.7 - 1.5 | < 0.7 |
| Volatilité (équilibré) | < 10% | 10-15% | > 15% |
| |MDD| | < 10% | 10-20% | > 20% |
| Pain Ratio | > 2 | 1-2 | < 1 |
| Flux Net (6M) | > 10% croissance | Stable (±5%) | < -5% |
| Score Risque Global | > 70 | 50-70 | < 50 |

### Signaux d'Alerte

🚨 **Alerte Majeure** (Action immédiate requise) :
- Sharpe < 0 sur 6 mois
- MDD en cours > 25%
- Décollecte > 20% sur 3 mois
- Score de risque global < 30
- Corrélation Flux-Performance > 0.7 (comportement pro-cyclique extrême)

⚠️ **Vigilance** (Surveillance accrue) :
- Sharpe en baisse continue sur 6 mois
- Volatilité en hausse > 50% vs historique
- Skewness < -0.5 (risque de queue gauche)
- Flux net négatif 3 mois consécutifs
- Score de risque 30-50

✅ **Normal** (Maintien de l'allocation) :
- Métriques dans les fourchettes satisfaisantes
- Pas de dégradation significative
- Flux stables ou en croissance

### Actions Recommandées par Situation

#### Situation : Sous-performance persistante
- **Diagnostic** : Sharpe faible, Performance < benchmark sur 6-12 mois
- **Actions** :
  1. Analyser les causes (allocation sectorielle, stock picking, timing)
  2. Comparer avec pairs et benchmark
  3. Si structurel : réduire allocation de 30-50%
  4. Si conjoncturel : maintenir avec surveillance

#### Situation : Décollecte importante
- **Diagnostic** : Flux net négatif > 15% sur 3 mois
- **Actions** :
  1. Investiguer causes (performance, commercialisation, concurrence)
  2. Renforcer liquidités (réduire actifs illiquides)
  3. Plan de communication clients
  4. Si > 30% : considérer fermeture ou fusion

#### Situation : Volatilité anormale
- **Diagnostic** : Volatilité > 2× historique récent
- **Actions** :
  1. Vérifier s'il s'agit d'un événement de marché général (crise) ou spécifique
  2. Si spécifique : analyser les positions problématiques
  3. Réduire temporairement l'exposition de 20-40%
  4. Attendre retour à la normale pour réallouer

#### Situation : Excellent profil
- **Diagnostic** : Score global > 70, Sharpe > 1.5, Flux positifs
- **Actions** :
  1. Augmenter allocation (si liquidité suffisante) de 20-30%
  2. Utiliser comme fonds core dans portefeuilles équilibrés
  3. Communiquer la performance (marketing)
  4. Surveiller maintien de la qualité

---

## 🛠️ Technologies Utilisées

### Framework et Bibliothèques

- **Streamlit** : Framework d'application web interactive
- **Pandas** : Manipulation et analyse de données
- **NumPy** : Calculs numériques
- **Plotly / Plotly Express** : Visualisations interactives
- **Scikit-learn** : Machine Learning (K-Means clustering)
- **SciPy** : Statistiques avancées
- **Statsmodels** : Décomposition temporelle (optionnel)

### Architecture

```
Application-FCP/
├── app.py                          # Page d'accueil
├── pages/
│   ├── 1_Valeurs_Liquidatives.py   # Analyse VL
│   ├── 2_Souscriptions_Rachats.py  # Analyse flux
│   ├── 3_Actifs_Nets.py            # Analyse actifs nets
│   └── 4_A_Propos.py               # Documentation
├── data_loader.py                  # (Optionnel) Chargement de données
├── data_fcp.xlsx                   # Données
└── README.md                       # Ce fichier
```

### Palette de Couleurs

L'application utilise une palette de couleurs cohérente pour une expérience utilisateur professionnelle :

- **PRIMARY_COLOR** : `#004080` (Bleu foncé) - Titres, boutons principaux
- **SECONDARY_COLOR** : `#333333` (Gris foncé) - Widgets, lignes, icônes
- **THIRD_COLOR** : `#E0DEDD` (Gris clair) - Fonds de cartes, hover

**Formatage Conditionnel des Tableaux** :
- 🟢 **Vert** : Valeurs positives (gains, croissance)
- 🔴 **Rouge** : Valeurs négatives (pertes, décroissance)

---

## 📞 Support et Contact

**Développé pour** : CGF BOURSE

**Auteur** : DYLANE

Pour toute question, suggestion ou problème :
- Créer une issue sur le repository GitHub
- Contacter l'équipe de développement CGF BOURSE

---

## 📝 Notes Importantes

### Limites et Avertissements

1. **Performances passées** : Les performances passées ne préjugent pas des performances futures
2. **Modèles statistiques** : Les modèles (VaR, corrélations) supposent une certaine stabilité des distributions, invalidée en période de crise
3. **Données** : La qualité des analyses dépend de la qualité et complétude des données sources
4. **Fréquence de mise à jour** : Les analyses sont basées sur les données disponibles au moment du chargement

### Bonnes Pratiques d'Utilisation

1. **Mettre à jour régulièrement** les données (quotidien ou hebdomadaire)
2. **Combiner plusieurs métriques** pour une décision (ne pas se baser sur un seul indicateur)
3. **Analyser le contexte** : tenir compte des conditions de marché générales
4. **Horizon temporel** : adapter l'analyse à l'horizon d'investissement
5. **Diversification** : ne jamais concentrer sur un seul FCP, même excellent

### Glossaire Rapide

- **VL** : Valeur Liquidative
- **FCP** : Fonds Commun de Placement
- **AUM** : Assets Under Management (Actifs sous Gestion)
- **MDD** : Maximum Drawdown
- **VaR** : Value at Risk
- **CVaR** : Conditional Value at Risk
- **WTD** : Week To Date
- **MTD** : Month To Date
- **QTD** : Quarter To Date
- **YTD** : Year To Date
- **CAGR** : Compound Annual Growth Rate

---

**Version** : 1.0
**Date de dernière mise à jour** : Décembre 2024

© 2024 CGF BOURSE - Tous droits réservés
