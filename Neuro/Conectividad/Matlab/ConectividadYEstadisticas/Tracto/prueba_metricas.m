load('metricas_04.mat'); %métricas del paciente
load('metricas_controles.mat'); %métricas de los controles

%Betweenness Centrality
%BC_PAT = BC_04;
mm = length(BC_04);
diferencia_BC = zeros(1,mm);
%Crawford-Howell t-test for Betweenness Centrality:
for i=1:mm
    control_vec_BC = [BC_c01(i) BC_c02(i) BC_c03(i) BC_c04(i) BC_c05(i) BC_c06(i) BC_c07(i) BC_c08(i) BC_c09(i) BC_c10(i) BC_c11(i) BC_c12(i) BC_c13(i) BC_c14(i) BC_c15(i) BC_c16(i) BC_c17(i) BC_c18(i) BC_c19(i) BC_c20(i) BC_c21(i) BC_c22(i) BC_c23(i) BC_c24(i) BC_c25(i) BC_c26(i) BC_c27(i) BC_c28(i) BC_c29(i) BC_c30(i) BC_c31(i) BC_c32(i) BC_c33(i) BC_c34(i) BC_c35(i) BC_c36(i) BC_c37(i) BC_c38(i) BC_c39(i) BC_c40(i)];
    diferencia_BC(i) = CrawfordHowell(BC_04(i),control_vec_BC);
end
%csvwrite('Diferencia_BC.csv',diferencia_BC);
figure
imagesc(diferencia_BC);
colorbar
set(gca,'ColorScale','log');
title('Betweenness Centrality Diferencia');




%definición de la función que permite realizar el test Crawford-Howell
function[pval]=CrawfordHowell(paciente,control)
    longitud=length(control);
    tval=(paciente-mean(control))./(std(control).*sqrt((longitud+1)./longitud));
    degfre=longitud-1;
    pval=2*(1-tcdf(abs(tval),degfre));
end