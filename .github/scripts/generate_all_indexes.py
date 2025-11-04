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
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️  BeautifulSoup non installé. Installation...")
    os.system("pip install beautifulsoup4 lxml")
    from bs4 import BeautifulSoup

# ============================================================================
# CONFIGURATION
# ============================================================================

# Dossiers et fichiers à ignorer
IGNORE_DIRS = {'.git', '.github', 'node_modules', '__pycache__', '.DS_Store'}
IGNORE_FILES = {'.gitignore', 'README.md', '.gitattributes', 'CNAME', 'generate_all_indexes.py'}

# Extensions de fichiers par catégorie
FILE_CATEGORIES = {
    'quiz': {'.html'},
    'image': {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'},
    'document': {'.pdf', '.doc', '.docx'},
    'web': {'.html', '.htm', '.css', '.js'},
    'data': {'.json', '.xml', '.csv', '.txt'}
}

# Tags thématiques pour l'Institut du Couple
COUPLE_TAGS = {
    'sommeil', 'travail', 'famille', 'taches', 'solo', 'social', 'couple',
    'communication', 'organisation', 'intimite', 'sexualite',
    'gestion', 'conflits', 'emotions', 'temps', 'activites',
    'famille-origine', 'enfants', 'loisirs', 'quotidien',
    'debutant', 'intermediaire', 'avance', 'exercice',
    'questionnaire', 'ressource', 'documentation',
    'module-1', 'module-2', 'module-3', 'module-4', 'module-5',
    'module-6', 'module-7', 'module-8', 'module-9', 'module-10'
}

# Couleurs de la charte graphique
COLORS = {
    'primary': '#8FAFB1',
    'secondary': '#C8D0C3',
    'beige': '#D8CDBB',
    'sable': '#E6D7C3',
    'white': '#FFFFFF',
    'text': '#333333',
}

# ============================================================================
# CLASSES
# ============================================================================

class FileInfo:
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
        
        if self.extension in {'.html', '.htm'}:
            self._extract_html_info()
        self._extract_filename_tags()
    
    def _get_category(self) -> str:
        for category, extensions in FILE_CATEGORIES.items():
            if self.extension in extensions:
                return category
        return 'other'
    
    def _extract_html_info(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                title = soup.find('title')
                if title:
                    self.content_preview = title.get_text().strip()
                
                meta_keywords = soup.find('meta', {'name': 'keywords'})
                if meta_keywords:
                    keywords = meta_keywords.get('content', '').split(',')
                    for keyword in keywords:
                        keyword = keyword.strip().lower()
                        if keyword in COUPLE_TAGS:
                            self.tags.add(keyword)
        except Exception as e:
            print(f"⚠️  Erreur lecture {self.path}: {e}")
    
    def _extract_filename_tags(self):
        filename_lower = self.name.lower()
        path_lower = str(self.relative_path).lower()
        for tag in COUPLE_TAGS:
            if tag in filename_lower or tag in path_lower:
                self.tags.add(tag)
    
    def get_icon(self) -> str:
        icons = {'quiz': '📝', 'web': '🌐', 'image': '🖼️', 'document': '📄', 'data': '📊', 'other': '📁'}
        return icons.get(self.category, '📁')
    
    def format_size(self) -> str:
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_url(self, base_url: str) -> str:
        from urllib.parse import quote
        path_str = str(self.relative_path).replace('\\', '/')
        return f"{base_url}/{quote(path_str)}"
    
    def to_dict(self) -> dict:
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
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.files: List[FileInfo] = []
        self.directories: Set[Path] = set()
    
    def scan(self):
        print(f"🔍 Scan de {self.root_dir}...")
        for item in self.root_dir.rglob('*'):
            if any(ignored in item.parts for ignored in IGNORE_DIRS):
                continue
            if item.is_file():
                if item.name in IGNORE_FILES or item.name == 'index.html':
                    continue
                self.files.append(FileInfo(item, self.root_dir))
            elif item.is_dir():
                self.directories.add(item)
        print(f"✅ Trouvé {len(self.files)} fichiers dans {len(self.directories)} dossiers")
    
    def get_files_in_directory(self, directory: Path) -> List[FileInfo]:
        return [f for f in self.files if f.path.parent == directory]
    
    def get_subdirectories(self, directory: Path) -> List[Path]:
        return sorted([d for d in self.directories if d.parent == directory])

class IndexGenerator:
    def __init__(self, scanner: DirectoryScanner, base_url: str):
        self.scanner = scanner
        self.base_url = base_url
    
    def generate_all(self):
        print("\n📝 Génération des index...")
        self.generate_root_index()
        for directory in self.scanner.directories:
            self.generate_directory_index(directory)
        print("✅ Tous les index générés")
    
    def generate_root_index(self):
        print("📄 Génération de l'index racine...")
        total_files = len(self.scanner.files)
        total_size = sum(f.size for f in self.scanner.files)
        html_files = len([f for f in self.scanner.files if f.extension in {'.html', '.htm'}])
        
        files_data = [f.to_dict() for f in self.scanner.files]
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Institut du Couple - Bibliothèque</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: {COLORS['white']}; padding: 20px; color: {COLORS['text']}; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: {COLORS['white']}; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); overflow: hidden; }}
        header {{ background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); color: white; padding: 60px 40px; text-align: center; }}
        header h1 {{ font-size: 48px; margin-bottom: 15px; font-weight: 700; }}
        .subtitle {{ font-size: 20px; opacity: 0.95; margin-top: 10px; }}
        .search-bar {{ position: sticky; top: 0; background: {COLORS['white']}; padding: 20px 40px; border-bottom: 3px solid {COLORS['primary']}; z-index: 1000; }}
        #searchInput {{ width: 100%; padding: 15px 20px; font-size: 16px; border: 2px solid {COLORS['primary']}; border-radius: 10px; font-family: 'Montserrat', sans-serif; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 40px; background: {COLORS['sable']}; }}
        .stat-card {{ background: {COLORS['white']}; padding: 25px; border-radius: 12px; text-align: center; border-top: 4px solid {COLORS['primary']}; }}
        .stat-number {{ font-size: 36px; font-weight: 700; color: {COLORS['primary']}; }}
        .stat-label {{ color: #666; font-size: 14px; text-transform: uppercase; font-weight: 600; }}
        main {{ padding: 40px; }}
        .section-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 3px solid {COLORS['primary']}; }}
        .section-title {{ font-size: 28px; color: {COLORS['primary']}; font-weight: 600; }}
        .file-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .file-card {{ background: linear-gradient(135deg, {COLORS['sable']} 0%, {COLORS['beige']} 100%); border-left: 4px solid {COLORS['primary']}; border-radius: 12px; padding: 20px; cursor: pointer; transition: all 0.3s; }}
        .file-card:hover {{ box-shadow: 0 8px 20px rgba(143, 175, 177, 0.3); transform: translateY(-3px); }}
        .file-icon {{ font-size: 32px; margin-bottom: 10px; }}
        .file-name {{ font-weight: 600; margin-bottom: 8px; }}
        .file-tags {{ display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }}
        .tag {{ background: {COLORS['primary']}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
        footer {{ background: {COLORS['text']}; color: white; text-align: center; padding: 40px 20px; font-size: 11px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💑 Institut du Couple</h1>
            <div class="subtitle">Base de Connaissances et Ressources</div>
            <div style="margin-top:20px; font-size:14px;">📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
        </header>
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="🔍 Rechercher...">
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">{total_files}</div><div class="stat-label">Fichiers</div></div>
            <div class="stat-card"><div class="stat-number">{html_files}</div><div class="stat-label">Pages HTML</div></div>
        </div>
        <main id="mainContent">
            <div class="section-header"><span class="section-title">📝 Tous les Fichiers</span></div>
            <div class="file-grid" id="fileGrid"></div>
        </main>
        <footer><p>Institut du Couple - Système Automatisé v1.0.0</p><p style="margin-top:10px;">Marie-Christine Abatte - Psychologue</p></footer>
    </div>
    <script>
        const filesData = {json.dumps(files_data, ensure_ascii=False)};
        function displayFiles(files) {{
            const grid = document.getElementById('fileGrid');
            grid.innerHTML = '';
            files.forEach(file => {{
                const card = document.createElement('div');
                card.className = 'file-card';
                card.onclick = () => window.open('{self.base_url}/' + file.path, '_blank');
                const tags = file.tags.map(t => `<span class="tag">${{t}}</span>`).join('');
                card.innerHTML = `<div class="file-icon">${{file.icon}}</div><div class="file-name">${{file.name}}</div><div class="file-tags">${{tags}}</div>`;
                grid.appendChild(card);
            }});
        }}
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const q = e.target.value.toLowerCase();
            if (!q) {{ displayFiles(filesData); return; }}
            const filtered = filesData.filter(f => f.name.toLowerCase().includes(q) || f.tags.some(t => t.includes(q)));
            displayFiles(filtered);
        }});
        displayFiles(filesData);
    </script>
</body>
</html>"""
        
        output_path = self.scanner.root_dir / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Index racine créé")
    
    def generate_directory_index(self, directory: Path):
        files = self.scanner.get_files_in_directory(directory)
        subdirs = self.scanner.get_subdirectories(directory)
        if not files and not subdirs:
            return
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{directory.name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: {COLORS['white']}; padding: 20px; color: {COLORS['text']}; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: {COLORS['white']}; border-radius: 20px; padding: 40px; }}
        h1 {{ color: {COLORS['primary']}; font-size: 36px; margin-bottom: 20px; }}
        .back-button {{ background: {COLORS['primary']}; color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; margin-bottom: 30px; }}
        .file-list {{ list-style: none; }}
        .file-item {{ background: linear-gradient(135deg, {COLORS['sable']} 0%, {COLORS['beige']} 100%); border-left: 4px solid {COLORS['primary']}; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .file-item a {{ color: {COLORS['text']}; text-decoration: none; display: flex; align-items: center; gap: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="{self.base_url}/index.html" class="back-button">← Retour</a>
        <h1>📁 {directory.name}</h1>
        <ul class="file-list">
            {''.join([f'<li class="file-item"><a href="{f.get_url(self.base_url)}"><span>{f.get_icon()}</span><span>{f.name}</span></a></li>' for f in files])}
        </ul>
    </div>
</body>
</html>"""
        
        output_path = directory / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Index créé : {directory.name}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("💑 Institut du Couple - Générateur d'Index")
    print("=" * 60)
    root_dir = Path.cwd()
    base_url = "https://11drumboy11.github.io/institut-du-couple"
    scanner = DirectoryScanner(root_dir)
    scanner.scan()
    generator = IndexGenerator(scanner, base_url)
    generator.generate_all()
    print("=" * 60)
    print("✅ TERMINÉ !")
    print("=" * 60)

if __name__ == "__main__":
    main()
