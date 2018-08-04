% Generar Agenda
unicom = '1120';
data = readtable(['data/unicoms/' unicom '.csv'], 'FileEncoding', 'UTF-8');
data = data(:, [2:8 18:20]);
% ??? Filter bad itins

% 