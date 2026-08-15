import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def obtener_resultados(busqueda):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch5',
    }
    results = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch5:{busqueda}", download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    results.append({
                        'title': entry.get('title', 'Canción'),
                        'artist': entry.get('uploader', 'Artista'),
                        'url': entry.get('url', ''),
                        'artworkUrl': entry.get('thumbnail', None),
                        'album': 'Sencillo'
                    })
        except Exception as e:
            print(f"Error en yt_dlp: {e}")
    return results

@app.route('/api/search', methods=['GET'])
def search_and_extract():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    return jsonify(obtener_resultados(query))

@app.route('/api/popular', methods=['GET'])
def popular():
    # Búsqueda por defecto para que no devuelva lista vacía
    return jsonify(obtener_resultados("musica popular 2026"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
