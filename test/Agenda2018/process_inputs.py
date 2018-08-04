
import os
import pandas as pd


# itins por Zona --------------------------------------------------------------
sw = False  # para no volver a cargar files/itins
path_file = 'data/itins.csv'
if sw:
    efile = pd.ExcelFile('files/itins.xlsx')
    sheets = efile.sheet_names
    ni = len(efile.sheet_names)
    data = efile.parse(0)
    data = data.drop(data.columns[[2, 6]], axis=1)
    for i in range(1, ni):
        datai = efile.parse(i)
        datai = datai.drop(datai.columns[[2, 6]], axis=1)
        data = pd.concat([data, datai], ignore_index=True)
    # borrar si existe previamente
    os.remove(path_file)
    # save
    data.to_csv(path_file, index=False)
else:
    data = pd.read_csv(path_file)
# agrupar por itins
# datag = data.groupby(['Centro_Lectura', 'Ruta', 'Itinerario']).sum()
# print('Itinerarios en itins: {}'.format(len(datag)))
# data file -------------------------------------------------------------------
x = pd.read_excel('files/data.xlsx')
xg = x.groupby(['COD_UNICOM', 'RUTA', 'NUM_ITIN']).sum()
print('Itinerarios en data: {}'.format(len(xg)))
# ini_itin --------------------------------------------------------------------
data = pd.read_csv('files/ini_itins.csv')
