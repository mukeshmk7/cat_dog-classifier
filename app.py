from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

image_shape = (364, 397)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', "POST"])
def predict():
    if request.method == 'POST':
        input_image = request.files['file']
        input_image.save(secure_filename(input_image.filename))
        test_image = image.load_img(f'{input_image.filename}', target_size = image_shape)
        test_image = (image.img_to_array(test_image))/255
        test_image = test_image.reshape(1, image_shape[0], image_shape[1], 3)
        output = model.predict(test_image)
        if output[0][0] > 0.5:
            classifier = 'Dog'
        else:
            classifier = 'Cat'
        return render_template('predict.html', output=classifier)


if __name__ == '__main__':
    model = load_model('classifier.h5')
    app.run(host='0.0.0.0', port=8080)
