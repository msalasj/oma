% Optimización de Dias
unicom = 2941;  % <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
unicom_del = readtable('data/unicom_del.csv', 'FileEncoding', 'UTF-8');
unicom_del.Properties.VariableNames{1} = 'UNICOM';
head = unicom_del.HEAD(ismember(unicom_del.UNICOM,unicom));
% load data
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
% unicom
data = data(data.UNICOM == unicom, :);
data.NEW_DAY = data.DIA;
data.Properties.VariableNames{1} = 'COD';
% plot itins
counts = hist(data.NEW_DAY, unique(data.NEW_DAY));
figure, bar(counts), grid on
%% Disminuir Dias ---------------------------------------------------------
max_dia = max(data.DIA);
% centros de cada dia
cxd = zeros(max_dia, 1);
cyd = zeros(max_dia, 1);
for i = 1:max_dia
    pxy = data.DIA == i & data.LAT > 0;
    cxd(i) = median(data.LON(pxy));
    cyd(i) = median(data.LAT(pxy));
end
% proceso
nk = 0; %<<<<<<<<<<<<<<<<<<
for i = 1:nk
    k = max_dia - (i - 1);
    posi = find(data.NEW_DAY == k);
    for j = 1:length(posi)
        ij = posi(j);
        if data.LAT(ij) == 0
            data.NEW_DAY(ij) = max_dia - nk;
        elseif (data.LAT(ij) > 0) % && ...
            % strcmpi(data.TIPO2(ij),'NORMAL')
            dist = sqrt((data.LON(ij) - cxd(1:max_dia - nk)).^2 + ...
                (data.LAT(ij) - cyd(1:max_dia - nk)).^2);
            data.NEW_DAY(ij) = find(dist == min(dist), 1, 'last');
        %else
        %    data.NEW_DAY(ij) = max_dia - nk;
        end
    end
end
dia_max = max(data.NEW_DAY);
% plot itins
counts = hist(data.NEW_DAY, unique(data.NEW_DAY));
figure, bar(counts), grid on
%% Optimizar Cabecera -----------------------------------------------------
if ~strcmpi(head,'') && false
% Filters
pos = data.CLIENTES > 0 & ismember(data.TIPO2,'NORMAL') & ...
    ismember(data.MUNICIPIO, head);
hdata = data(pos, :);
sw = floor(height(hdata)/dia_max);
pki = 1;
dia_max = length(unique(hdata.NEW_DAY));
% plot itins
counts = hist(hdata.NEW_DAY, unique(hdata.NEW_DAY));
figure, bar(counts), grid on
% new day
dia = hdata.NEW_DAY;
diasj = unique(dia);
newday = zeros(height(hdata),1);
cxd = zeros(1, dia_max);
for j = 1:dia_max
    i = diasj(j);
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
    ccd = sum(newday == i);
    while ccd <= sw
        if (ii + 1) <= length(index)
            if (ccd + 1) <= sw
                ii = ii + 1;
                newday(index(ii)) = i;
                dia(index(ii)) = i;
                ccd = sum(newday == i);
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
end
% -------
% dias = unique(hdata.NEW_DAY);
hdata.NEW_DAY = newday;
% -------
% day center
cxd = zeros(dia_max, 1);
cyd = zeros(dia_max, 1);
for i = 1:dia_max
    pxy = hdata.NEW_DAY == i & hdata.LAT > 0;
    cxd(i) = median(hdata.LON(pxy));
    cyd(i) = median(hdata.LAT(pxy));
end
% newday == 0
pos = find(newday == 0);
for i = 1:length(pos)
    if hdata.LAT(pos(i)) > 0
        dist = sqrt((hdata.LON(pos(i)) - cxd).^2 + ...
            (hdata.LAT(pos(i)) - cyd).^2);
        hdata.NEW_DAY(pos(i)) = find(dist == min(dist),1);
    else
        hdata.NEW_DAY(pos(i)) = hdata.DIA(pos(i));
    end
end
% plot itins
counts = hist(hdata.NEW_DAY, unique(hdata.NEW_DAY));
figure, bar(counts), grid on
% agrupar resultados:
[posa, posb] = ismember(data(:,2:4), hdata(:,2:4),'rows');
data.NEW_DAY(posa) = hdata.NEW_DAY(posb(posa));
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

% %% Agrupar Resultados
% data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
% data = data(data.UNICOM == unicom, :);
% data.NEW_DAY = zeros(height(data),1);
% data.OPTIMIZADO = zeros(height(data),1);
% % subdata
% [posa, posb] = ismember(data(:,2:4), subdata(:,2:4),'rows');
% data.NEW_DAY(posa) = subdata.NEW_DAY(posb(posa));
% data.OPTIMIZADO(posa) = 1;
% % hdata
% if ~strcmpi(head,'')
% [posa, posb] = ismember(data(:,2:4), hdata(:,2:4),'rows');
% data.NEW_DAY(posa) = hdata.NEW_DAY(posb(posa));
% data.OPTIMIZADO(posa) = 1;
% end
% % completar new_day ==0
% data.NEW_DAY(data.NEW_DAY == 0) = data.DIA(data.NEW_DAY == 0);
% sort
data = sortrows(data,'DIA','ascend');
% save
writetable(data,['data/unicoms/' num2str(unicom) '.csv'])
