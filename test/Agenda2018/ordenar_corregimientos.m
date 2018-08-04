function orden = ordenar_corregimientos(head, data)

corr = unique(data.CORREGIMIENTO);
corr = corr(~ismember(corr,head));
x = zeros(length(corr), 1);
for i = 1:length(corr)
    posi = ismember(data.CORREGIMIENTO,corr(i));
    x(i) = sum(data.DIA(posi).*data.CLIENTES(posi))/sum(data.CLIENTES(posi));
end
[~, index] = sort(x);
orden = corr(index);
