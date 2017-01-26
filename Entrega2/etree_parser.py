from lxml import etree
import os
import urllib
import sys

tree = etree.parse('portada.xml')

items = 0
n_images = 0
images = []
content_search = 0
path = "static/images/"

# Root element
rss = tree.getroot()

# Los elementos funcionan como listas
# First child
channel = rss[0]

#open file to search something

f = open('static/html/rss_content.html', 'w')

for e in channel:
	if e.tag == 'item':
		items += 1
		for element in e:
			if element.get('type') == 'image/jpeg':
				n_images += 1
				url = element.get('url')
				images.append(url)
				img_name = url.split('/')[-1]
				if os.path.isfile(path + img_name) == 0:
					urllib.URLopener().retrieve(url, path + img_name)

			if element.text:
				data = element.text.encode('utf-8')
				if len(sys.argv) > 1 and element.text and sys.argv[1].lower() in data.lower(): 
					content_search += 1
					content = ("<div class='rss_content'>"+element.text+"</div>").encode('utf-8', errors='replace')
					f.write(content)

f.close()

#show data

print "There are " + str(items) + " items and " + str(n_images) + " images."
if len(sys.argv) > 1:
	print str(content_search) + " elements founded"
print "All images download at " + path
		

