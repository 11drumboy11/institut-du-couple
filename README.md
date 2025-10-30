# 🎯 Guide de Déploiement sur Netlify (Mac)

## 📦 Contenu du dossier

Votre dossier `bilan-couple-site` contient :

✅ **index.html** - Page d'accueil avec navigation vers tous les outils
✅ **10 outils interactifs** - Tous vos questionnaires et exercices
✅ **2 chartes graphiques** - Documentation de votre identité visuelle

### Liste complète des fichiers :

1. **Page d'accueil**
   - index.html → Accueil avec liens vers tous les outils

2. **Outils d'évaluation**
   - isqv-couple.html → Indice de Satisfaction Conjugale
   - das32.html → Questionnaire d'Ajustement Dyadique
   - controle-technique.html → Contrôle Technique du Couple
   - swot-conjugal.html → Analyse SWOT de votre couple
   - exercice-gottman.html → Exercice Gottman
   - big5.html → Test de personnalité Big Five

3. **Outils d'analyse**
   - relatiogramme.html → Réseau relationnel
   - appartenancogramme.html → Cartographie des appartenances
   - agenda-couple.html → Analyse du temps
   - centres-interet.html → Compatibilité des centres d'intérêt

4. **Ressources**
   - charte-graphique.html → Charte graphique complète
   - charte-categories.html → Palette de couleurs

---

## 🚀 Comment déployer sur Netlify (3 étapes simples)

### Étape 1 : Décompresser le fichier ZIP

1. **Téléchargez** le fichier `bilan-couple-site.zip`
2. **Double-cliquez** dessus pour le décompresser
3. Vous obtenez un dossier `bilan-couple-site` avec tous les fichiers

### Étape 2 : Aller sur Netlify

1. Ouvrez Safari (ou votre navigateur)
2. Allez sur : **https://app.netlify.com**
3. Connectez-vous avec votre compte
4. Cliquez sur votre site **"bilandecompetencesducouple"**
5. Cliquez sur l'onglet **"Deploys"** en haut

### Étape 3 : Glisser-Déposer

1. **Ouvrez le Finder** et trouvez votre dossier `bilan-couple-site`
2. **Glissez le dossier entier** directement dans la zone Netlify qui dit :
   ```
   "Need to update your site? 
   Drag and drop your site folder here"
   ```
3. ⏳ **Attendez 10-30 secondes**
4. ✅ **C'est en ligne !**

---

## 🔗 Vos URLs seront :

**Page d'accueil :**
https://bilandecompetencesducouple.netlify.app/

**Exemples d'outils :**
- https://bilandecompetencesducouple.netlify.app/swot-conjugal.html
- https://bilandecompetencesducouple.netlify.app/das32.html
- https://bilandecompetencesducouple.netlify.app/isqv-couple.html
- etc.

---

## 💡 Pour ajouter une nouvelle page plus tard

1. **Créez** le nouveau fichier `.html` dans votre dossier `bilan-couple-site`
2. **Mettez à jour** `index.html` pour ajouter un lien vers cette nouvelle page
3. **Glissez-déposez** à nouveau le dossier complet sur Netlify
4. ✅ Votre site est mis à jour avec la nouvelle page

---

## 🎨 Pour intégrer dans Podia

### Option 1 : Iframe (page complète)

```html
<iframe 
    src="https://bilandecompetencesducouple.netlify.app/nom-outil.html" 
    width="100%" 
    height="1000px" 
    style="border:none;">
</iframe>
```

### Option 2 : Lien direct

Créez un bouton avec le lien :
```
https://bilandecompetencesducouple.netlify.app/nom-outil.html
```

---

## ⚠️ Important pour Mac

- ✅ Les noms de fichiers sont en minuscules avec tirets (pas d'espaces)
- ✅ Tous les fichiers sont au format HTML
- ✅ Aucun dossier CSS/JS séparé n'est nécessaire
- ✅ Tout fonctionne "hors de la boîte"

---

## 📞 Besoin d'aide ?

Si vous avez des questions, contactez-moi et je vous aiderai !

---

**Créé avec ❤️ pour votre Bilan de Compétences du Couple**
Marie-Christine Abatte - Psychologue
