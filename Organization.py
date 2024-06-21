import pandas as pd
from Test_api import get_tle_data
from matplotlib import pyplot as plt


def get_dataframe():
    get_tle_data()
    sep = ' - '

    def org(string_part):
        str = string_part.strip(' ')
        if str == '':
            return None
        return str

    with open("TLE_data.txt", "r") as file:
        f = list(filter(None, file.read().replace("TBA - TO BE ASSIGNED", "TBA").split("\n")))
        TLE_dict = []
        TBA_counter = 1

        # https://www.space-track.org/documentation#/tle

        for index, i in enumerate(f, 1):
            line_num = org(i[0])
            if line_num == '0':
                name = org(i[2:25])
                if name == 'TBA':
                    name = name + str(TBA_counter)
                    TBA_counter += 1
            if line_num == '1':
                spu_num = org(i[2:7])
                сlassification = org(i[7])
                designator = org(i[9:17])
                epoch = org(i[18:32])
                derivative_1 = org(i[33:43])
                derivative_2 = org(i[44:52])
                braking_koef = org(i[53:61])
                element_set_type = org(i[62])
                version_num = org(i[64:68])
                checksum_1 = org(i[68])
            if line_num == '2':
                if spu_num != org(i[2:7]):
                    print("error")
                orbit_degree = org(i[8:16])
                rAscofAscenNode = org(i[17:25])
                eccentricity = org(i[26:33])
                argPerigee = org(i[34:42])
                meanAnomaly = org(i[43:51])
                meanMotion = org(i[52:63])
                revolution_num = org(i[63:68])
                checksum_2 = org(i[68])

                TLE_dict.append({
                    "Название": name,
                    "Линия номер один": 1,
                    "Номер спутника": spu_num,
                    "Классификация": сlassification,
                    "Международное обозначение": designator,
                    "Эпоха": epoch,
                    "Первая производная среднего движения": derivative_1,
                    "Вторая производная среднего движения": derivative_2,
                    "Коэффицент торможения": braking_koef,
                    "Тип эфериды": element_set_type,
                    "Номер элемента": version_num,
                    "Контрольная сумма 1": int(checksum_1),
                    "Линия номер 2": 2,
                    "Наклонение в градусах": float(orbit_degree),
                    "Долгота восходящего солнца": float(rAscofAscenNode),
                    "Эксцентриситет": eccentricity,
                    "Аргумент перицентра": float(argPerigee),
                    "Средняя аномалия": float(meanAnomaly),
                    "Средняя частота обращений": float(meanMotion),
                    "Номер витка": int(revolution_num),
                    "Контрольная сумма 2": int(checksum_2),
                })

    df = pd.DataFrame.from_dict(TLE_dict)
    sortDf_revolution = df.sort_values("Номер витка")
    sortDf_meanMotion = df.sort_values("Средняя частота обращений")

    return df
df = get_dataframe()


def get_year(x):
    new_list = []
    for i in x:
        if i == None:
            new_list.append(None)
            continue
        year = int(i[:2])

        if year < 50:
            year += 2000
            new_list.append(year)
        else:
            year += 1900
            new_list.append(year)
    return new_list

histogram_1 = plt.figure(figsize = (9,5))
plt.hist(df["Номер витка"], color = "black", bins = 30)
plt.xlabel('Количество витков, с момента старта')
plt.ylabel("Количество спутников")
plt.title("Распределение количества витков")
plt.savefig('public/images/plot1.png')



df_epoch = df[["Международное обозначение", 'Номер витка']]
new_list = get_year(df_epoch["Международное обозначение"])
df_epoch.insert(2, "Год запуска", new_list)

histogram_2 = plt.figure(figsize=(9, 5))
plt.hist(df_epoch["Год запуска"], orientation='horizontal', bins=60, color="black")
plt.xlabel('Количество спутников')
plt.ylabel("Год запуска")
plt.title("Распределение количества запущеных спутников по годам")
plt.savefig('public/images/plot2.png')

df_speed = df["Средняя частота обращений"]
histogram_3 = plt.figure(figsize=(9, 5))
plt.hist(df_speed, bins=20, color="black")
plt.xlabel('Среднее количество витков')
plt.ylabel("Количество спутников")
plt.title("Распределение количества витков")
plt.savefig('public/images/plot3.png')
