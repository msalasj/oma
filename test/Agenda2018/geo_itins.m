
%% pegar delegación
data = readtable('data/itins.csv', 'FileEncoding', 'UTF-8');
data.Properties.VariableNames{4} = 'ITIN';
ud = readtable('data/unicom_del.csv', 'FileEncoding', 'UTF-8');
ud.Properties.VariableNames{1} = 'UNICOM';
[posa, posb] = ismember(data.UNICOM, ud.UNICOM);
data.DELEGACION = cell(height(data), 1);
data.DELEGACION(:) = {'NULL'};
data.DELEGACION(posa) = ud.DELEGACION(posb(posa));
writetable(data, 'data/itins.csv')
%% local - itins - tar:
data = readtable('data/itins.csv', 'FileEncoding', 'UTF-8');
lit = readtable('data/local_itins_tar.csv', 'FileEncoding', 'UTF-8');
lit.Properties.VariableNames{1} = 'DEPARTAMENTO';
uri = unique(lit(:,6:8),'rows');
n = height(data);
data.DEPARTAMENTO = cell(n, 1);
data.MUNICIPIO = cell(n, 1);
data.CORREGIMIENTO = cell(n, 1);
data.BARRIO = cell(n, 1);
data(:,12:15) = {'NULL'};
% process
h = waitbar(0);
n = height(uri);
for i = 1:n
    posi = ismember(lit(:,6:8), uri(i,:),'rows');
    xi = lit(posi,:);
    x = varfun(@sum, xi, 'InputVariables','SUMINISTROS', ...
        'GroupingVariables', xi.Properties.VariableNames(1:4));
    x = sortrows(x,'sum_SUMINISTROS','descend');
    px = find(ismember(data(:,2:4), uri(i,:),'rows'));
    data.DEPARTAMENTO(px) = x.DEPARTAMENTO(1);
    data.MUNICIPIO(px) = x.MUNICIPIO(1);
    data.CORREGIMIENTO(px) = x.CORREGIMIENTO(1);
    data.BARRIO(px) = x.BARRIO(1);
    tc = sum(x.sum_SUMINISTROS);
    if tc > data.CLIENTES(px)
        data.CLIENTES(px) = tc;
    end
    waitbar(i/n)
end
close(h)
disp('listo')
writetable(data,'data/new_itins.csv')
%% geo - del
dm = readtable('data/local_itins_tar.csv', 'FileEncoding', 'UTF-8');
[dm, ind] = unique(dm(:,1:2), 'rows');
dm.Properties.VariableNames{1} = 'DEPARTAMENTO';
[posa, posb] = ismember(dm, geo_del(:,2:3), 'rows');
dm.DEL = cell(height(dm), 1);
dm.DEL(posa) = geo_del.DEL(posb(posa));
writetable(dm,'data/geo_del.csv')
%% lat - lon con google::: si no dan el orden
for i = 1:height(dm)
    dmi = [dm.DEPARTAMENTO{i} ', ' dm.MUNICIPIO{i}];
    
end
%% pegar lat - lon
Data = Data(Data.LAT ~= 0,1:6);
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
n = height(data);
data.LAT = zeros(n,1);
data.LON = zeros(n,1);
x = varfun(@median, Data, 'InputVariables',{'LAT','LON'}, ...
        'GroupingVariables', Data.Properties.VariableNames(4:6));
[posa, posb] = ismember(data(:,2:4), x(:,1:3), 'rows');
data.LAT(posa) = x.median_LAT(posb(posa));
data.LON(posa) = x.median_LON(posb(posa));
writetable(data,'data/new_itins2.csv')
%% completar lat-lon
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
x = data(data.LAT > 0,:);
pos = find(data.LAT == 0 & data.CLIENTES > 0);
h = waitbar(0);
for i = 1:length(pos)
    % MCB
    p1 = ismember(x(:,13:15), data(pos(i),13:15));
    if sum(p1) > 0
        data.LAT(pos(i)) = mean(x.LAT(p1)) + (-1 + 2*rand)*km2deg(1);
        data.LON(pos(i)) = mean(x.LON(p1)) + (-1 + 2*rand)*km2deg(1);
%     else
%         % MC
%         p2 = ismember(x(:,13:14), data(pos(i),13:14));
%         if sum(p2) > 0
%             data.LAT(pos(i)) = mean(x.LAT(p2)) + ...
%                 (-1 + 2*rand)*km2deg(5);
%             data.LON(pos(i)) = mean(x.LON(p2)) + ...
%                 (-1 + 2*rand)*km2deg(5);
%         end
    end
    waitbar(i/length(pos))
end
close(h)
writetable(data,'data/new_itins2.csv')
%% DM lat-lon
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
x = data(data.LAT > 0,:);
% DM
dm = unique(data(:,12:13),'rows');
n = height(dm);
dm.LAT = zeros(n,1);
dm.LON = zeros(n,1);
for i = 1:height(dm)
    pi = ismember(x(:,12:13), dm(i,1:2));
    if sum(pi) > 0
        dm.LAT(i) = median(x.LAT(pi));
        dm.LON(i) = median(x.LON(pi));
    end
end
writetable(dm,'data/dm.csv')
% DMC
dmc = unique(data(:,12:14),'rows');
n = height(dmc);
dmc.LAT = zeros(n,1);
dmc.LON = zeros(n,1);
for i = 1:n
    pi = ismember(x(:,12:14), dmc(i,1:3));
    if sum(pi) > 0
        dmc.LAT(i) = median(x.LAT(pi));
        dmc.LON(i) = median(x.LON(pi));
    end
end
writetable(dmc,'data/dmc.csv')
%% Calcular dia de lectura del itinerario dentro del unicom
data = readtable('data/new_itins.csv', 'FileEncoding', 'UTF-8');
unicoms = unique(data.UNICOM);
fechas = datenum(data.F_INI,'mm/dd/yy');
data.DIA = zeros(height(data),1);
for i = 1:length(unicoms)
    pos = data.UNICOM == unicoms(i);
    f = unique(fechas(pos));
    for j = 1:length(f)
        pj = pos & (fechas == f(j));
        data.DIA(pj) = j;
    end
    disp(['Maximo dia en unicom ' num2str(unicoms(i)) ' ' num2str(j) ...
        ' fecha: ' datestr(f(j))])
end
writetable(data,'data/new_itins2.csv')

