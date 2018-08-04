% Optimización de Dias
% test para un unicom: 1120
unicom = 1120;
unicom_del = readtable('data/unicom_del.csv', 'FileEncoding', 'UTF-8');
unicom_del.Properties.VariableNames{1} = 'UNICOM';
head = unicom_del.HEAD(ismember(unicom_del.UNICOM,unicom));
% load data
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
% Filters
pos = data.CLIENTES > 0 & ismember(data.TIPO2,'NORMAL');
data = data(pos, :);
% unicom
data = data(data.UNICOM == unicom, :);
% Ver orden de municipios
M = unique(data.CORREGIMIENTO);
dias = unique(data.DIA);
x = zeros(length(M), length(dias));
y = zeros(length(M), length(dias));
for i = 1:length(M)
    pi = ismember(data.CORREGIMIENTO,M{i});
    for j = 1:length(dias)
        pj = pi & data.DIA == dias(j);
        x(i,j) = sum(data.CLIENTES(pj));
        y(i,j) = sum(pj);
    end
end
data.NEW_DAY = zeros(height(data),1);
%% Ordenar Corregimientos
% parametros
% inicialmente tomar el orden que ya viene analizando la diagonal, pero
% proponer una manera óptima generar dicho orden: de norte a sur
orden = ordenar_corregimientos(head, data);
% orden = {'CGTO JUAN MINA', ... 
%     'VILLA CAMPESTRE', ...
%     'EDUARDO SANTOS (LA PLAYA)', ...
%     'CGTO SABANILLA (MONTE CARMELO)', ...
%     'CGTO SALGAR', ...
%     'PUERTO COLOMBIA'};
dia_max = max(dias);
pki = 1.03;
pos = ismember(data.CORREGIMIENTO, orden);
sw = sum(data.CLIENTES(pos))/dia_max;
subdata = data(pos, :);
% sort subdata
subdata.NUMCOR = zeros(height(subdata),1);
for i = 1:length(orden)
    pi = ismember(subdata.CORREGIMIENTO,orden(i));
    subdata.NUMCOR(pi) = i;
end
subdata = sortrows(subdata,{'NUMCOR', 'DIA'},'ascend');
% new day
newday = zeros(height(subdata),1);
cxd_ini = zeros(1, dia_max);
for i = 1:dia_max
    pi = find(newday == 0,1);
    % TODO: if pi isempty
    newday(pi) = i;
    ccd = sum(subdata.CLIENTES(newday == i));
    while ccd <= pki*sw
        pi = find(newday == 0,1);
        if ~(isempty(pi))
            if (ccd + subdata.CLIENTES(pi)) <= pki*sw
                newday(pi) = i;
                ccd = sum(subdata.CLIENTES(newday == i));
            else
                break
            end
        else
            break
        end
    end
    cxd_ini(i) = ccd;
end
subdata.NEW_DAY = newday;
figure, bar(cxd_ini), grid on
%% Optimizar Cabecera <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
if ~strcmpi(head,'')
pos = ismember(data.CORREGIMIENTO, head);
hdata = data(pos,:);
sw = sum(data.CLIENTES)/dia_max;
pki = 1.03;
% new day
dia = hdata.DIA;
newday = zeros(height(hdata),1);
cxd = zeros(1, dia_max);
h = waitbar(0);
for i = 1:dia_max
    pxy = dia == i & hdata.LAT > 0;
    cx = median(hdata.LON(pxy));
    cy = median(hdata.LAT(pxy));
    dist = sqrt((hdata.LON - cx).^2 + (hdata.LAT - cy).^2);
    dist(hdata.LAT == 0) = 0;
    [~, index] = sortrows([dia dist], [1, 2]);
    % asignar dia
    index = index(newday(index) == 0);
    ii = 1;
    newday(index(ii)) = i;
    dia(index(ii)) = i;
    ccd = cxd_ini(i) + sum(hdata.CLIENTES(newday == i));
    while ccd <= pki*sw
        if (ii + 1) <= length(index)
            if (ccd + hdata.CLIENTES(index(ii + 1))) <= pki*sw
                ii = ii + 1;
                newday(index(ii)) = i;
                dia(index(ii)) = i;
                ccd = cxd_ini(i) + sum(hdata.CLIENTES(newday == i));
            else
                % cambiar el dia de los previos
                dia(dia == i & newday == 0) = i + 1;
                break
            end
        else
            break
        end
    end
    cxd(i) = ccd;
    waitbar(i/dia_max)
end
hdata.NEW_DAY = newday;
close(h)
figure, bar(cxd), grid on
end
% optimización final de itins con altas desviaciones geograficas
% % Este proceso debe ser un intercambio: 
% dgeo = zeros(1, dia_max);
% for i = 1:dia_max
%     posi = hdata.NEW_DAY == i & hdata.LAT > 0;
%     cx = median(hdata.LON(posi));
%     cy = median(hdata.LAT(posi));
%     dist = sqrt((hdata.LON(posi) - cx).^2 + (hdata.LAT(posi) - cy).^2);
%     dgeo(i) = deg2km(mean(dist));
%     disp(deg2km(max(dist)))
% end
% 
% %% Dispersion geografica actual 
% dgeo_ini = zeros(1, dia_max);
% for i = 1:dia_max
%     posi = data.DIA == i & data.LAT > 0 & ismember(data.CORREGIMIENTO,'BARRANQUILLA');
%     cx = median(data.LON(posi));
%     cy = median(data.LAT(posi));
%     dist = sqrt((data.LON(posi) - cx).^2 + (data.LAT(posi) - cy).^2);
%     dgeo_ini(i) = deg2km(mean(dist));
% end

% Agrupar Resultados
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
data = data(data.UNICOM == unicom, :);
data.NEW_DAY = zeros(height(data),1);
data.OPTIMIZADO = zeros(height(data),1);
% subdata
[posa, posb] = ismember(data(:,2:4), subdata(:,2:4),'rows');
data.NEW_DAY(posa) = subdata.NEW_DAY(posb(posa));
data.OPTIMIZADO(posa) = 1;
% hdata
if ~strcmpi(head,'')
[posa, posb] = ismember(data(:,2:4), hdata(:,2:4),'rows');
data.NEW_DAY(posa) = hdata.NEW_DAY(posb(posa));
data.OPTIMIZADO(posa) = 1;
end
% completar new_day ==0
data.NEW_DAY(data.NEW_DAY == 0) = data.DIA(data.NEW_DAY == 0);
% sort
data = sortrows(data,'DIA','ascend');
% save
writetable(data,['data/unicoms/' num2str(unicom) '.csv'])
