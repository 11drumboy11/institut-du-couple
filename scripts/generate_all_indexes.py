#!/usr/bin/env python3
"""
Institut du Couple - Générateur Automatique d'Index Complets
=============================================================

Ce script scanne TOUT le site GitHub et génère :
1. index.html à la racine (page d'accueil complète)
2. index.html dans chaque dossier
3. Système de recherche par nom, contenu et tags

Adapté pour le projet Institut du Couple
Charte graphique : Fond blanc #FFFFFF, couleurs principales
Auteur: Claude
Version: 1.0.0
Date: 2025-11-04
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
from bs4 import BeautifulSoup
import mimetypes
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# Dossiers et fichiers à ignorer
IGNORE_DIRS = {'.git', '.github', 'node_modules', '__pycache__', '.DS_Store'}
IGNORE_FILES = {'.gitignore', 'README.md', '.gitattributes', 'CNAME', 'generate_all_indexes.py'}

# Extensions de fichiers par catégorie
FILE_CATEGORIES = {
    'quiz': {'.html'},  # Formulaires de quiz
    'image': {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'},
    'document': {'.pdf', '.doc', '.docx'},
    'web': {'.html', '.htm', '.css', '.js'},
    'data': {'.json', '.xml', '.csv', '.txt'}
}

# Tags thématiques pour l'Institut du Couple
COUPLE_TAGS = {
    # Catégories du quiz
    'sommeil', 'travail', 'famille', 'tâches', 'solo', 'social', 'couple',
    
    # Thématiques
    'communication', 'organisation', 'intimité', 'sexualité', 
    'gestion', 'conflits', 'émotions', 'temps', 'activités',
    'famille-origine', 'enfants', 'loisirs', 'quotidien',
    
    # Niveaux/Types
    'débutant', 'intermédiaire', 'avancé', 'exercice', 
    'questionnaire', 'ressource', 'documentation',
    
    # Modules
    'module-1', 'module-2', 'module-3', 'module-4', 'module-5',
    'module-6', 'module-7', 'module-8', 'module-9', 'module-10'
}

# Couleurs de la charte graphique
COLORS = {
    'primary': '#8FAFB1',      # Mer (Bleu-Vert Doux)
    'secondary': '#C8D0C3',    # Vert Sauge Clair
    'beige': '#D8CDBB',        # Beige Sable
    'sable': '#E6D7C3',        # Sable
    'white': '#FFFFFF',        # Blanc Pur (fond)
    'text': '#333333',         # Texte principal
    
    # Couleurs des catégories du quiz
    'sommeil': '#7B68EE',
    'travail': '#4A90E2',
    'famille': '#FFD700',
    'taches': '#FF6B35',
    'solo': '#BD10E0',
    'social': '#00D9FF',
    'couple_cat': '#E74C3C'
}

# ============================================================================
# CLASSES PRINCIPALES
# ============================================================================

class FileInfo:
    """Représente un fichier avec ses métadonnées"""
    
    def __init__(self, path: Path, root_dir: Path):
        self.path = path
        self.name = path.name
        self.relative_path = path.relative_to(root_dir)
        self.extension = path.suffix.lower()
        self.size = path.stat().st_size if path.exists() else 0
        self.modified = datetime.fromtimestamp(path.stat().st_mtime)
        self.category = self._get_category()
        self.tags = set()
        self.content_preview = ""
        
        # Extraire tags et contenu
        if self.extension in {'.html', '.htm'}:
            self._extract_html_info()
        
        # Extraire tags du nom de fichier et du chemin
        self._extract_filename_tags()
    
    def _get_category(self) -> str:
        """Détermine la catégorie du fichier"""
        for category, extensions in FILE_CATEGORIES.items():
            if self.extension in extensions:
                return category
        return 'other'
    
    def _extract_html_info(self):
        """Extrait les infos d'un fichier HTML"""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
                # Extraire le titre
                title = soup.find('title')
                if title:
                    self.content_preview = title.get_text().strip()
                
                # Extraire meta keywords
                meta_keywords = soup.find('meta', {'name': 'keywords'})
                if meta_keywords:
                    keywords = meta_keywords.get('content', '').split(',')
                    for keyword in keywords:
                        keyword = keyword.strip().lower()
                        if keyword in COUPLE_TAGS:
                            self.tags.add(keyword)
                
                # Extraire meta description
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc and not self.content_preview:
                    self.content_preview = meta_desc.get('content', '').strip()[:200]
                
                # Chercher dans le contenu
                text_content = soup.get_text().lower()
                for tag in COUPLE_TAGS:
                    if tag in text_content:
                        self.tags.add(tag)
                        
        except Exception as e:
            print(f"⚠️  Erreur lecture HTML {self.path}: {e}")
    
    def _extract_filename_tags(self):
        """Extrait les tags du nom de fichier et du chemin"""
        # Nom de fichier en minuscules
        filename_lower = self.name.lower()
        path_lower = str(self.relative_path).lower()
        
        # Chercher les tags
        for tag in COUPLE_TAGS:
            if tag in filename_lower or tag in path_lower:
                self.tags.add(tag)
    
    def get_icon(self) -> str:
        """Retourne l'icône emoji selon la catégorie"""
        icons = {
            'quiz': '📝',
            'web': '🌐',
            'image': '🖼️',
            'document': '📄',
            'data': '📊',
            'other': '📁'
        }
        return icons.get(self.category, '📁')
    
    def format_size(self) -> str:
        """Formate la taille en Ko, Mo, etc."""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_url(self, base_url: str) -> str:
        """Construit l'URL complète du fichier"""
        from urllib.parse import quote
        path_str = str(self.relative_path).replace('\\', '/')
        return f"{base_url}/{quote(path_str)}"
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour JSON"""
        return {
            'name': self.name,
            'path': str(self.relative_path).replace('\\', '/'),
            'category': self.category,
            'extension': self.extension,
            'size': self.size,
            'size_formatted': self.format_size(),
            'modified': self.modified.strftime('%Y-%m-%d %H:%M'),
            'tags': list(self.tags),
            'preview': self.content_preview,
            'icon': self.get_icon()
        }


class DirectoryScanner:
    """Scanne récursivement les répertoires"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.files: List[FileInfo] = []
        self.directories: Set[Path] = set()
    
    def scan(self):
        """Scanne tous les fichiers et dossiers"""
        print(f"🔍 Scan de {self.root_dir}...")
        
        for item in self.root_dir.rglob('*'):
            # Ignorer certains dossiers
            if any(ignored in item.parts for ignored in IGNORE_DIRS):
                continue
            
            if item.is_file():
                # Ignorer certains fichiers
                if item.name in IGNORE_FILES:
                    continue
                
                # Ignorer les index.html existants (on va les régénérer)
                if item.name == 'index.html':
                    continue
                
                file_info = FileInfo(item, self.root_dir)
                self.files.append(file_info)
            
            elif item.is_dir():
                self.directories.add(item)
        
        print(f"✅ Trouvé {len(self.files)} fichiers dans {len(self.directories)} dossiers")
    
    def get_files_by_category(self, category: str) -> List[FileInfo]:
        """Retourne les fichiers d'une catégorie"""
        return [f for f in self.files if f.category == category]
    
    def get_files_in_directory(self, directory: Path) -> List[FileInfo]:
        """Retourne les fichiers d'un dossier spécifique"""
        return [f for f in self.files if f.path.parent == directory]
    
    def get_subdirectories(self, directory: Path) -> List[Path]:
        """Retourne les sous-dossiers directs"""
        return sorted([d for d in self.directories if d.parent == directory])


class IndexGenerator:
    """Génère les fichiers index.html"""
    
    def __init__(self, scanner: DirectoryScanner, base_url: str):
        self.scanner = scanner
        self.base_url = base_url
    
    def generate_all(self):
        """Génère tous les index"""
        print("\n📝 Génération des index...")
        
        # Index racine
        self.generate_root_index()
        
        # Index par dossier
        for directory in self.scanner.directories:
            self.generate_directory_index(directory)
        
        print("✅ Tous les index générés")
    
    def generate_root_index(self):
        """Génère l'index.html à la racine"""
        print("📄 Génération de l'index racine...")
        
        # Statistiques
        total_files = len(self.scanner.files)
        total_size = sum(f.size for f in self.scanner.files)
        html_files = len([f for f in self.scanner.files if f.extension in {'.html', '.htm'}])
        quiz_files = len([f for f in self.scanner.files if 'quiz' in str(f.relative_path).lower() or 'questionnaire' in str(f.relative_path).lower()])
        
        # Préparer les données JSON
        files_data = [f.to_dict() for f in self.scanner.files]
        
        # Générer le HTML
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Institut du Couple - Bibliothèque Complète</title>
    <meta name="description" content="Base de connaissances et ressources pour la formation Bilan de Compétences du Couple">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {COLORS['white']};
            padding: 20px;
            line-height: 1.6;
            color: {COLORS['text']};
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: {COLORS['white']};
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 48px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            font-weight: 700;
        }}
        
        .subtitle {{
            font-size: 20px;
            opacity: 0.95;
            margin-top: 10px;
            font-weight: 500;
        }}
        
        .update-info {{
            margin-top: 20px;
            font-size: 14px;
            opacity: 0.9;
            font-weight: 400;
        }}
        
        .search-bar {{
            position: sticky;
            top: 0;
            background: {COLORS['white']};
            padding: 20px 40px;
            border-bottom: 3px solid {COLORS['primary']};
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        #searchInput {{
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid {COLORS['primary']};
            border-radius: 10px;
            outline: none;
            transition: all 0.3s;
            font-family: 'Montserrat', sans-serif;
        }}
        
        #searchInput:focus {{
            box-shadow: 0 0 0 3px rgba(143, 175, 177, 0.2);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: {COLORS['sable']};
        }}
        
        .stat-card {{
            background: {COLORS['white']};
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-top: 4px solid {COLORS['primary']};
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: 700;
            color: {COLORS['primary']};
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        
        main {{
            padding: 40px;
            background: {COLORS['white']};
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid {COLORS['primary']};
        }}
        
        .section-title {{
            font-size: 28px;
            color: {COLORS['primary']};
            font-weight: 600;
        }}
        
        .section-count {{
            background: {COLORS['primary']};
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .file-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .file-card {{
            background: linear-gradient(135deg, {COLORS['sable']} 0%, {COLORS['beige']} 100%);
            border: 2px solid {COLORS['secondary']};
            border-left: 4px solid {COLORS['primary']};
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        .file-card:hover {{
            border-color: {COLORS['primary']};
            box-shadow: 0 8px 20px rgba(143, 175, 177, 0.3);
            transform: translateY(-3px);
        }}
        
        .file-icon {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .file-name {{
            font-weight: 600;
            color: {COLORS['text']};
            margin-bottom: 8px;
            word-break: break-word;
        }}
        
        .file-meta {{
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .file-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 10px;
        }}
        
        .tag {{
            background: {COLORS['primary']};
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        
        footer {{
            background: {COLORS['text']};
            color: white;
            text-align: center;
            padding: 40px 20px;
            font-size: 11px;
            font-weight: 400;
        }}
        
        footer a {{
            color: {COLORS['primary']};
            text-decoration: none;
        }}
        
        .directory-section {{
            margin-top: 30px;
        }}
        
        .directory-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .directory-card {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['secondary']};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        .directory-card:hover {{
            border-color: {COLORS['primary']};
            box-shadow: 0 4px 15px rgba(143, 175, 177, 0.2);
            transform: translateY(-2px);
        }}
        
        .directory-icon {{
            font-size: 40px;
            margin-bottom: 10px;
        }}
        
        .directory-name {{
            font-weight: 600;
            color: {COLORS['text']};
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💑 Institut du Couple</h1>
            <div class="subtitle">
                Base de Connaissances et Ressources Pédagogiques
            </div>
            <div class="update-info">
                📅 Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </header>
        
        <div class="search-bar">
            <input 
                type="text" 
                id="searchInput" 
                placeholder="🔍 Rechercher par nom, contenu ou tags (ex: communication, module-1, exercice)..."
            >
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_files}</div>
                <div class="stat-label">Fichiers Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{html_files}</div>
                <div class="stat-label">Pages HTML</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{quiz_files}</div>
                <div class="stat-label">Quiz & Exercices</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{FileInfo(Path('.'), self.scanner.root_dir).format_size() if total_size > 0 else '0 B'}</div>
                <div class="stat-label">Taille Totale</div>
            </div>
        </div>
        
        <main id="mainContent">
            <div class="section">
                <div class="section-header">
                    <span class="section-title">📝 Tous les Fichiers</span>
                    <span class="section-count" id="totalCount">{total_files}</span>
                </div>
                <div class="file-grid" id="fileGrid">
                    <!-- Les fichiers seront insérés ici par JavaScript -->
                </div>
            </div>
            
            <div class="directory-section">
                <div class="section-header">
                    <span class="section-title">📁 Navigation par Module</span>
                </div>
                <div class="directory-grid" id="directoryGrid">
                    <!-- Les dossiers seront insérés ici par JavaScript -->
                </div>
            </div>
        </main>
        
        <footer>
            <p><strong>Institut du Couple - Système de Bibliothèque Automatisé v1.0.0</strong></p>
            <p style="margin-top: 10px;">
                🤖 Index généré automatiquement par GitHub Actions
            </p>
            <p style="margin-top: 15px;">
                <a href="https://github.com/11drumboy11/institut-du-couple" target="_blank">
                    📂 Voir sur GitHub
                </a>
            </p>
            <p style="margin-top: 20px;">
                Bilan de Compétences du Couple© - Marie-Christine Abatte Psychologue
            </p>
        </footer>
    </div>
    
    <script>
        // Données des fichiers
        const filesData = {json.dumps(files_data, ensure_ascii=False, indent=2)};
        
        // Afficher tous les fichiers
        function displayFiles(files) {{
            const grid = document.getElementById('fileGrid');
            const totalCount = document.getElementById('totalCount');
            
            grid.innerHTML = '';
            totalCount.textContent = files.length;
            
            files.forEach(file => {{
                const card = document.createElement('div');
                card.className = 'file-card';
                card.onclick = () => window.open('{self.base_url}/' + file.path, '_blank');
                
                const tagsHtml = file.tags.map(tag => `<span class="tag">${{tag}}</span>`).join('');
                
                card.innerHTML = `
                    <div class="file-icon">${{file.icon}}</div>
                    <div class="file-name">${{file.name}}</div>
                    ${{file.preview ? `<div class="file-meta">📄 ${{file.preview}}</div>` : ''}}
                    <div class="file-meta">
                        📁 ${{file.size_formatted}} | 📅 ${{file.modified}}
                    </div>
                    ${{tagsHtml ? `<div class="file-tags">${{tagsHtml}}</div>` : ''}}
                `;
                
                grid.appendChild(card);
            }});
        }}
        
        // Recherche
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase().trim();
            
            if (!query) {{
                displayFiles(filesData);
                return;
            }}
            
            const filtered = filesData.filter(file => {{
                const nameMatch = file.name.toLowerCase().includes(query);
                const pathMatch = file.path.toLowerCase().includes(query);
                const previewMatch = file.preview && file.preview.toLowerCase().includes(query);
                const tagsMatch = file.tags.some(tag => tag.toLowerCase().includes(query));
                
                return nameMatch || pathMatch || previewMatch || tagsMatch;
            }});
            
            displayFiles(filtered);
        }});
        
        // Affichage initial
        displayFiles(filesData);
        
        // Afficher les dossiers de modules
        const directories = Array.from(new Set(filesData.map(f => f.path.split('/')[0]))).filter(d => d);
        const directoryGrid = document.getElementById('directoryGrid');
        
        directories.forEach(dir => {{
            const card = document.createElement('div');
            card.className = 'directory-card';
            card.onclick = () => window.location.href = '{self.base_url}/' + dir + '/index.html';
            
            card.innerHTML = `
                <div class="directory-icon">📂</div>
                <div class="directory-name">${{dir}}</div>
            `;
            
            directoryGrid.appendChild(card);
        }});
    </script>
</body>
</html>"""
        
        # Écrire le fichier
        output_path = self.scanner.root_dir / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Index racine créé : {output_path}")
    
    def generate_directory_index(self, directory: Path):
        """Génère l'index.html pour un dossier"""
        files = self.scanner.get_files_in_directory(directory)
        subdirs = self.scanner.get_subdirectories(directory)
        
        # Si pas de fichiers ni de sous-dossiers, on ne crée pas d'index
        if not files and not subdirs:
            return
        
        # Nom du dossier
        dir_name = directory.name
        relative_path = directory.relative_to(self.scanner.root_dir)
        
        # Générer le HTML
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{dir_name} - Institut du Couple</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {COLORS['white']};
            padding: 20px;
            color: {COLORS['text']};
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {COLORS['white']};
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 40px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid {COLORS['primary']};
        }}
        
        h1 {{
            color: {COLORS['primary']};
            font-size: 36px;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .breadcrumb {{
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }}
        
        .breadcrumb a {{
            color: {COLORS['primary']};
            text-decoration: none;
        }}
        
        .section {{
            margin: 30px 0;
        }}
        
        .section-title {{
            color: {COLORS['primary']};
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid {COLORS['secondary']};
            font-weight: 600;
        }}
        
        .file-list {{
            list-style: none;
        }}
        
        .file-item {{
            background: linear-gradient(135deg, {COLORS['sable']} 0%, {COLORS['beige']} 100%);
            border-left: 4px solid {COLORS['primary']};
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        
        .file-item:hover {{
            box-shadow: 0 4px 15px rgba(143, 175, 177, 0.2);
            transform: translateX(5px);
        }}
        
        .file-item a {{
            color: {COLORS['text']};
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
        }}
        
        .file-icon {{
            font-size: 24px;
        }}
        
        .folder-item {{
            background: {COLORS['white']};
            border: 2px solid {COLORS['secondary']};
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        
        .folder-item:hover {{
            border-color: {COLORS['primary']};
            box-shadow: 0 4px 15px rgba(143, 175, 177, 0.2);
        }}
        
        .folder-item a {{
            color: {COLORS['text']};
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }}
        
        .back-button {{
            background: {COLORS['primary']};
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 30px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .back-button:hover {{
            background: {COLORS['secondary']};
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="{self.base_url}/index.html" class="back-button">← Retour à l'accueil</a>
        
        <header>
            <h1>📁 {dir_name}</h1>
            <div class="breadcrumb">
                <a href="{self.base_url}/index.html">Accueil</a> / {relative_path}
            </div>
        </header>
        
        {self._generate_subdirs_section(subdirs) if subdirs else ''}
        
        {self._generate_files_section(files) if files else ''}
    </div>
</body>
</html>"""
        
        # Écrire le fichier
        output_path = directory / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Index créé : {output_path}")
    
    def _generate_subdirs_section(self, subdirs: List[Path]) -> str:
        """Génère la section des sous-dossiers"""
        items = []
        for subdir in subdirs:
            rel_path = subdir.relative_to(self.scanner.root_dir)
            items.append(f"""
                <li class="folder-item">
                    <a href="{self.base_url}/{rel_path}/index.html">
                        <span class="file-icon">📂</span>
                        <span>{subdir.name}</span>
                    </a>
                </li>
            """)
        
        return f"""
        <div class="section">
            <h2 class="section-title">📂 Sous-dossiers ({len(subdirs)})</h2>
            <ul class="file-list">
                {''.join(items)}
            </ul>
        </div>
        """
    
    def _generate_files_section(self, files: List[FileInfo]) -> str:
        """Génère la section des fichiers"""
        items = []
        for file_info in sorted(files, key=lambda f: f.name):
            items.append(f"""
                <li class="file-item">
                    <a href="{file_info.get_url(self.base_url)}">
                        <span class="file-icon">{file_info.get_icon()}</span>
                        <span>{file_info.name}</span>
                        <span style="margin-left: auto; font-size: 12px; color: #666;">
                            {file_info.format_size()}
                        </span>
                    </a>
                </li>
            """)
        
        return f"""
        <div class="section">
            <h2 class="section-title">📄 Fichiers ({len(files)})</h2>
            <ul class="file-list">
                {''.join(items)}
            </ul>
        </div>
        """


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale"""
    print("=" * 60)
    print("💑 Institut du Couple - Générateur d'Index Automatique")
    print("=" * 60)
    print()
    
    # Déterminer le répertoire racine
    root_dir = Path.cwd()
    print(f"📂 Répertoire racine : {root_dir}")
    
    # URL de base GitHub Pages
    base_url = "https://11drumboy11.github.io/institut-du-couple"
    print(f"🌐 URL de base : {base_url}")
    print()
    
    # Scanner
    scanner = DirectoryScanner(root_dir)
    scanner.scan()
    print()
    
    # Générer les index
    generator = IndexGenerator(scanner, base_url)
    generator.generate_all()
    print()
    
    print("=" * 60)
    print("✅ TERMINÉ ! Tous les index ont été générés.")
    print("=" * 60)


if __name__ == "__main__":
    main()
