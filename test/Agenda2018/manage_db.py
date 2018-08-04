
import sqlite3
import numpy as np
import pandas as pd

# create ini table
path = '/Users/jonate/sqlite_db/eca/agenda/'
db_name = 'agenda.db'
conn = sqlite3.connect(path + db_name)
cur = conn.cursor()

# load data-files: itinerarios
itins = pd.read_csv('data/itins.csv')
itins.to_sql('itins', conn, if_exists="replace")
# LOCAL - ITINS - TAR
local = pd.read_csv('data/local_itins_tar.csv')
local.to_sql('local_itin_tar', conn, if_exists="replace")
x = local.values[:, [0, 1, 2, 3, 4, 5, 6, 7, 9]]
_, ind = np.unique(x[:, 5:8].astype('int'), axis=0, return_index=True)
x = x[ind, :]
itins['DEPARTAMENTO'] = ""
itins['MUNICIPIO'] = ""
itins['CORREGIMIENTO'] = ""
itins['BARRIO'] = ""
itins['CODLOCAL'] = np.nan
xyz = itins.values[:, 1:4].astype('int')
lmn = x[:, 5:8].astype('int')
for i in range(0, len(x)):
    posi = []

# GEO - NIF
# geo = pd.read_csv('data/geo_nif.csv')
# geo.to_sql('geo_nif', conn, if_exists="replace")


# function [cx, cy, dg] = geo_metrics(x,y)
# x = x(x ~= 0);
# y = y(y ~= 0);
# dist = sqrt((x - median(x)).^2 + (y - median(y)).^2);
# pk = (dist <= quantile(dist,0.75) + 1.5*iqr(dist));
# if sum(pk) >= 1
#     cx = median(x(pk));
#     cy = median(y(pk));
# else
#     cx = 0;
#     cy = 0;
# end
# dg = deg2km(mean(dist));

# Capital de cada Delegación
del_city = [['Atlántico Norte', 'BARRANQUILLA'],
            ['Atlántico Sur', 'SABANALARGA'],
            ['Bolívar Norte', 'CARTAGENA'],
            ['Bolívar Sur', 'MAGANGUE'],
            ['Cesar', 'VALLEDUPAR'],
            ['Córdoba Norte', 'MONTERIA'],
            ['Córdoba Sur', 'PLANETA RICA'],
            ['Guajira', 'RIOHACHA'],
            ['Magdalena', 'SANTA MARTA'],
            ['Sucre', 'SINCELEJO']]
