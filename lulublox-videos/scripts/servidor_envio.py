"""Serves the batch MP4s to the YouTube Studio open in the user's Chrome, with no size limit.

  python servidor_envio.py LOTE [--porta 8768]

The browser upload tool only takes files up to 10 MB and the Shorts are 15-45 MB. This server listens only on
127.0.0.1 and only answers the https://studio.youtube.com origin (CORS + Private Network Access), with the final
MP4s listed in the batch agenda.json: GET /video/NN returns video NN, GET /meta/NN its title, description, tags,
date and time. In the Studio upload dialog, the JavaScript in references/youtube-studio.md fetches the file from
here and puts it in the file input (DataTransfer). Nothing leaves the computer through this server: the Studio
itself uploads to YouTube, in the user's account.
"""
import argparse, http.server, json, socketserver
from pathlib import Path

ORIGEM = 'https://studio.youtube.com'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lote')
    ap.add_argument('--porta', type=int, default=8768)
    a = ap.parse_args()
    lote = Path(a.lote).resolve()
    agenda = json.loads((lote / 'agenda.json').read_text(encoding='utf-8'))
    videos = {it['n']: Path(it['video']) for it in agenda['itens']}
    # Metadados de cada vídeo para preencher o formulário do Studio direto da agenda (sem digitar à mão).
    metas = {it['n']: {k: it[k] for k in ('titulo', 'descricao', 'tags', 'data_studio', 'hora_studio')} | {'arquivo': Path(it['video']).name}
             for it in agenda['itens']}

    class Handler(http.server.BaseHTTPRequestHandler):
        def _cors(self):
            if self.headers.get('Origin') == ORIGEM:
                self.send_header('Access-Control-Allow-Origin', ORIGEM)
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.send_header('Vary', 'Origin')

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors()
            self.end_headers()

        def do_GET(self):
            partes = self.path.strip('/').split('/')
            if partes == ['ping']:
                corpo = b'ok'
                tipo = 'text/plain'
            elif len(partes) == 2 and partes[0] == 'meta' and partes[1] in metas:
                corpo = json.dumps(metas[partes[1]], ensure_ascii=False).encode('utf-8')
                tipo = 'application/json; charset=utf-8'
            elif len(partes) == 2 and partes[0] == 'video' and partes[1] in videos and videos[partes[1]].exists():
                corpo = videos[partes[1]].read_bytes()
                tipo = 'video/mp4'
            else:
                self.send_response(404)
                self._cors()
                self.end_headers()
                return
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', tipo)
            self.send_header('Content-Length', str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)

        def log_message(self, fmt, *args):
            print('[envio]', fmt % args, flush=True)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', a.porta), Handler) as srv:
        print(f'servindo {len(videos)} vídeos de {lote.name} em http://127.0.0.1:{a.porta}/video/NN (só para {ORIGEM})', flush=True)
        srv.serve_forever()


if __name__ == '__main__':
    main()
