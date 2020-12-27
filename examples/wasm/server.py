import http.server
import socketserver

PORT = 9000
Handler = http.server.SimpleHTTPRequestHandler

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):

		print("GET:{}".format(self.path))
		if self.path == '/':
			self.path = 'hotword_demo.html'

		if self.path == '/nyumaya_premium.wasm':
			self.path = './lib/nyumaya_premium.wasm'

		if self.path == '/nyumaya_premium.js':
			self.path = './lib/nyumaya_premium.js'

		return http.server.SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()
