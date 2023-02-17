from flask import Flask, request
from flask import render_template, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def start_page():
    return render_template("index.html")


@app.route('/error')
def error_page():
    return render_template("error.html")


@app.route('/download/')
def download_page():
    return render_template("download.html")


@app.route("/download/image")
def download_image():
    if os.path.exists("./uploads/image.png") and (os.path.exists("./uploads/watermark.png")):
        image = Image.open("./uploads/image.png")
        watermark = Image.open("./uploads/watermark.png")
        imageSize = image.size
        watermarkSize = watermark.size
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        pos = (round(imageSize[0] * (x / 100) - watermarkSize[0] / 2),
               round(imageSize[1] * (y / 100) - watermarkSize[1] / 2))
        image.paste(watermark, pos)
        image.save(os.path.join("./downloads", "download.png"))
        return send_file(os.getcwd() + "/downloads/download.png", as_attachment=True)


@app.route('/upload/images',  methods=['POST'])
def upload_images():
    image = request.files['file']
    watermark = request.files['watermark']
    if image and watermark:
        image_name = "image." + secure_filename(image.filename.split(".")[1])
        watermark_name = "watermark." + secure_filename(watermark.filename.split(".")[1])
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        watermark.save(os.path.join(app.config['UPLOAD_FOLDER'], watermark_name))
        return download_page()
    return error_page()


if __name__ == '__main__':
    app.run()
