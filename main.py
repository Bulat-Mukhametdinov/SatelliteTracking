from flask import Flask, render_template, request, redirect, url_for, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import base64
from Organization import get_dataframe
from visualization.visualization import get_satellite_orb_img
from visualization.utils import getSatellitesObjects
import cv2

app = Flask(__name__, static_url_path="", static_folder="public")

df = get_dataframe()
satellites = getSatellitesObjects()

@app.route('/')
def index():
    return df.to_html()

@app.route('/satellite/<int:id>', methods=["GET"])
def satellite(id):
    try:
        cv2.imwrite("public/satellite/img.png", get_satellite_orb_img(satellites[id]))
        return render_template_string('<img src="img.png">')
    except:
        return render_template_string(f"{satellites[id].satellite_name} was died")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
    app.run(debug=True)