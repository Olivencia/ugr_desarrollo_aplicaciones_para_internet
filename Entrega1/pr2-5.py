from flask import Flask, request, render_template, send_file
from random import randint
import mandelbrot as mandel
import os.path

app = Flask(__name__)

@app.route("/")


def svg():
	form = randint(0,3);
	if form == 0:
		svg = circle();
	elif form == 1:
		svg = rect()	
	elif form == 2:
		svg = round_rec()
	elif form == 3:
		svg = polygon()
	print form
	context = { 'svg':svg }
	return render_template( 'svg.html', **context )

def circle():
	r = randint(0,200)
	stroke = randint(0,150)
	cx = randint(0,100)+r+stroke
	cy = randint(0,100)+r+stroke
	c1 = randint(0,255)
	c2 = randint(0,255)
	c3 = randint(0,255)
	svg = '<svg width="1000" height="1000">{0}</svg>'
	circ = '<circle cx="{0}" cy="{1}" r="{2}" fill="rgb({5},{4},{3})" stroke="rgb({3},{4},{5})" stroke-width="{6}" />'
	circ = circ.format( cx, cy, r, c1, c2, c3, stroke )
	svg = svg.format( circ )
	return svg

def rect():
	w = randint(100,800)
	h = randint(100,800)
	c1 = randint(0,255)
	c2 = randint(0,255)
	c3 = randint(0,255)
	stroke = randint(0,50)
	svg = '<svg width="1000" height="1000">{0}</svg>'
	rect = '<rect width="{0}" height="{1}" style="fill:rgb({2},{3},{4}); stroke-width:{5};stroke:rgb({4},{2},{3})"/>'
	rect = rect.format( w, h, c1, c2, c3, stroke)
	svg = svg.format( rect )
	return svg

def round_rec():
	w = randint(100,800)
	h = randint(100,800)
	x = randint(10,80)
	y = randint(10,80)	
	rx = randint(10,80)
	ry = randint(10,80)
	c1 = randint(0,255)
	c2 = randint(0,255)
	c3 = randint(0,255)
	stroke = randint(0,50)
	opacity = randint(3,9)
	svg = '<svg width="1000" height="1000">{0}</svg>'
	round_rect = '<rect width="{0}" height="{1}" x="{6}" y="{7}" rx="{8}" ry="{9}" style="fill:rgb({2},{3},{4});stroke-width:{5};stroke:rgb({4},{2},{3});opacity:0.{10}/>"'
	round_rect = round_rect.format( w, h, c1, c2, c3, stroke, x, y, rx, ry, opacity)
	svg = svg.format( round_rect )
	return svg

def polygon():
	p1 = randint(100,200)
	p2 = randint(5,50)
	p3 = randint(5,50)
	p4 = randint(150,200)
	p5 = randint(150,200)
	p6 = randint(50,100)
	p7 = randint(5,50)
	p8 = randint(50,100)
	p9 = randint(150,200)
	p10 = randint(150,200)	
	c1 = randint(0,255)
	c2 = randint(0,255)
	c3 = randint(0,255)
	stroke = randint(0,50)
	stroke = randint(0,10)
	svg = '<svg width="1000" height="1000">{0}</svg>'
	polygon = '<polygon points="{1},{2} {3},{4} {5},{6} {7},{8} {9},{10}" style="fill:rgb({11},{12},{13});stroke-width:{0};stroke:rgb({13},{11},{12});fill-rule:evenodd;"/>'
	polygon = polygon.format(stroke,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,c1,c2,c3)
	svg = svg.format( polygon )
	return svg

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
