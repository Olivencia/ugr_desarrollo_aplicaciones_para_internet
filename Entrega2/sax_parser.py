from lxml import etree
import urllib
import sys
import os

items = 0
n_images = 0
images = []
cnt = 0
content_search = []

def generateRSSData(search_data):
	global cnt, content_search
	items = 0
	n_images = 0
	cnt = 0
	images = []
	content_search = []
	class ParseRssNews():
		def __init__ (self):
			print ('Comenzando la lectura del RSS...')
		
		def start (self, tag, attrib): 	
			global items, n_images, images
			if tag == "item": items += 1
			for k in attrib:
				if k == "type" and attrib[k] == "image/jpeg":
					n_images += 1
					images.append(attrib['url'])

		def data (self, data): 			
			if search_data:
				global content_search, cnt
				if data.lower().find(search_data.lower()) >= 0 and data.find('<p>') >=0:
					cnt += 1
					style = "style='display: table; margin: 0 auto; text-align: justify; width: 80%'"
					content_search.append("<h3 " + style +  ">Result " + str(cnt) + " for: " + search_data.capitalize() + "</h3>")
					content_search.append("<div " + style +  ">"+ data + "</div>")
		
		def close (self):
			print ('Se ha terminado de escribir en el archivo los datos del RSS. Para mas informacion consulte el archivo sax_parser_data.txt.' )

	parser = etree.XMLParser(target=ParseRssNews ())
	etree.parse('portada.xml', parser)

	# Download images
	cnt = 0
	path = "static/images/"
	for img in images:
		img_name = img.split('/')[-1]
		if os.path.isfile(path + img_name) == 0:
			urllib.URLopener().retrieve(img, path + img_name)
		cnt += 1

	rss_data = open('sax_parser_data.txt', 'w')
	rss_data.write("There are " + str(items) + " items and " + str(n_images) + " images.")
	rss_data.write(os.linesep)
	rss_data.write(str(len(content_search)) + " elements founded")
	rss_data.write(os.linesep)
	rss_data.write("All images downloaded and stored in " + path)
	rss_data.write(os.linesep)
	rss_data.close()

	return content_search
