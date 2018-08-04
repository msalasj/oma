
import numpy as np
import os
import pandas as pd
import datetime
import time


def generar_calendario(df, nd):
    """
    :param df: dias festivos de cada mes
    :param nd: número de dias de lectura
    :return: calendario de dias de lectura
    """
    cal = np.zeros([12, nd])
    for i in range(0, 12):
        k = 1
        j = 0
        while j < nd:
            if not(k in df[i]):
                cal[i, j] = k
                j += 1
            k += 1
    return cal


def generar_agenda(fini, cal):
    """
    :param fini: fecha de diciembre del año anterior
    :param cal: calendario de días de lectura
    :return: agenda con los dias de lectura en cada mes
    """
    # dxi = np.array(fini.day)
    # dias_mes
    # inid = np.unique(new_day)
    ag = np.zeros([len(fini), 12])
    # for i in range(0, 12):
    #     for j in range(0, len(inid)):
    #         posj = np.where(new_day == inid[j])[0]
    #         ag[posj, i] = cal[i, j]
    for i in range(0, 12):
        ag[:, i] = cal[i, (dias_mes[:, i] - 1).astype('int')]
    return ag


def generar_fechas(fini, ag):
    """
    :param fini: fecha de diciembre del año anterior
    :param ag: agenda con los dias de lectura en cada mes
    :return: agenda con las fechas de los dias de lectura en cada mes
    """
    fechas = list()
    fechas.append(fini)
    for i in range(0, 12):
        origin = pd.Timestamp('2018-' + str(i+1) + '-01')
        x = pd.to_datetime(ag[:, i] - 1, unit='D', origin=origin)
        fechas.append(x)
    return fechas


def performance_metrics(datexm):
    """
    :param datexm:  agenda con las fechas de los dias de lectura en cada mes
    :return: promedio de dias facturados
    """
    nd = len(datexm[0])
    dfxm = np.zeros([nd, 12])
    d32 = np.zeros(12)
    it = np.zeros(12)
    for i in range(0, 12):
        dfxm[:, i] = np.array((datexm[i + 1] - datexm[i]).days)
        nanxm = np.isnan(dfxm[:, i])
        dfxm[nanxm, i] = 0
        d32[i] = np.sum(dfxm[:, i] > 32)
        it[i] = np.round(100 * np.sum(datexm[i + 1].day > vencimientos[i])/nd)
    # dias facturados
    adf = np.mean(np.sum(dfxm, 1))
    adfm = np.mean(dfxm, 0)
    return adf, adfm, d32, it


def save_agenda(itins, fechas):
    """
    :param itins: dataframe con los itinerarios
    :param fechas: agenda con las fechas de los dias de lectura en cada mes
    """
    x = (pd.DataFrame(fechas)).T
    pathfile = 'data/unicoms/Agenda.' + unicom + '.csv'
    if os.path.exists(pathfile):
        os.remove(pathfile)
    # concat data
    x.drop(0, axis=1, inplace=True)
    cnames = []
    for i in range(1, 13):
        cnames.append('2018-' + np.str(i).zfill(2))
    x.columns = cnames
    itins.F_INI = pd.to_datetime(itins.F_INI.values)
    y = pd.concat([itins, x], axis=1)
    y.to_csv(pathfile, index=False, date_format='%d/%m/%Y')


def optimizar_agenda(adfm, fini, df_oa):
    # mes a modificar
    ms = adfm.argmax()
    print('Mes a modificar: {}'.format(ms + 1))
    # proccess
    nd = len(np.unique(np.array(fini.day)))
    dfi = df_oa[ms]
    pm = np.zeros(len(dfi))
    for j in range(0, len(dfi)):
        # borrar dia festivo del mes
        df_oa[ms] = dfi[:j] + dfi[j+1:]
        # calcular agenda
        cal_oa = generar_calendario(df_oa, nd)
        dag = generar_agenda(fini, cal_oa)
        fag = generar_fechas(fini, dag)
        # guardar pdf
        pm[j], mx = performance_metrics(fag)
        print(mx)
    # seleccionar mejor opción
    bo = pm.argmin()
    print('dfi: {}'.format(dfi))
    print('pdf: {}'.format(pm))


def agregar_domingos(x, y):
    for i in range(12):
        x[i] = np.array(x[i])
        if len(y[i]) > 0:
            pi = np.in1d(x[i], y[i], invert=True)
            x[i] = x[i][pi]
    return x


def generar_dias():
    start_month = 0  # 0: enero, 1: febrero, ...
    d2m = new_day - dia_ini
    dm = np.zeros([len(new_day), 12])
    for i in range(0, len(new_day)):
        dm[i, :] = new_day[i]
        if d2m[i] != 0:
            if start_month > 0:
                dm[i, 0:start_month] = dia_ini[i]
            km = int(abs(d2m[i]))
            if d2m[i] > 0:
                vector = dia_ini[i] + np.cumsum(movimientos[km])
            else:
                vector = dia_ini[i] - np.cumsum(movimientos[km])
            dm[i, start_month:start_month+3] = vector
    return dm


def disminuir_dias(nd, dxi, n):
    for i in range(n):
        k = nd - i
        posi = np.where(dxi == k)[0]
        dxi[posi] = nd - n
    nd = nd - n
    return nd, dxi

# Main ------------------------------------------------------------------------
if __name__ == '__main__':
    # load ini itins
    unicom = '2941'
    data = pd.read_csv('data/unicoms/' + unicom + '.csv')
    f_ini = pd.to_datetime(data.F_INI.values)
    dia_ini = data.DIA.values
    new_day = data.NEW_DAY.values
    num_dias = max(dia_ini)
    # dias festivos 2018
    tic = time.time()
    dias_festivos = [[1, 7, 8, 14, 21, 28],
                     [4, 11, 18, 25],
                     [4, 11, 18, 19, 25, 29, 30],

                     [1, 8, 15, 22, 29],
                     [1, 6, 13, 14, 20, 27],
                     [3, 4, 10, 11, 17, 24],

                     [1, 2, 8, 15, 20, 22, 29],
                     [5, 7, 12, 19, 20, 26],
                     [2, 9, 16, 23, 30],

                     [7, 14, 15, 21, 28],
                     [4, 5, 11, 12, 18, 25],
                     [2, 8, 9, 16, 23, 25, 30]]
    vencimientos = [24, 21, 21, 23, 24, 22, 24, 24, 21, 24, 23, 21]
    domingos = [[], [], [],
                [], [], [],
                [], [], [],
                [], [], []]
    movimientos = {1: [1, 0, 0], 2: [1, 1, 0], 3: [1, 1, 1], 4: [2, 1, 1],
                   5: [2, 2, 1], 6: [2, 2, 2], 7: [3, 2, 2], 8: [3, 3, 2],
                   9: [3, 3, 3], 10: [4, 3, 3],
                   11: [4, 4, 3], 12: [4, 4, 4], 13: [5, 4, 4], 14: [5, 5, 4],
                   15: [5, 5, 5], 16: [6, 5, 5], 17: [6, 6, 5], 18: [6, 6, 6],
                   19: [7, 6, 6], 20: [7, 7, 6], 21: [7, 7, 7], }
    dias_festivos = agregar_domingos(dias_festivos, domingos)
    # Disminuir Dias Calendario: test de modificación de dias de lectura
    if False:
        print('Diminuyendo Dias')
        new_day = dia_ini
        nk = 1
        print(num_dias, num_dias-nk)
        num_dias, new_day = disminuir_dias(num_dias, new_day, nk)
    # calendario
    calendario = generar_calendario(dias_festivos, num_dias)
    # >>>>> agenda <<<<<<
    dias_mes = generar_dias()
    dias_agenda = generar_agenda(f_ini, calendario)
    fechas_agenda = generar_fechas(f_ini, dias_agenda)
    save_agenda(data, fechas_agenda)
    # indicador de rendimiento
    pdf, pdfm, pm3, pm4 = performance_metrics(fechas_agenda)
    print('Promedio de Dias Facturados 2018: {}'. format(pdf))
    # print(pdfm)
    dpm2018 = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    print(np.round(100*(pdfm - dpm2018))/100)
    # print(np.mean(pdfm))
    # print('Itins > 32 dias')
    # print(pm3)
    print('Itins Trasladados %')
    print(pm4)
    # optimizar agenda
    # print('... Optimizando Agenda ...')
    # optimizar_agenda(pdfm, f_ini, dias_festivos)
