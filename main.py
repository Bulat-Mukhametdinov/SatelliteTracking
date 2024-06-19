from flask import Flask, render_template, request, render_template_string, redirect, url_for, flash, session
from Organization import get_dataframe
from visualization.visualization import get_satellite_orb_img
from visualization.utils import getSatellitesObjects
import cv2

app = Flask(__name__, static_url_path='', static_folder='public')
app.config['SECRET_KEY'] = 'wqefcb23y4br4hjgfj45'

df = get_dataframe()
satellites = getSatellitesObjects()


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method=="POST":
        try:
            if 0 <= int(request.form['sat_id']) < 21987:
                return redirect(url_for('satellite', id = int(request.form['sat_id'])))
            else:
                flash("Неверные данные. Введите число от 0 до 21987.")
        except ValueError:
            flash("Неверные данные. Введите число от 0 до 21987.")
    return render_template("main.html", title = "Трекинг спутников - Главная страница")




@app.route("/df/")
def df_info():
    return render_template("dataframe_page.html", title = "TLE data", df = df)


@app.route("/plots/")
def plots():
    return render_template("plot_info.html")


@app.route('/satellite/<int:id>', methods=["GET", "POST"])
def satellite(id):
    try:
        cv2.imwrite("public/satellite/img.png", get_satellite_orb_img([satellites[id], satellites[0]]))
        return render_template('satellite.html', image = 'img.png', sat_name = satellites[id].satellite_name, id_next = "/satellite/"+str(min(id+1, 21986)), id_prev = "/satellite/"+str(max(id-1, 0)))
    except:
        return render_template_string(f"{satellites[id].satellite_name} was died")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
    app.run(debug=True)






