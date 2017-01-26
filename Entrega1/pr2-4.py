from flask import Flask, request, render_template
import mandelbrot as mandel
import os.path

app = Flask(__name__)

@app.route("/")
def getData():
	return render_template('table.html')

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

@app.route("/fractal", methods=['POST', 'GET'])
def fractal():
	data = request.form

	paleta = data.getlist('color')
	nColoresPaleta = len(paleta)
	colores = ''
	for i in range(0, len(paleta)):
		color_num = paleta[i].replace('#','')
		colores += 'c' + str(i) + ':' + color_num; 
		paleta[i] = hex_to_rgb(paleta[i])

	img_name = 'images/fractal_x1' + data['x1'] + 'x2' + data['x2'] + 'y1' + data['y1'] + 'y2' + data['y2'] + 'ancho' + data['ancho'] + 'iteraciones' + data['iteraciones'] + colores + '.png'

	if os.path.isfile("static/" + img_name)  == 0:

		x1 = float(data['x1'])
		y1 = float(data['y1'])
		x2 = float(data['x2'])
		y2 = float(data['y2'])
		ancho = int(data['ancho'])
		iteraciones = int(data['iteraciones'])

		mandel.renderizaMandelbrotBonito(x1, y1, x2, y2, ancho, iteraciones, "static/" + img_name, paleta, nColoresPaleta)

	return render_template("fractal.html", img_name = img_name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
