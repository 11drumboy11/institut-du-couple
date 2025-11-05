#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'index automatique pour l'Institut du Couple
Crée des pages d'index pour chaque module et la page d'accueil principale
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Configuration
REPO_ROOT = "."
MODULES = [f"Module {i}" for i in range(11)] + ["Outils"]
BASE_URL = "https://11drumboy11.github.io/institut-du-couple/"

# Catégories de fichiers
FILE_CATEGORIES = {
    '.html': {'icon': '📄', 'category': 'quiz', 'label': 'Page Interactive'},
    '.pdf': {'icon': '📕', 'category': 'document', 'label': 'Document PDF'},
    '.docx': {'icon': '📝', 'category': 'document', 'label': 'Document Word'},
    '.md': {'icon': '📋', 'category': 'other', 'label': 'Documentation'},
    '.mp4': {'icon': '🎬', 'category': 'media', 'label': 'Vidéo'},
    '.jpg': {'icon': '🖼️', 'category': 'media', 'label': 'Image'},
    '.png': {'icon': '🖼️', 'category': 'media', 'label': 'Image'},
}

def get_file_info(filepath):
    """Récupère les informations d'un fichier"""
    stat = os.stat(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    
    info = FILE_CATEGORIES.get(ext, {'icon': '📄', 'category': 'other', 'label': 'Fichier'})
    
    return {
        'name': os.path.basename(filepath),
        'path': filepath,
        'extension': ext,
        'size': stat.st_size,
        'size_formatted': format_size(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
        'icon': info['icon'],
        'category': info['category'],
        'label': info['label']
    }

def format_size(size):
    """Formate la taille en Ko, Mo, etc."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def scan_module(module_path):
    """Scanne un module et retourne la liste des fichiers"""
    files = []
    
    if not os.path.exists(module_path):
        return files
    
    for item in os.listdir(module_path):
        if item.startswith('.') or item == '__pycache__':
            continue
            
        item_path = os.path.join(module_path, item)
        
        if os.path.isfile(item_path):
            files.append(get_file_info(item_path))
    
    return sorted(files, key=lambda x: x['name'].lower())

def generate_module_index(module_name, files):
    """Génère la page d'index pour un module"""
    
    module_number = module_name.replace("Module ", "").replace("Outils", "Outils")
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - Institut du Couple</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Montserrat', sans-serif;
            background: #FFFFFF;
            color: #333333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #8FAFB1 0%, #C8D0C3 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.95;
        }}
        
        .nav-back {{
            background: #E6D7C3;
            padding: 15px 20px;
            border-bottom: 3px solid #8FAFB1;
        }}
        
        .nav-back a {{
            color: #8FAFB1;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            transition: color 0.3s;
        }}
        
        .nav-back a:hover {{
            color: #C8D0C3;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border-left: 4px solid #8FAFB1;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: 700;
            color: #8FAFB1;
        }}
        
        .stat-label {{
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        
        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .file-card {{
            background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%);
            border-left: 4px solid #8FAFB1;
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .file-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(143, 175, 177, 0.3);
        }}
        
        .file-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .file-name {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
        }}
        
        .file-meta {{
            font-size: 0.85em;
            color: #666;
        }}
        
        .file-label {{
            display: inline-block;
            background: #8FAFB1;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            margin-top: 10px;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}
        
        .empty-state-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        
        footer {{
            background: #333333;
            color: white;
            text-align: center;
            padding: 30px 20px;
            margin-top: 60px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .files-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{module_name}</h1>
        <div class="subtitle">Institut du Couple - Bilan de Compétences du Couple</div>
    </div>
    
    <div class="nav-back">
        <a href="../index.html">← Retour à l'accueil</a>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(files)}</div>
                <div class="stat-label">Ressources</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([f for f in files if f['extension'] == '.html'])}</div>
                <div class="stat-label">Pages Interactives</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([f for f in files if f['extension'] in ['.pdf', '.docx']])}</div>
                <div class="stat-label">Documents</div>
            </div>
        </div>
"""

    if files:
        html += """        <div class="files-grid">\n"""
        
        for file in files:
            # Construire le chemin relatif
            file_path = file['path'].replace('\\', '/')
            
            html += f"""            <div class="file-card" onclick="window.open('{file_path}', '_blank')">
                <div class="file-icon">{file['icon']}</div>
                <div class="file-name">{file['name']}</div>
                <div class="file-meta">{file['size_formatted']} • {file['modified']}</div>
                <div class="file-label">{file['label']}</div>
            </div>\n"""
        
        html += """        </div>\n"""
    else:
        html += """        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h2>Aucune ressource disponible</h2>
            <p>Ce module ne contient pas encore de contenu.</p>
        </div>\n"""

    html += f"""    </div>
    
    <footer>
        <p>Institut du Couple - Marie-Christine Abatte Psychologue</p>
        <p style="margin-top: 10px; font-size: 0.85em;">Généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
    </footer>
</body>
</html>"""

    return html

def generate_main_index(all_modules_data):
    """Génère la page d'accueil principale avec tous les modules"""
    
    total_files = sum(len(data['files']) for data in all_modules_data.values())
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Institut du Couple - Bibliothèque de Formation</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: #FFFFFF;
            color: #333333;
            line-height: 1.6;
        }
        
        .hero {
            background: linear-gradient(135deg, #8FAFB1 0%, #C8D0C3 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .hero h1 {
            font-size: 3em;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .hero .tagline {
            font-size: 1.3em;
            opacity: 0.95;
            margin-bottom: 30px;
        }
        
        .hero .cta {
            background: white;
            color: #8FAFB1;
            padding: 15px 40px;
            border-radius: 30px;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
            transition: transform 0.3s;
        }
        
        .hero .cta:hover {
            transform: scale(1.05);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .section-title {
            font-size: 2em;
            color: #8FAFB1;
            margin: 40px 0 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #C8D0C3;
            font-weight: 600;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            border-top: 4px solid #8FAFB1;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 3em;
            font-weight: 700;
            color: #8FAFB1;
        }
        
        .stat-label {
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .modules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .module-card {
            background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%);
            border-left: 4px solid #8FAFB1;
            border-radius: 15px;
            padding: 30px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            display: block;
        }
        
        .module-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(143, 175, 177, 0.4);
        }
        
        .module-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .module-icon {
            font-size: 2.5em;
        }
        
        .module-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #8FAFB1;
        }
        
        .module-count {
            background: #8FAFB1;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            display: inline-block;
            margin-top: 15px;
        }
        
        .tools-section {
            background: #E6D7C3;
            border-radius: 15px;
            padding: 40px;
            margin-top: 50px;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        
        .tool-card {
            background: white;
            border-left: 4px solid #8FAFB1;
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            display: block;
        }
        
        .tool-card:hover {
            transform: translateX(8px);
            box-shadow: 0 6px 20px rgba(143, 175, 177, 0.3);
        }
        
        .tool-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .tool-name {
            font-weight: 600;
            color: #8FAFB1;
            font-size: 1.1em;
        }
        
        footer {
            background: #333333;
            color: white;
            text-align: center;
            padding: 40px 20px;
            margin-top: 80px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2em; }
            .modules-grid { grid-template-columns: 1fr; }
            .tools-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Institut du Couple</h1>
        <div class="tagline">Bibliothèque de Formation et Ressources</div>
        <div style="margin-top: 20px; font-size: 0.9em; opacity: 0.9;">
            Marie-Christine Abatte - Psychologue
        </div>
    </div>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">11</div>
                <div class="stat-label">Modules de Formation</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(total_files) + """</div>
                <div class="stat-label">Ressources Totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len([f for data in all_modules_data.values() for f in data['files'] if f['extension'] == '.html'])) + """</div>
                <div class="stat-label">Outils Interactifs</div>
            </div>
        </div>
        
        <h2 class="section-title">Modules de Formation</h2>
        <div class="modules-grid">
"""
    
    # Générer les cartes des modules
    for i in range(11):
        module_name = f"Module {i}"
        module_data = all_modules_data.get(module_name, {'files': []})
        file_count = len(module_data['files'])
        
        html += f"""            <a href="{module_name}/index.html" class="module-card">
                <div class="module-header">
                    <div class="module-icon">📚</div>
                    <div class="module-title">{module_name}</div>
                </div>
                <div class="module-count">{file_count} ressource{'s' if file_count > 1 else ''}</div>
            </a>
"""
    
    html += """        </div>
        
        <div class="tools-section">
            <h2 class="section-title" style="border-color: #8FAFB1; color: #8FAFB1;">Outils et Questionnaires</h2>
            <div class="tools-grid">
"""
    
    # Ajouter les outils du dossier Outils
    if "Outils" in all_modules_data:
        for file in all_modules_data["Outils"]['files']:
            if file['extension'] == '.html':
                html += f"""                <a href="{file['path']}" class="tool-card" target="_blank">
                    <div class="tool-icon">{file['icon']}</div>
                    <div class="tool-name">{file['name'].replace('.html', '')}</div>
                </a>
"""
    
    html += f"""            </div>
        </div>
    </div>
    
    <footer>
        <p>Institut du Couple - Bilan de Compétences du Couple</p>
        <p style="margin-top: 10px;">Marie-Christine Abatte Psychologue</p>
        <p style="margin-top: 15px; font-size: 0.85em; opacity: 0.8;">
            Généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        </p>
    </footer>
</body>
</html>"""
    
    return html

def main():
    """Fonction principale"""
    print("🚀 Génération des index de modules...")
    print("=" * 50)
    
    all_modules_data = {}
    
    # Scanner et générer l'index pour chaque module
    for module_name in MODULES:
        module_path = os.path.join(REPO_ROOT, module_name)
        
        print(f"\n📁 Traitement : {module_name}")
        
        # Scanner les fichiers
        files = scan_module(module_path)
        all_modules_data[module_name] = {'files': files}
        
        print(f"   ✓ {len(files)} fichier(s) trouvé(s)")
        
        # Générer l'index du module
        if os.path.exists(module_path):
            index_html = generate_module_index(module_name, files)
            index_path = os.path.join(module_path, "index.html")
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            print(f"   ✓ Index créé : {index_path}")
    
    # Générer la page d'accueil principale
    print(f"\n🏠 Génération de la page d'accueil principale...")
    main_index_html = generate_main_index(all_modules_data)
    main_index_path = os.path.join(REPO_ROOT, "index.html")
    
    with open(main_index_path, 'w', encoding='utf-8') as f:
        f.write(main_index_html)
    
    print(f"   ✓ Page d'accueil créée : {main_index_path}")
    
    print("\n" + "=" * 50)
    print("✅ Génération terminée avec succès !")
    print(f"📊 Total : {len(MODULES)} modules traités")
    print(f"📄 Total : {sum(len(data['files']) for data in all_modules_data.values())} fichiers indexés")

if __name__ == "__main__":
    main()
