import http.server
import socketserver

PORT = 9000
Handler = http.server.SimpleHTTPRequestHandler

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	extensions_map = {
		'': 'application/octet-stream',
		'.manifest': 'text/cache-manifest',
		'.html': 'text/html',
		'.png': 'image/png',
		'.jpg': 'image/jpg',
		'.svg':	'image/svg+xml',
		'.css':	'text/css',
		'.js':'application/x-javascript',
		'.wasm': 'application/wasm',
		'.json': 'application/json',
		'.xml': 'application/xml',
	}

	def do_GET(self):

		print("GET:{}".format(self.path))
		if self.path == '/':
			self.path = 'hotword_demo.html'

		if self.path == '/nyumaya_premium.wasm':
			self.path = './lib/nyumaya_premium.wasm'
			self.mimetype = 'application/wasm'

		if self.path == '/nyumaya_premium.js':
			self.path = './lib/nyumaya_premium.js'

		return http.server.SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()
