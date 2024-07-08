
from flask import Flask, render_template, request
import requests
import json
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)


def fetch_api_data(url):
    try:
        response = requests.get(url)
        print(f'{url} Geted.')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    data = fetch_api_data("http://127.0.0.1:8000/api/data")
    summary = fetch_api_data("http://127.0.0.1:8000/api/summary")
    future = fetch_api_data("http://127.0.0.1:8000/api/future_research")
    limit = fetch_api_data('http://127.0.0.1:8000/api/limitations')
    insights = fetch_api_data('http://127.0.0.1:8000/api/insights')
    patterns = fetch_api_data('http://127.0.0.1:8000/api/patterns')
    correlation_matrix = fetch_api_data('http://127.0.0.1:8000/api/correlation')
    preprocess = requests.post('http://localhost:8000/api/preprocess').json()
    visualization_image, visualization_error, statistical, statistical_error = None, None, None, None

    if request.method == 'POST':
        if request.values.get('statistical-test-type'):
            test_type = request.values.get('statistical-test-type')
            var = request.values.get('statistical-var')


            url = "http://127.0.0.1:8000/api/stat_tests"
            try:
                data = {
                    "test_type": test_type,
                    "variables": var.split(',')
                }
                statistical = requests.post(url, json=data).json()
                print(statistical)
            except KeyError:
                statistical_error = 'Not Found.'

            except:
                if not ',' in var:
                    statistical_error = 'variables are not enough.'
 

        if request.values.get('test-type'):
            test_type = request.values.get('test-type')
            var1 = request.values.get('var1')
            var2 = request.values.get('var2')

            try:
                img_data = fetch_api_data(f'http://127.0.0.1:8000/api/visualization?type={test_type}&var1={var1}&var2={var2}')['image']
                bytes_decoded = base64.b64decode(img_data)
                img = Image.open(BytesIO(bytes_decoded))
                out_jpg = img.convert("RGB")
                out_jpg.save("static/images/visualization.jpg")
                visualization_image = 'images/visualization.jpg'
            except:
                visualization_error = 'Not Found.'

    print(statistical)
    return render_template('index.html', data=data, summary=summary, statistical=statistical, statistical_error=statistical_error, preprocess=preprocess, correlation_matrix=correlation_matrix, patterns=patterns, insights=insights, limit=limit, future=future, visualization_image=visualization_image, visualization_error=visualization_error)

if __name__ == '__main__':
    app.run(debug=False)