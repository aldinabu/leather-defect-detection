from flask import request, render_template, send_file
from flask import jsonify
from flask import Flask
from flask_cors import cross_origin

from logging_defects import get_logger, log_prediction
from prediction import get_prediction, save_image, tile_and_predict_image
from tiling import read_image, tile_image

app = Flask(__name__)

logger = get_logger()


@app.route("/", methods=["GET"])
def start():
    return render_template('index.html')


@app.route('/groupprediction')
def groupprediction():
    return render_template('group_prediction.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    print("[+] request received")
    image_path = save_image(request.files['image'])
    defect = get_prediction(image_path)
    response = defect['name']
    print("[+] results {}".format(response))

    log_prediction(image_path, response)
    return jsonify(response)


@app.route("/tile", methods=["POST"])
@cross_origin()
def tile():
    print("[+] request received")
    image = request.files['image']
    image_path = save_image(image)
    img = read_image(image_path)
    path, rows, cols = tile_image(img, image_path, image.filename)
    return jsonify(path)


@app.route("/tile-and-predict", methods=["POST"])
@cross_origin()
def tile_and_predict():
    print("[+] request received")
    image = request.files['image']
    image_path = save_image(image)
    img = read_image(image_path)
    path = tile_and_predict_image(img, image_path, image.filename)
    return send_file(path, "image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)
