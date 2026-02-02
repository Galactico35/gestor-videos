"""
YouTube Video Manager - Gestor de Contenidos
Base de datos y búsqueda de videos de YouTube
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime
import re

app = Flask(__name__)

# Configuración
DATABASE = 'videos_database.db'

def get_db():
    """Obtener conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializar base de datos"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            etiquetas TEXT,
            resolucion TEXT,
            fps INTEGER,
            camara TEXT,
            perfil_color TEXT,
            sede TEXT,
            audiovisual TEXT,
            orientacion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal - Buscador"""
    from flask import make_response
    response = make_response(render_template('manager.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Obtener todos los videos o buscar"""
    query = request.args.get('q', '').strip()
    resolucion = request.args.get('resolucion', '').strip()
    fps = request.args.get('fps', '').strip()
    sede = request.args.get('sede', '').strip()
    orientacion = request.args.get('orientacion', '').strip()
    
    conn = get_db()
    
    # Construir query SQL
    sql = 'SELECT * FROM videos WHERE 1=1'
    params = []
    
    if query:
        sql += ' AND (titulo LIKE ? OR descripcion LIKE ? OR etiquetas LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
    
    if resolucion:
        sql += ' AND resolucion = ?'
        params.append(resolucion)
    
    if fps:
        sql += ' AND fps = ?'
        params.append(int(fps))
    
    if sede:
        sql += ' AND sede LIKE ?'
        params.append(f'%{sede}%')
    
    if orientacion:
        sql += ' AND orientacion = ?'
        params.append(orientacion)
    
    sql += ' ORDER BY fecha_creacion DESC'
    
    cursor = conn.execute(sql, params)
    videos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Extraer ID de YouTube para thumbnail
    for video in videos:
        video['video_id'] = extract_video_id(video['url'])
        video['thumbnail'] = f"https://img.youtube.com/vi/{video['video_id']}/mqdefault.jpg" if video['video_id'] else None
    
    return jsonify({'success': True, 'videos': videos, 'count': len(videos)})

@app.route('/api/videos', methods=['POST'])
def add_video():
    """Agregar nuevo video"""
    data = request.get_json()
    
    required_fields = ['url', 'titulo']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400
    
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO videos (
                url, titulo, descripcion, etiquetas, resolucion, fps,
                camara, perfil_color, sede, audiovisual, orientacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['url'],
            data['titulo'],
            data.get('descripcion', ''),
            data.get('etiquetas', ''),
            data.get('resolucion', ''),
            data.get('fps', 0),
            data.get('camara', ''),
            data.get('perfil_color', ''),
            data.get('sede', ''),
            data.get('audiovisual', ''),
            data.get('orientacion', '')
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Video agregado exitosamente'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Este video ya existe'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/videos/<int:video_id>')
def get_video(video_id):
    """Obtener un video específico con videos relacionados"""
    conn = get_db()
    cursor = conn.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
    video = cursor.fetchone()
    
    if not video:
        conn.close()
        return jsonify({'success': False, 'error': 'Video no encontrado'}), 404
    
    video_dict = dict(video)
    video_dict['video_id'] = extract_video_id(video_dict['url'])
    video_dict['thumbnail'] = f"https://img.youtube.com/vi/{video_dict['video_id']}/maxresdefault.jpg" if video_dict['video_id'] else None
    
    # Encontrar videos relacionados
    related_videos = []
    if video_dict.get('etiquetas') or video_dict.get('titulo'):
        # Buscar por etiquetas y palabras del título
        search_terms = []
        if video_dict.get('etiquetas'):
            search_terms.extend(video_dict['etiquetas'].split(','))
        if video_dict.get('titulo'):
            search_terms.extend(video_dict['titulo'].split())
        
        # Construir query para videos relacionados
        sql = 'SELECT * FROM videos WHERE id != ? AND ('
        conditions = []
        params = [video_id]
        
        for term in search_terms:
            term = term.strip()
            if term:
                conditions.append('titulo LIKE ? OR etiquetas LIKE ? OR descripcion LIKE ?')
                params.extend([f'%{term}%', f'%{term}%', f'%{term}%'])
        
        if conditions:
            sql += ' OR '.join(conditions) + ') LIMIT 6'
            cursor = conn.execute(sql, params)
            related_videos = [dict(row) for row in cursor.fetchall()]
            
            for rel_video in related_videos:
                rel_video['video_id'] = extract_video_id(rel_video['url'])
                rel_video['thumbnail'] = f"https://img.youtube.com/vi/{rel_video['video_id']}/mqdefault.jpg" if rel_video['video_id'] else None
    
    conn.close()
    
    return jsonify({
        'success': True,
        'video': video_dict,
        'related': related_videos
    })

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    """Actualizar video"""
    data = request.get_json()
    
    conn = get_db()
    try:
        conn.execute('''
            UPDATE videos SET
                titulo = ?, descripcion = ?, etiquetas = ?, resolucion = ?,
                fps = ?, camara = ?, perfil_color = ?, sede = ?,
                audiovisual = ?, orientacion = ?
            WHERE id = ?
        ''', (
            data['titulo'],
            data.get('descripcion', ''),
            data.get('etiquetas', ''),
            data.get('resolucion', ''),
            data.get('fps', 0),
            data.get('camara', ''),
            data.get('perfil_color', ''),
            data.get('sede', ''),
            data.get('audiovisual', ''),
            data.get('orientacion', ''),
            video_id
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Video actualizado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Eliminar video"""
    conn = get_db()
    try:
        conn.execute('DELETE FROM videos WHERE id = ?', (video_id,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Video eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/stats')
def get_stats():
    """Obtener estadísticas"""
    conn = get_db()
    
    total = conn.execute('SELECT COUNT(*) as count FROM videos').fetchone()['count']
    
    por_resolucion = {}
    cursor = conn.execute('SELECT resolucion, COUNT(*) as count FROM videos GROUP BY resolucion')
    for row in cursor:
        if row['resolucion']:
            por_resolucion[row['resolucion']] = row['count']
    
    por_sede = {}
    cursor = conn.execute('SELECT sede, COUNT(*) as count FROM videos GROUP BY sede')
    for row in cursor:
        if row['sede']:
            por_sede[row['sede']] = row['count']
    
    conn.close()
    
    return jsonify({
        'total': total,
        'por_resolucion': por_resolucion,
        'por_sede': por_sede
    })

def extract_video_id(url):
    """Extraer ID del video de YouTube"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

if __name__ == '__main__':
    # Puerto configurable via variable de entorno (para Render.com)
    port = int(os.environ.get('PORT', 5001))
    
    print("=" * 60)
    print("  YouTube Video Manager - Gestor de Contenidos")
    print("=" * 60)
    print()
    print("Inicializando base de datos...")
    init_db()
    print("✓ Base de datos lista")
    print()
    print(f"🌐 Puerto: {port}")
    print()
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # No abrir navegador en producción
    if os.environ.get('RENDER'):
        # Producción en Render
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        # Desarrollo local
        import webbrowser
        import threading
        threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
        app.run(debug=False, host='0.0.0.0', port=port)
