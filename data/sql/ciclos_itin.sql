select
COD_UNICOM,
RUTA,
NUM_ITIN,
CICLO,
F_LTEOR,
F_LREAL,
F_FACT
from ciclos_itin
where F_LREAL = TO_DATE('{}', 'DD/MM/YYYY')