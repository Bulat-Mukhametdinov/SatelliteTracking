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
        number = int(request.form['num_of_sat'])
        if number == 1:
            if request.form['sat_id'].isnumeric():
                if 0 <= int(request.form['sat_id']) < 21987:
                    return redirect(url_for('satellite', id = int(request.form['sat_id'])))
                else:
                    flash("Неверные данные. Введите число от 0 до 21987 или полное название спутника.")
            else:
                if df['Название'].isin([request.form['sat_id']]).any():
                    return redirect(url_for('satellite', id = df.index[df['Название'] == request.form['sat_id']].tolist()[0]))
                else:
                    flash("Неверные данные. Введите число от 0 до 21987 или полное название спутника.")
        elif number > 1:
            if request.form['sat_id'].count(" ") == number-1:
                a = request.form['sat_id'].split(" ")
                flag = 0
                for i in range(len(a)):
                    if a[i].isnumeric():
                        if 0 <= int(a[i]) <= 21987:
                            a[i] = int(a[i])
                        else:
                            flag = 1
                    elif df['Название'].isin([a[i]]).any():
                        a[i] = df.index[df['Название'] == a[i]].tolist()[0]
                    else:
                        flag = 1
                    if flag:
                        break
                if flag == 0:
                    for i in range(len(a)):
                        a[i] = str(a[i])
                    return redirect(url_for('multiple', ids = "+".join(a)))
                else:
                    flash("Неверные данные.")
            else:
                flash("Неверные данные.")
    return render_template("main.html", title = "Трекинг спутников - Главная страница")


@app.route("/df/")
def df_info():
    return render_template("dataframe_page.html", title = "База данных", df = df)


@app.route("/plots/")
def plots():
    return render_template("plot_info.html", title ="Графики")


@app.route('/satellite/<int:id>', methods=["GET", "POST"])
def satellite(id):
    try:
        cv2.imwrite("public/satellite/img.png", get_satellite_orb_img([satellites[id]]))
        return render_template('satellite.html', image = 'img.png', sat_name = satellites[id].satellite_name, id_next = "/satellite/"+str(min(id+1, 21986)), id_prev = "/satellite/"+str(max(id-1, 0)))
    except:
        return render_template_string(f"{satellites[id].satellite_name} died")


@app.route('/satellite/multiple/<ids>', methods=["GET", "POST"])
def multiple(ids):
    arr = ids.split("+")
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    try:
        cv2.imwrite("public/satellite/img.png", get_satellite_orb_img([satellites[x] for x in arr]))
        return render_template('multiple.html', image = 'satellite/img.png')
    except:
        return render_template_string("one of satellites died")
    

if __name__ == '__main__':
    app.run(debug=True)
