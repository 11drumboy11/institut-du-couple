#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'index automatique pour l'Institut du Couple - Version 2.0
✨ Nouveautés :
- Gère tous les types de fichiers (HTML, PDF, DOCX, images, vidéos)
- Scanne la racine ET les dossiers de modules
- Mise à jour automatique avec GitHub Actions
- Affichage des médias et documents
"""

import os
from datetime import datetime

# Configuration
REPO_ROOT = "."
MODULES = [f"Module {i}" for i in range(11)] + ["Outils"]

# Catégories de fichiers avec icônes et labels
FILE_CATEGORIES = {
    # Pages interactives
    '.html': {'icon': '📄', 'category': 'interactive', 'label': 'Page Interactive'},
    
    # Documents
    '.pdf': {'icon': '📕', 'category': 'document', 'label': 'Document PDF'},
    '.docx': {'icon': '📝', 'category': 'document', 'label': 'Document Word'},
    '.doc': {'icon': '📝', 'category': 'document', 'label': 'Document Word'},
    '.pptx': {'icon': '📊', 'category': 'document', 'label': 'Présentation'},
    '.xlsx': {'icon': '📈', 'category': 'document', 'label': 'Tableur Excel'},
    
    # Images
    '.jpg': {'icon': '🖼️', 'category': 'image', 'label': 'Image'},
    '.jpeg': {'icon': '🖼️', 'category': 'image', 'label': 'Image'},
    '.png': {'icon': '🖼️', 'category': 'image', 'label': 'Image'},
    '.gif': {'icon': '🖼️', 'category': 'image', 'label': 'Image Animée'},
    '.webp': {'icon': '🖼️', 'category': 'image', 'label': 'Image'},
    '.svg': {'icon': '🎨', 'category': 'image', 'label': 'Image Vectorielle'},
    
    # Vidéos
    '.mp4': {'icon': '🎬', 'category': 'video', 'label': 'Vidéo'},
    '.webm': {'icon': '🎬', 'category': 'video', 'label': 'Vidéo'},
    '.mov': {'icon': '🎬', 'category': 'video', 'label': 'Vidéo'},
    '.avi': {'icon': '🎬', 'category': 'video', 'label': 'Vidéo'},
    
    # Audio
    '.mp3': {'icon': '🎵', 'category': 'audio', 'label': 'Audio'},
    '.wav': {'icon': '🎵', 'category': 'audio', 'label': 'Audio'},
    
    # Documentation
    '.md': {'icon': '📋', 'category': 'doc', 'label': 'Documentation'},
    '.txt': {'icon': '📄', 'category': 'doc', 'label': 'Texte'},
    
    # Archives
    '.zip': {'icon': '📦', 'category': 'archive', 'label': 'Archive ZIP'},
}

def format_size(size):
    """Formate la taille en Ko, Mo, etc."""
    for unit in ['o', 'Ko', 'Mo', 'Go']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} To"

def get_file_info(filepath, repo_root="."):
    """Récupère les informations d'un fichier"""
    stat = os.stat(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    
    info = FILE_CATEGORIES.get(ext, {'icon': '📄', 'category': 'other', 'label': 'Fichier'})
    
    # Chemin relatif depuis la racine du repository
    rel_path = os.path.relpath(filepath, repo_root).replace('\\', '/')
    
    return {
        'name': os.path.basename(filepath),
        'path': rel_path,
        'extension': ext,
        'size': stat.st_size,
        'size_formatted': format_size(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
        'icon': info['icon'],
        'category': info['category'],
        'label': info['label']
    }

def scan_directory_recursive(directory, repo_root="."):
    """Scanne un dossier récursivement et retourne tous les fichiers"""
    files = []
    
    if not os.path.exists(directory):
        return files
    
    for root, dirs, filenames in os.walk(directory):
        # Ignorer les dossiers cachés et spéciaux
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
        
        for filename in filenames:
            # Ignorer les fichiers cachés, index.html et fichiers système
            if filename.startswith('.') or filename == 'index.html' or filename.endswith('.pyc'):
                continue
                
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            # Seulement les fichiers avec extensions reconnues
            if ext in FILE_CATEGORIES:
                files.append(get_file_info(filepath, repo_root))
    
    return sorted(files, key=lambda x: x['name'].lower())

def scan_root_files(repo_root="."):
    """Scanne les fichiers à la racine (pas dans les sous-dossiers)"""
    files = []
    
    if not os.path.exists(repo_root):
        return files
    
    for item in os.listdir(repo_root):
        item_path = os.path.join(repo_root, item)
        
        # Seulement les fichiers à la racine, pas les dossiers
        if os.path.isfile(item_path):
            # Ignorer les fichiers système et index.html
            if not item.startswith('.') and item != 'index.html' and not item.endswith('.py') and not item.endswith('.yml'):
                ext = os.path.splitext(item)[1].lower()
                # Seulement les fichiers intéressants
                if ext in FILE_CATEGORIES:
                    files.append(get_file_info(item_path, repo_root))
    
    return sorted(files, key=lambda x: x['name'].lower())

def generate_module_index(module_name, files, root_files):
    """Génère la page d'index pour un module avec tous les fichiers disponibles"""
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - Institut du Couple</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: #FFFFFF; color: #333333; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #8FAFB1 0%, #C8D0C3 100%); color: white; padding: 40px 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }}
        .header .subtitle {{ font-size: 1.2em; opacity: 0.95; }}
        .nav-back {{ background: #E6D7C3; padding: 15px 20px; border-bottom: 3px solid #8FAFB1; }}
        .nav-back a {{ color: #8FAFB1; text-decoration: none; font-weight: 600; font-size: 1.1em; transition: color 0.3s; }}
        .nav-back a:hover {{ color: #C8D0C3; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%); padding: 20px; border-radius: 12px; text-align: center; border-left: 4px solid #8FAFB1; }}
        .stat-number {{ font-size: 2em; font-weight: 700; color: #8FAFB1; }}
        .stat-label {{ color: #666; font-weight: 600; text-transform: uppercase; font-size: 0.85em; margin-top: 5px; }}
        .section-title {{ font-size: 1.6em; color: #8FAFB1; margin: 30px 0 20px; padding-bottom: 10px; border-bottom: 3px solid #C8D0C3; font-weight: 600; }}
        .files-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .file-card {{ background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%); border-left: 4px solid #8FAFB1; border-radius: 12px; padding: 20px; cursor: pointer; transition: all 0.3s; position: relative; }}
        .file-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(143, 175, 177, 0.3); }}
        .file-icon {{ font-size: 2.5em; margin-bottom: 10px; }}
        .file-name {{ font-weight: 600; margin-bottom: 8px; color: #333; word-break: break-word; }}
        .file-meta {{ font-size: 0.85em; color: #666; margin-bottom: 10px; }}
        .category-badge {{ position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 600; color: #8FAFB1; }}
        .empty-state {{ text-align: center; padding: 60px 20px; color: #999; }}
        .empty-state-icon {{ font-size: 4em; margin-bottom: 20px; }}
        footer {{ background: #333333; color: white; text-align: center; padding: 30px 20px; margin-top: 60px; font-size: 11px; }}
        @media (max-width: 768px) {{ .header h1 {{ font-size: 1.8em; }} .files-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{module_name}</h1>
        <div class="subtitle">Institut du Couple - Bilan de Compétences du Couple</div>
    </div>
    <div class="nav-back"><a href="../index.html">← Retour à l'accueil</a></div>
    <div class="container">
"""
    
    # Statistiques
    all_files = files + root_files
    interactive_count = len([f for f in all_files if f['category'] == 'interactive'])
    document_count = len([f for f in all_files if f['category'] == 'document'])
    media_count = len([f for f in all_files if f['category'] in ['image', 'video', 'audio']])
    
    html += f"""        <div class="stats">
            <div class="stat-card"><div class="stat-number">{len(all_files)}</div><div class="stat-label">Total</div></div>
            <div class="stat-card"><div class="stat-number">{interactive_count}</div><div class="stat-label">Pages</div></div>
            <div class="stat-card"><div class="stat-number">{document_count}</div><div class="stat-label">Documents</div></div>
            <div class="stat-card"><div class="stat-number">{media_count}</div><div class="stat-label">Médias</div></div>
        </div>
"""
    
    # Fichiers du module
    if files:
        html += f"""        <h2 class="section-title">Ressources dans {module_name}</h2><div class="files-grid">\n"""
        for file in files:
            relative_path = os.path.basename(file['path'])
            html += f"""            <div class="file-card" onclick="window.open('{relative_path}', '_blank')">
                <div class="category-badge">{file['label']}</div>
                <div class="file-icon">{file['icon']}</div>
                <div class="file-name">{file['name']}</div>
                <div class="file-meta">{file['size_formatted']} • {file['modified']}</div>
            </div>\n"""
        html += """        </div>\n"""
    
    # Fichiers de la racine (outils généraux)
    if root_files:
        html += """        <h2 class="section-title">Outils Généraux (Accessibles depuis tous les modules)</h2><div class="files-grid">\n"""
        for file in root_files:
            relative_path = '../' + file['path']
            html += f"""            <div class="file-card" onclick="window.open('{relative_path}', '_blank')">
                <div class="category-badge">{file['label']}</div>
                <div class="file-icon">{file['icon']}</div>
                <div class="file-name">{file['name']}</div>
                <div class="file-meta">{file['size_formatted']} • {file['modified']}</div>
            </div>\n"""
        html += """        </div>\n"""
    
    if not files and not root_files:
        html += """        <div class="empty-state"><div class="empty-state-icon">📭</div><h2>Aucune ressource disponible</h2><p>Ce module ne contient pas encore de contenu.</p></div>\n"""
    
    html += f"""    </div>
    <footer>
        <p>Institut du Couple - Marie-Christine Abatte Psychologue</p>
        <p style="margin-top: 10px;">Bilan de Compétences du Couple©</p>
        <p style="margin-top: 10px;">Généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
    </footer>
</body>
</html>"""
    
    return html

def generate_main_index(all_modules_data, root_files):
    """Génère la page d'accueil principale"""
    
    total_files = sum(len(data['files']) for data in all_modules_data.values()) + len(root_files)
    total_interactive = len([f for f in root_files if f['category'] == 'interactive'])
    total_documents = len([f for f in root_files if f['category'] == 'document'])
    total_media = len([f for f in root_files if f['category'] in ['image', 'video', 'audio']])
    
    for data in all_modules_data.values():
        total_interactive += len([f for f in data['files'] if f['category'] == 'interactive'])
        total_documents += len([f for f in data['files'] if f['category'] == 'document'])
        total_media += len([f for f in data['files'] if f['category'] in ['image', 'video', 'audio']])
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Institut du Couple - Bibliothèque de Formation</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Montserrat', sans-serif; background: #FFFFFF; color: #333333; line-height: 1.6; }
        .hero { background: linear-gradient(135deg, #8FAFB1 0%, #C8D0C3 100%); color: white; padding: 60px 20px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .hero h1 { font-size: 3em; margin-bottom: 15px; font-weight: 700; }
        .hero .tagline { font-size: 1.3em; opacity: 0.95; margin-bottom: 20px; }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
        .section-title { font-size: 2em; color: #8FAFB1; margin: 40px 0 30px; padding-bottom: 15px; border-bottom: 3px solid #C8D0C3; font-weight: 600; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin-bottom: 50px; }
        .stat-card { background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%); padding: 30px; border-radius: 15px; text-align: center; border-top: 4px solid #8FAFB1; transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 3em; font-weight: 700; color: #8FAFB1; }
        .stat-label { color: #666; font-weight: 600; text-transform: uppercase; font-size: 0.9em; margin-top: 10px; }
        .modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; margin-top: 30px; }
        .module-card { background: linear-gradient(135deg, #E6D7C3 0%, #D8CDBB 100%); border-left: 4px solid #8FAFB1; border-radius: 15px; padding: 30px; cursor: pointer; transition: all 0.3s; text-decoration: none; color: #333; display: block; }
        .module-card:hover { transform: translateY(-8px); box-shadow: 0 12px 30px rgba(143, 175, 177, 0.4); }
        .module-header { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; }
        .module-icon { font-size: 2.5em; }
        .module-title { font-size: 1.5em; font-weight: 600; color: #8FAFB1; }
        .module-count { background: #8FAFB1; color: white; padding: 8px 16px; border-radius: 20px; font-size: 0.9em; font-weight: 600; display: inline-block; margin-top: 15px; }
        .tools-section { background: #E6D7C3; border-radius: 15px; padding: 40px; margin-top: 50px; }
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; margin-top: 25px; }
        .tool-card { background: white; border-left: 4px solid #8FAFB1; border-radius: 12px; padding: 20px; cursor: pointer; transition: all 0.3s; text-decoration: none; color: #333; display: block; }
        .tool-card:hover { transform: translateX(8px); box-shadow: 0 6px 20px rgba(143, 175, 177, 0.3); }
        .tool-icon { font-size: 2em; margin-bottom: 10px; }
        .tool-name { font-weight: 600; color: #8FAFB1; font-size: 1.1em; }
        footer { background: #333333; color: white; text-align: center; padding: 40px 20px; margin-top: 80px; font-size: 11px; }
        @media (max-width: 768px) { .hero h1 { font-size: 2em; } .modules-grid { grid-template-columns: 1fr; } .tools-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Institut du Couple</h1>
        <div class="tagline">Bibliothèque de Formation et Ressources</div>
        <div style="margin-top: 20px; font-size: 0.9em; opacity: 0.9;">Marie-Christine Abatte - Psychologue</div>
    </div>
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">11</div><div class="stat-label">Modules</div></div>
            <div class="stat-card"><div class="stat-number">""" + str(total_files) + """</div><div class="stat-label">Ressources</div></div>
            <div class="stat-card"><div class="stat-number">""" + str(total_interactive) + """</div><div class="stat-label">Pages Interactives</div></div>
            <div class="stat-card"><div class="stat-number">""" + str(total_documents) + """</div><div class="stat-label">Documents</div></div>
            <div class="stat-card"><div class="stat-number">""" + str(total_media) + """</div><div class="stat-label">Médias</div></div>
        </div>
        <h2 class="section-title">Modules de Formation</h2>
        <div class="modules-grid">
"""
    
    for i in range(11):
        module_name = f"Module {i}"
        module_data = all_modules_data.get(module_name, {'files': []})
        file_count = len(module_data['files'])
        html += f"""            <a href="{module_name}/index.html" class="module-card">
                <div class="module-header"><div class="module-icon">📚</div><div class="module-title">{module_name}</div></div>
                <div class="module-count">{file_count} ressource{'s' if file_count != 1 else ''}</div>
            </a>
"""
    
    html += """        </div>
        <div class="tools-section">
            <h2 class="section-title" style="border-color: #8FAFB1; color: #8FAFB1;">Outils et Questionnaires Généraux</h2>
            <div class="tools-grid">
"""
    
    for file in root_files:
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
        <p style="margin-top: 15px;">Généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
    </footer>
</body>
</html>"""
    
    return html

def main():
    """Fonction principale"""
    print("🚀 Génération des index de modules - Version 2.0")
    print("=" * 60)
    
    # Scanner les fichiers à la racine
    print("\n📁 Scan des fichiers à la racine...")
    root_files = scan_root_files(REPO_ROOT)
    print(f"   ✓ {len(root_files)} fichier(s) trouvé(s) à la racine")
    
    all_modules_data = {}
    
    # Scanner et générer l'index pour chaque module
    for module_name in MODULES:
        module_path = os.path.join(REPO_ROOT, module_name)
        
        print(f"\n📁 Traitement : {module_name}")
        
        # Scanner les fichiers du module
        files = scan_directory_recursive(module_path, REPO_ROOT)
        all_modules_data[module_name] = {'files': files}
        
        print(f"   ✓ {len(files)} fichier(s) dans le module")
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(module_path, exist_ok=True)
        
        # Générer l'index du module
        index_html = generate_module_index(module_name, files, root_files)
        index_path = os.path.join(module_path, "index.html")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"   ✓ Index créé : {index_path}")
    
    # Générer la page d'accueil principale
    print(f"\n🏠 Génération de la page d'accueil principale...")
    main_index_html = generate_main_index(all_modules_data, root_files)
    main_index_path = os.path.join(REPO_ROOT, "index.html")
    
    with open(main_index_path, 'w', encoding='utf-8') as f:
        f.write(main_index_html)
    
    print(f"   ✓ Page d'accueil créée : {main_index_path}")
    
    print("\n" + "=" * 60)
    print("✅ Génération terminée avec succès !")
    print(f"📊 Total : {len(MODULES)} modules traités")
    print(f"📄 Total : {sum(len(data['files']) for data in all_modules_data.values()) + len(root_files)} fichiers indexés")
    print(f"   - {len(root_files)} fichiers à la racine")
    print(f"   - {sum(len(data['files']) for data in all_modules_data.values())} fichiers dans les modules")
    print("\n💡 Les fichiers de la racine sont accessibles depuis tous les modules!")

if __name__ == "__main__":
    main()
