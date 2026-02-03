"""
YouTube Downloader - Web App
Descarga videos de YouTube en la calidad que elijas
"""

from flask import Flask, render_template, request, jsonify
import subprocess
import os
import sys
import threading
from datetime import datetime
import re

app = Flask(__name__)

# Configuración
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Videos")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Estado global de descargas
downloads_status = {}

@app.route('/')
def index():
    """Página principal del descargador"""
    from flask import make_response
    import time
    response = make_response(render_template('downloader.html', v=int(time.time())))
    # Headers para prevenir caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/get-video-info', methods=['POST'])
def get_video_info():
    """Obtener información del video (thumbnail, título, calidades)"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'URL vacía'}), 400
    
    try:
        # Extraer ID del video
        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({'success': False, 'error': 'URL inválida'}), 400
        
        # Thumbnail de YouTube
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Obtener formatos disponibles con bypass
        comando = [
            sys.executable,
            '-m', 'yt_dlp',
            '--dump-json',
            '--no-warnings',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--extractor-args', 'youtube:player_client=android,web',  # ← NUEVO: Bypass
            url
        ]
        
        if os.path.exists('youtube_cookies.txt'):
            comando.extend(['--cookies', 'youtube_cookies.txt'])
        
        result = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': 'No se pudo obtener información del video'
            }), 400
        
        # Parsear JSON
        import json
        video_info = json.loads(result.stdout)
        
        title = video_info.get('title', 'Sin título')
        duration = video_info.get('duration', 0)
        
        # Obtener formatos
        formats = []
        format_dict = {}
        
        for fmt in video_info.get('formats', []):
            if fmt.get('vcodec') != 'none' and fmt.get('ext') == 'mp4':
                height = fmt.get('height', 0)
                if height >= 720:
                    format_dict[height] = True
        
        # Construir lista de calidades
        if 2160 in format_dict:
            formats.append({'id': 'best4k', 'label': '4K (2160p)', 'resolution': 2160})
        if 1440 in format_dict:
            formats.append({'id': 'best1440', 'label': '1440p (2K)', 'resolution': 1440})
        if 1080 in format_dict:
            formats.append({'id': 'best1080', 'label': '1080p (Full HD)', 'resolution': 1080})
        if 720 in format_dict:
            formats.append({'id': 'best720', 'label': '720p (HD)', 'resolution': 720})
        
        if not formats:
            formats = [
                {'id': 'best', 'label': 'Mejor calidad disponible', 'resolution': 9999}
            ]
        
        return jsonify({
            'success': True,
            'title': title,
            'thumbnail': thumbnail_url,
            'duration': duration,
            'formats': formats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download', methods=['POST'])
def download_video():
    """Iniciar descarga de video"""
    data = request.get_json()
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL vacía'}), 400
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return jsonify({'success': False, 'error': 'No es una URL de YouTube'}), 400
    
    # Generar ID de descarga
    download_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Iniciar descarga en thread separado
    thread = threading.Thread(
        target=download_worker,
        args=(url, quality, download_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Descarga iniciada',
        'download_id': download_id,
        'folder': DOWNLOAD_FOLDER
    })

def download_worker(url, quality, download_id):
    """Worker que ejecuta la descarga"""
    downloads_status[download_id] = {
        'status': 'downloading',
        'progress': 0,
        'message': 'Iniciando descarga...'
    }
    
    try:
        # Mapear calidad a formato de yt-dlp
        format_map = {
            'best4k': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]',
            'best1440': 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]',
            'best1080': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]',
            'best720': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]',
            'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        }
        
        format_string = format_map.get(quality, format_map['best'])
        
        # Comando de descarga
        comando = [
            sys.executable,
            '-m', 'yt_dlp',
            '--no-check-certificates',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-f', format_string,
            '--merge-output-format', 'mp4',
            '-o', os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            '--newline',
        ]
        
        if os.path.exists('youtube_cookies.txt'):
            comando.extend(['--cookies', 'youtube_cookies.txt'])
        
        comando.append(url)
        
        # Ejecutar descarga
        process = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Leer output
        for line in process.stdout:
            line = line.strip()
            if line:
                if '[download]' in line and '%' in line:
                    try:
                        percent = line.split('%')[0].split()[-1]
                        downloads_status[download_id]['progress'] = float(percent)
                    except:
                        pass
                
                downloads_status[download_id]['message'] = line
        
        process.wait()
        
        if process.returncode == 0:
            downloads_status[download_id] = {
                'status': 'completed',
                'progress': 100,
                'message': '✅ Descarga completada',
                'folder': DOWNLOAD_FOLDER
            }
        else:
            downloads_status[download_id] = {
                'status': 'error',
                'progress': 0,
                'message': '❌ Error en la descarga'
            }
    
    except Exception as e:
        downloads_status[download_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'❌ Error: {str(e)}'
        }

@app.route('/status/<download_id>')
def get_status(download_id):
    """Obtener estado de una descarga"""
    status = downloads_status.get(download_id, {
        'status': 'unknown',
        'progress': 0,
        'message': 'Descarga no encontrada'
    })
    return jsonify(status)

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
    port = int(os.environ.get('DOWNLOADER_PORT', 5000))
    
    print("=" * 60)
    print("  YouTube Downloader")
    print("=" * 60)
    print()
    print(f"📁 Carpeta de descargas: {DOWNLOAD_FOLDER}")
    print()
    print(f"🌐 Puerto: {port}")
    print()
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # No abrir navegador en producción
    if not os.environ.get('RENDER'):
        import webbrowser
        threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    app.run(debug=False, host='0.0.0.0', port=port)

