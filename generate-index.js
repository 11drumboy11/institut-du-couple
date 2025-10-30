#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  sourceDir: '.', // Dossier à scanner
  outputFile: 'index.html', // Fichier de sortie
  excludeFiles: ['index.html', 'generate-index.js', 'package.json', 'package-lock.json', 'node_modules', '.git', '.github'],
  extensions: ['.html', '.htm'], // Extensions à inclure
  title: 'Institut du Couple - Marie-Christine Abatte',
  header: 'Institut du Couple',
  description: 'Tous les outils et questionnaires pour évaluer et améliorer votre relation'
};

/**
 * Récupère tous les fichiers HTML du dossier
 */
function getHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    // Ignorer les fichiers/dossiers exclus
    if (CONFIG.excludeFiles.some(exclude => filePath.includes(exclude))) {
      return;
    }

    if (stat.isDirectory()) {
      // Récursion dans les sous-dossiers
      getHtmlFiles(filePath, fileList);
    } else {
      // Vérifier l'extension
      const ext = path.extname(file).toLowerCase();
      if (CONFIG.extensions.includes(ext)) {
        fileList.push({
          path: filePath.replace(/\\/g, '/').replace('./', ''),
          name: file,
          dir: path.dirname(filePath).replace(/\\/g, '/').replace('.', ''),
          modified: stat.mtime,
          size: stat.size
        });
      }
    }
  });

  return fileList;
}

/**
 * Extrait le titre d'un fichier HTML
 */
function extractTitle(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const titleMatch = content.match(/<title>(.*?)<\/title>/i);
    if (titleMatch) {
      return titleMatch[1].trim();
    }
  } catch (error) {
    console.warn(`Impossible de lire ${filePath}:`, error.message);
  }
  return null;
}

/**
 * Formate la taille du fichier
 */
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

/**
 * Formate la date
 */
function formatDate(date) {
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Génère le HTML de l'index
 */
function generateIndexHtml(files) {
  // Trier les fichiers par nom
  files.sort((a, b) => a.path.localeCompare(b.path));

  // Générer les cartes de fichiers
  const fileCards = files.map(file => {
    const title = extractTitle(file.path) || file.name;
    const dirLabel = file.dir ? `📁 ${file.dir}` : '📄 Racine';
    
    return `
    <div class="file-card">
      <div class="file-icon">📄</div>
      <div class="file-info">
        <h3><a href="${file.path}" target="_blank">${title}</a></h3>
        <p class="file-path">${dirLabel}</p>
        <div class="file-meta">
          <span>📅 ${formatDate(file.modified)}</span>
          <span>💾 ${formatSize(file.size)}</span>
        </div>
      </div>
    </div>`;
  }).join('\n');

  // Template HTML complet
  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="generator" content="Auto-generated index">
  <meta name="last-updated" content="${new Date().toISOString()}">
  <title>${CONFIG.title}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      min-height: 100vh;
      padding: 20px;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    header {
      background: white;
      padding: 40px;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      margin-bottom: 30px;
      text-align: center;
    }

    h1 {
      color: #f5576c;
      font-size: 2.5rem;
      margin-bottom: 10px;
      font-weight: 800;
    }

    .subtitle {
      color: #666;
      font-size: 1.1rem;
    }

    .stats {
      display: flex;
      justify-content: center;
      gap: 30px;
      margin-top: 20px;
      flex-wrap: wrap;
    }

    .stat {
      background: #f8f9fa;
      padding: 15px 25px;
      border-radius: 10px;
      font-weight: 600;
    }

    .stat-number {
      color: #f5576c;
      font-size: 1.5rem;
    }

    .search-box {
      background: white;
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      margin-bottom: 30px;
    }

    .search-box input {
      width: 100%;
      padding: 15px 20px;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      font-size: 1rem;
      transition: all 0.3s;
    }

    .search-box input:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .files-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }

    .file-card {
      background: white;
      border-radius: 15px;
      padding: 25px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      transition: all 0.3s;
      display: flex;
      gap: 20px;
      align-items: start;
    }

    .file-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }

    .file-icon {
      font-size: 2.5rem;
      flex-shrink: 0;
    }

    .file-info {
      flex: 1;
      min-width: 0;
    }

    .file-info h3 {
      margin-bottom: 8px;
      font-size: 1.2rem;
    }

    .file-info h3 a {
      color: #333;
      text-decoration: none;
      transition: color 0.3s;
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .file-info h3 a:hover {
      color: #667eea;
    }

    .file-path {
      color: #888;
      font-size: 0.9rem;
      margin-bottom: 10px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .file-meta {
      display: flex;
      gap: 15px;
      font-size: 0.85rem;
      color: #999;
      flex-wrap: wrap;
    }

    footer {
      background: white;
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      text-align: center;
      color: #666;
    }

    .no-results {
      text-align: center;
      padding: 60px 20px;
      background: white;
      border-radius: 15px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      display: none;
    }

    .no-results.show {
      display: block;
    }

    @media (max-width: 768px) {
      .files-grid {
        grid-template-columns: 1fr;
      }
      
      h1 {
        font-size: 2rem;
      }
      
      .stats {
        gap: 15px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🚀 ${CONFIG.header}</h1>
      <p class="subtitle">${CONFIG.description}</p>
      <div class="stats">
        <div class="stat">
          <div class="stat-number">${files.length}</div>
          <div>Pages</div>
        </div>
        <div class="stat">
          <div class="stat-number">${formatDate(new Date())}</div>
          <div>Dernière mise à jour</div>
        </div>
      </div>
    </header>

    <div class="search-box">
      <input 
        type="text" 
        id="searchInput" 
        placeholder="🔍 Rechercher une page..."
        autocomplete="off"
      >
    </div>

    <div class="files-grid" id="filesGrid">
      ${fileCards}
    </div>

    <div class="no-results" id="noResults">
      <h2>😔 Aucun résultat</h2>
      <p>Essayez avec d'autres mots-clés</p>
    </div>

    <footer>
      <p>✨ Index généré automatiquement • ${files.length} pages • Dernière mise à jour : ${formatDate(new Date())}</p>
    </footer>
  </div>

  <script>
    // Fonction de recherche
    const searchInput = document.getElementById('searchInput');
    const filesGrid = document.getElementById('filesGrid');
    const noResults = document.getElementById('noResults');
    const cards = document.querySelectorAll('.file-card');

    searchInput.addEventListener('input', (e) => {
      const searchTerm = e.target.value.toLowerCase().trim();
      let visibleCount = 0;

      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (visibleCount === 0) {
        filesGrid.style.display = 'none';
        noResults.classList.add('show');
      } else {
        filesGrid.style.display = 'grid';
        noResults.classList.remove('show');
      }
    });

    // Animation au chargement
    cards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      setTimeout(() => {
        card.style.transition = 'all 0.5s';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 50);
    });
  </script>
</body>
</html>`;
}

/**
 * Fonction principale
 */
function main() {
  console.log('🚀 Génération de l\'index en cours...\n');

  // Scanner les fichiers
  const files = getHtmlFiles(CONFIG.sourceDir);
  console.log(`✅ ${files.length} fichier(s) HTML trouvé(s)`);

  if (files.length === 0) {
    console.log('⚠️  Aucun fichier HTML trouvé !');
    return;
  }

  // Générer le HTML
  const html = generateIndexHtml(files);

  // Écrire le fichier
  fs.writeFileSync(CONFIG.outputFile, html, 'utf-8');
  console.log(`\n✨ Index généré avec succès : ${CONFIG.outputFile}`);
  console.log(`📁 Fichiers indexés :`);
  files.forEach(f => console.log(`   - ${f.path}`));
}

// Exécution
main();
