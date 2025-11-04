# 💑 GUIDE DE DÉMARRAGE - Institut du Couple

## 📥 FICHIERS TÉLÉCHARGÉS

Tu as téléchargé plusieurs fichiers. Voici **exactement où** les mettre dans ton repository local.

---

## 📂 OÙ METTRE CHAQUE FICHIER ?

### Dans ton dossier local `institut-du-couple/` :

```
institut-du-couple/                    ← Ton dossier local (déjà cloné)
│
├── .github/                           ← CRÉER CE DOSSIER
│   ├── workflows/                     ← CRÉER CE SOUS-DOSSIER
│   │   └── generate-indexes.yml      ← COPIER ICI (depuis github-workflows/)
│   │
│   └── scripts/                       ← CRÉER CE SOUS-DOSSIER
│       └── generate_all_indexes.py   ← COPIER ICI (depuis github-scripts/)
│
├── Module 1/                          ← CRÉER CES DOSSIERS
├── Module 2/                          ← (pour ton contenu)
├── Module 3/
├── Module 4/
├── Module 5/
├── Module 6/
├── Module 7/
├── Module 8/
├── Module 9/
├── Module 10/
├── Quiz/
├── Resultats/
├── Documentation/
│
├── requirements.txt                   ← COPIER ICI (déjà téléchargé)
├── .gitignore                        ← RENOMMER gitignore.txt en .gitignore
└── test-local.sh                     ← COPIER ICI (optionnel)
```

---

## ✅ ÉTAPES À SUIVRE

### Étape 1 : Crée la structure (2 min)

Ouvre un Terminal/PowerShell dans ton dossier `institut-du-couple` et tape :

**Sur Mac/Linux :**
```bash
mkdir -p .github/workflows
mkdir -p .github/scripts
mkdir -p "Module 1" "Module 2" "Module 3" "Module 4" "Module 5"
mkdir -p "Module 6" "Module 7" "Module 8" "Module 9" "Module 10"
mkdir -p Quiz Resultats Documentation
```

**Sur Windows (PowerShell) :**
```powershell
New-Item -ItemType Directory -Force -Path .github\workflows
New-Item -ItemType Directory -Force -Path .github\scripts
New-Item -ItemType Directory -Force -Path "Module 1"
New-Item -ItemType Directory -Force -Path "Module 2"
New-Item -ItemType Directory -Force -Path "Module 3"
New-Item -ItemType Directory -Force -Path "Module 4"
New-Item -ItemType Directory -Force -Path "Module 5"
New-Item -ItemType Directory -Force -Path "Module 6"
New-Item -ItemType Directory -Force -Path "Module 7"
New-Item -ItemType Directory -Force -Path "Module 8"
New-Item -ItemType Directory -Force -Path "Module 9"
New-Item -ItemType Directory -Force -Path "Module 10"
New-Item -ItemType Directory -Force -Path Quiz
New-Item -ItemType Directory -Force -Path Resultats
New-Item -ItemType Directory -Force -Path Documentation
```

### Étape 2 : Copie les fichiers téléchargés (3 min)

**Fichier 1 : Workflow GitHub Actions**
- Prends le fichier : `github-workflows/generate-indexes.yml`
- Copie-le dans : `.github/workflows/generate-indexes.yml`

**Fichier 2 : Script Python**
- Prends le fichier : `github-scripts/generate_all_indexes.py`
- Copie-le dans : `.github/scripts/generate_all_indexes.py`

**Fichier 3 : Requirements**
- Prends le fichier : `requirements.txt`
- Copie-le à la racine : `requirements.txt`

**Fichier 4 : Gitignore**
- Prends le fichier : `gitignore.txt`
- Renomme-le en : `.gitignore` (AVEC le point au début)
- Copie-le à la racine

**Fichier 5 : Test (optionnel)**
- Prends le fichier : `test-local.sh`
- Copie-le à la racine : `test-local.sh`

**Documentation (optionnelle mais recommandée)**
- Prends tous les fichiers du dossier `Documentation/`
- Copie-les dans : `Documentation/`

### Étape 3 : Vérifie ta structure (1 min)

Tu dois avoir exactement ça :

```
institut-du-couple/
├── .github/
│   ├── workflows/
│   │   └── generate-indexes.yml       ✅
│   └── scripts/
│       └── generate_all_indexes.py    ✅
├── requirements.txt                   ✅
├── .gitignore                        ✅
└── (les dossiers Module 1-10, Quiz, etc.)
```

### Étape 4 : Push avec GitHub Desktop (2 min)

1. **Ouvre GitHub Desktop**
2. Tu verras tous les nouveaux fichiers dans "Changes"
3. **Message de commit** : `🤖 Add: Système de bibliothèque automatisé`
4. **Clique sur** "Commit to main"
5. **Clique sur** "Push origin"

### Étape 5 : Active sur GitHub (3 min)

#### Activer GitHub Actions
1. Va sur https://github.com/11drumboy11/institut-du-couple
2. Clique sur **"Actions"**
3. Si demandé, clique sur **"I understand my workflows, go ahead and enable them"**

#### Activer GitHub Pages
1. Va dans **"Settings"** (onglet)
2. Menu gauche : **"Pages"**
3. Sous "Source" :
   - **Branch** : sélectionne `main`
   - **Folder** : sélectionne `/ (root)`
4. Clique sur **"Save"**

✅ **TON SITE SERA ACCESSIBLE ICI** :
```
https://11drumboy11.github.io/institut-du-couple/
```

---

## ⏱️ TEMPS D'ATTENTE

Après le push :
- **GitHub Actions** : 2-3 minutes pour générer les index
- **GitHub Pages** : 5-10 minutes pour publier le site

Total : **Attends environ 10 minutes** avant de visiter ton site la première fois.

---

## 🔍 VÉRIFICATION

### Dans GitHub Desktop
Après le workflow (2-3 min) :
1. Clique sur **"Fetch origin"**
2. Si "Pull origin" apparaît, clique dessus
3. Tu verras maintenant `index.html` dans tes fichiers locaux

### Sur GitHub
1. Va dans **"Actions"**
2. Tu devrais voir un workflow avec ✅ (succès)
3. Si ❌ (erreur), consulte `Documentation/GUIDE-DEPANNAGE.md`

### Sur le site
1. Visite : https://11drumboy11.github.io/institut-du-couple/
2. Tu devrais voir la page d'accueil avec ta charte graphique
3. Teste la recherche (tape "module")

---

## 📚 DOCUMENTATION

Une fois installé, lis ces fichiers pour en savoir plus :

- **`Documentation/QUICK-START.md`**  
  → Commandes rapides et workflow quotidien

- **`Documentation/README-INSTALLATION-COMPLETE.md`**  
  → Guide détaillé avec explications

- **`Documentation/GUIDE-DEPANNAGE.md`**  
  → Solutions si tu as un problème

- **`Documentation/RECAPITULATIF-INSTALLATION.md`**  
  → Vue d'ensemble complète

---

## 🎯 APRÈS L'INSTALLATION

### Workflow quotidien simple

1. **Crée/modifie des fichiers** dans tes modules
2. **Ouvre GitHub Desktop**
3. **Commit et Push**
4. ⏳ **Attends 2-3 minutes**
5. ✅ **Ton site se met à jour automatiquement !**

### Ajouter du contenu

Exemple : Tu veux ajouter un quiz sur la communication

1. Crée `quiz-communication.html` dans le dossier `Quiz/`
2. Push avec GitHub Desktop
3. Le quiz apparaît automatiquement sur le site !

---

## ⚠️ IMPORTANT : Le fichier .gitignore

**Sur Windows** : Le fichier `.gitignore` doit commencer par un point.

Si tu as `gitignore.txt`, renomme-le en `.gitignore` :

**Windows Explorer** :
- Affiche les extensions (Vue → Afficher les extensions de fichiers)
- Renomme `gitignore.txt` → `.gitignore`

**Terminal/PowerShell** :
```bash
mv gitignore.txt .gitignore
```

---

## 🆘 PROBLÈMES ?

### Le workflow ne se lance pas
→ Settings → Actions → Vérifie que c'est activé

### Les fichiers ne sont pas au bon endroit
→ Vérifie que tu as bien :
- `.github/workflows/generate-indexes.yml`
- `.github/scripts/generate_all_indexes.py`

### Le site ne se met pas à jour
→ Attends 10 minutes, puis vide le cache (Ctrl+Shift+R)

### Autre problème
→ Consulte `Documentation/GUIDE-DEPANNAGE.md`

---

## ✅ CHECKLIST FINALE

Avant de considérer que c'est terminé :

- [ ] Dossiers `.github/workflows/` et `.github/scripts/` créés
- [ ] Fichiers copiés aux bons endroits
- [ ] Modules créés (Module 1-10, Quiz, etc.)
- [ ] Push fait avec GitHub Desktop
- [ ] GitHub Actions activé
- [ ] GitHub Pages activé
- [ ] Workflow terminé avec ✅
- [ ] `index.html` généré (visible après Fetch origin)
- [ ] Site accessible sur https://11drumboy11.github.io/institut-du-couple/

---

## 🚀 C'EST PARTI !

Tu es maintenant prêt à :
1. ✅ Ajouter ton contenu
2. ✅ Push avec GitHub Desktop
3. ✅ Laisser le système générer tout automatiquement

**Le système fait tout le travail technique pour toi !**

---

**💑 Institut du Couple - Guide de Démarrage**  
**Version 1.0.0 - 2025-11-04**

**Questions ? Commence par les fichiers dans `Documentation/` !**
