load('metricas_14.mat'); %métricas del paciente
load('metricas_controles.mat'); %métricas de los controles

%Betweenness Centrality
BC_PAT = BC_14;
mm = length(BC_PAT);
diferencia_BC = zeros(1,mm);
%Crawford-Howell t-test for Betweenness Centrality:
for i=1:mm
    control_vec_BC = [BC_c01(i) BC_c02(i) BC_c03(i) BC_c04(i) BC_c05(i) BC_c06(i) BC_c07(i) BC_c08(i) BC_c09(i) BC_c10(i) BC_c11(i) BC_c12(i) BC_c13(i) BC_c14(i) BC_c15(i) BC_c16(i) BC_c17(i) BC_c18(i) BC_c19(i) BC_c20(i) BC_c21(i) BC_c22(i) BC_c23(i) BC_c24(i) BC_c25(i) BC_c26(i) BC_c27(i) BC_c28(i) BC_c29(i) BC_c30(i) BC_c31(i) BC_c32(i) BC_c33(i) BC_c34(i) BC_c35(i) BC_c36(i) BC_c37(i) BC_c38(i) BC_c39(i) BC_c40(i)];
    diferencia_BC(i) = CrawfordHowell(BC_PAT(i),control_vec_BC);
end
%csvwrite('Diferencia_BC.csv',diferencia_BC);
figure
imagesc(diferencia_BC);
colorbar
set(gca,'ColorScale','log');
title('Betweenness Centrality Diferencia');



%Cluster Coefficient
cluster_coef_PAT = cluster_coef_14;
mm = length(cluster_coef_PAT);
diferencia_clustercoef = zeros(1,mm);
%Crawford-Howell t-test for Cluster Coefficient:
for i=1:mm
    control_vec_clustercoef = [cluster_coef_c01(i) cluster_coef_c02(i) cluster_coef_c03(i) cluster_coef_c04(i) cluster_coef_c05(i) cluster_coef_c06(i) cluster_coef_c07(i) cluster_coef_c08(i) cluster_coef_c09(i) cluster_coef_c10(i) cluster_coef_c11(i) cluster_coef_c12(i) cluster_coef_c13(i) cluster_coef_c14(i) cluster_coef_c15(i) cluster_coef_c16(i) cluster_coef_c17(i) cluster_coef_c18(i) cluster_coef_c19(i) cluster_coef_c20(i) cluster_coef_c21(i) cluster_coef_c22(i) cluster_coef_c23(i) cluster_coef_c24(i) cluster_coef_c25(i) cluster_coef_c26(i) cluster_coef_c27(i) cluster_coef_c28(i) cluster_coef_c29(i) cluster_coef_c30(i) cluster_coef_c31(i) cluster_coef_c32(i) cluster_coef_c33(i) cluster_coef_c34(i) cluster_coef_c35(i) cluster_coef_c36(i) cluster_coef_c37(i) cluster_coef_c38(i) cluster_coef_c39(i) cluster_coef_c40(i)];
    diferencia_clustercoef(i) = CrawfordHowell(cluster_coef_PAT(i),control_vec_clustercoef);
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_clustercoef);
colorbar
set(gca,'ColorScale','log');
title('Cluster Coefficient Diferencia');



%Distance matrix
distance_matrix_PAT = distance_matrix_14;
[mm, nn] = size(distance_matrix_PAT);
diferencia_distancematrix = zeros(mm,nn);
%Crawford-Howell t-test for Distance Matrix:
for i=1:mm
    for j=1:nn
        control_vec_distancematrix=[distance_matrix_c01(i,j) distance_matrix_c02(i,j) distance_matrix_c03(i,j) distance_matrix_c04(i,j) distance_matrix_c05(i,j) distance_matrix_c06(i,j) distance_matrix_c07(i,j) distance_matrix_c08(i,j) distance_matrix_c09(i,j) distance_matrix_c10(i,j) distance_matrix_c11(i,j) distance_matrix_c12(i,j) distance_matrix_c13(i,j) distance_matrix_c14(i,j) distance_matrix_c15(i,j) distance_matrix_c16(i,j) distance_matrix_c17(i,j) distance_matrix_c18(i,j) distance_matrix_c19(i,j) distance_matrix_c20(i,j) distance_matrix_c21(i,j) distance_matrix_c22(i,j) distance_matrix_c23(i,j) distance_matrix_c24(i,j) distance_matrix_c25(i,j) distance_matrix_c26(i,j) distance_matrix_c27(i,j) distance_matrix_c28(i,j) distance_matrix_c29(i,j) distance_matrix_c30(i,j) distance_matrix_c31(i,j) distance_matrix_c32(i,j) distance_matrix_c33(i,j) distance_matrix_c34(i,j) distance_matrix_c35(i,j) distance_matrix_c36(i,j) distance_matrix_c37(i,j) distance_matrix_c38(i,j) distance_matrix_c39(i,j) distance_matrix_c40(i,j)];
        diferencia_distancematrix(i,j)=CrawfordHowell(distance_matrix_PAT(i,j),control_vec_distancematrix);
    end
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_distancematrix);
colorbar
set(gca,'ColorScale','log');
title('Distance Matrix Diferencia');



%Edges
edges_PAT = edges_14;
%Crawford-Howell t-test for edges:
control_vec_edges=[edges_c01 edges_c02 edges_c01 edges_c03 edges_c04 edges_c05 edges_c06 edges_c07 edges_c08 edges_c09 edges_c10 edges_c11 edges_c12 edges_c13 edges_c14 edges_c15 edges_c16 edges_c17 edges_c18 edges_c19 edges_c20 edges_c21 edges_c22 edges_c23 edges_c24 edges_c25 edges_c26 edges_c27 edges_c28 edges_c29 edges_c30 edges_c31 edges_c32 edges_c33 edges_c34 edges_c35 edges_c36 edges_c37 edges_c38 edges_c39 edges_c40];
diferencia_edges = CrawfordHowell(edges_PAT,control_vec_edges);



%Edges_distance
edgesdistance_PAT = edges_distance_14;
[mm, nn] = size(edgesdistance_PAT);
diferencia_edgesdistance = zeros(mm,nn);
%Crawford-Howell t-test for Edges Distance:
for i=1:mm
    for j=1:nn
        control_vec_edgesdistance=[edges_distance_c01(i,j) edges_distance_c02(i,j) edges_distance_c03(i,j) edges_distance_c04(i,j) edges_distance_c05(i,j) edges_distance_c06(i,j) edges_distance_c07(i,j) edges_distance_c08(i,j) edges_distance_c09(i,j) edges_distance_c10(i,j) edges_distance_c11(i,j) edges_distance_c12(i,j) edges_distance_c13(i,j) edges_distance_c14(i,j) edges_distance_c15(i,j) edges_distance_c16(i,j) edges_distance_c17(i,j) edges_distance_c18(i,j) edges_distance_c19(i,j) edges_distance_c20(i,j) edges_distance_c21(i,j) edges_distance_c22(i,j) edges_distance_c23(i,j) edges_distance_c24(i,j) edges_distance_c25(i,j) edges_distance_c26(i,j) edges_distance_c27(i,j) edges_distance_c28(i,j) edges_distance_c29(i,j) edges_distance_c30(i,j) edges_distance_c31(i,j) edges_distance_c32(i,j) edges_distance_c33(i,j) edges_distance_c34(i,j) edges_distance_c35(i,j) edges_distance_c36(i,j) edges_distance_c37(i,j) edges_distance_c38(i,j) edges_distance_c39(i,j) edges_distance_c40(i,j)];
        diferencia_edgesdistance(i,j)=CrawfordHowell(edgesdistance_PAT(i,j),control_vec_edgesdistance);
    end
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_edgesdistance);
colorbar
set(gca,'ColorScale','log');
title('Edges Distance Diferencia');



%Global Efficiency
globalefficiency_PAT = global_efficiency_14;
%Crawford-Howell t-test for global efficiency:
control_vec_globaleff=[global_efficiency_c01 global_efficiency_c02 global_efficiency_c03 global_efficiency_c04 global_efficiency_c05 global_efficiency_c06 global_efficiency_c07 global_efficiency_c08 global_efficiency_c09 global_efficiency_c10 global_efficiency_c11 global_efficiency_c12 global_efficiency_c13 global_efficiency_c14 global_efficiency_c15 global_efficiency_c16 global_efficiency_c17 global_efficiency_c18 global_efficiency_c19 global_efficiency_c20 global_efficiency_c21 global_efficiency_c22 global_efficiency_c23 global_efficiency_c24 global_efficiency_c25 global_efficiency_c26 global_efficiency_c27 global_efficiency_c28 global_efficiency_c29 global_efficiency_c30 global_efficiency_c31 global_efficiency_c32 global_efficiency_c33 global_efficiency_c34 global_efficiency_c35 global_efficiency_c36 global_efficiency_c37 global_efficiency_c38 global_efficiency_c39 global_efficiency_c40];
diferencia_globaleff = CrawfordHowell(globalefficiency_PAT,control_vec_globaleff);



%Local efficiency
localeff_PAT = local_efficiency_14;
mm = length(localeff_PAT);
diferencia_localeff = zeros(1,mm);
%Crawford-Howell t-test for Local Efficiency:
for i=1:mm
    control_vec_localeff = [local_efficiency_c01(i) local_efficiency_c02(i) local_efficiency_c03(i) local_efficiency_c04(i) local_efficiency_c05(i) local_efficiency_c06(i) local_efficiency_c07(i) local_efficiency_c08(i) local_efficiency_c09(i) local_efficiency_c10(i) local_efficiency_c11(i) local_efficiency_c12(i) local_efficiency_c13(i) local_efficiency_c14(i) local_efficiency_c15(i) local_efficiency_c16(i) local_efficiency_c17(i) local_efficiency_c18(i) local_efficiency_c19(i) local_efficiency_c20(i) local_efficiency_c21(i) local_efficiency_c22(i) local_efficiency_c23(i) local_efficiency_c24(i) local_efficiency_c25(i) local_efficiency_c26(i) local_efficiency_c27(i) local_efficiency_c28(i) local_efficiency_c29(i) local_efficiency_c30(i) local_efficiency_c31(i) local_efficiency_c32(i) local_efficiency_c33(i) local_efficiency_c34(i) local_efficiency_c35(i) local_efficiency_c36(i) local_efficiency_c37(i) local_efficiency_c38(i) local_efficiency_c39(i) local_efficiency_c40(i)];
    diferencia_localeff(i) = CrawfordHowell(localeff_PAT(i),control_vec_localeff);
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_localeff);
colorbar
set(gca,'ColorScale','log');
title('Local Efficiency Diferencia');



%Strengths
str_PAT = str_14;
mm = length(str_PAT);
diferencia_str = zeros(1,mm);
%Crawford-Howell t-test for strengths:
for i=1:mm
    control_vec_str = [str_c01(i) str_c02(i) str_c03(i) str_c04(i) str_c05(i) str_c06(i) str_c07(i) str_c08(i) str_c09(i) str_c10(i) str_c11(i) str_c12(i) str_c13(i) str_c14(i) str_c15(i) str_c16(i) str_c17(i) str_c18(i) str_c19(i) str_c20(i) str_c21(i) str_c22(i) str_c23(i) str_c24(i) str_c25(i) str_c26(i) str_c27(i) str_c28(i) str_c29(i) str_c30(i) str_c31(i) str_c32(i) str_c33(i) str_c34(i) str_c35(i) str_c36(i) str_c37(i) str_c38(i) str_c39(i) str_c40(i)];
    diferencia_str(i) = CrawfordHowell(str_PAT(i),control_vec_str);
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_str);
colorbar
set(gca,'ColorScale','log');
title('Strengths Diferencia');



%Density
density_PAT = density_14;
%Crawford-Howell t-test for density:
control_vec_density=[density_c01 density_c02 density_c03 density_c04 density_c05 density_c06 density_c07 density_c08 density_c09 density_c10 density_c11 density_c12 density_c13 density_c14 density_c15 density_c16 density_c17 density_c18 density_c19 density_c20 density_c21 density_c22 density_c23 density_c24 density_c25 density_c26 density_c27 density_c28 density_c29 density_c30 density_c31 density_c32 density_c33 density_c34 density_c35 density_c36 density_c37 density_c38 density_c39 density_c40];
diferencia_density = CrawfordHowell(density_PAT,control_vec_density);



%Degree
deg_PAT = deg_14;
mm = length(deg_PAT);
diferencia_deg = zeros(1,mm);
%Crawford-Howell t-test for strengths:
for i=1:mm
    control_vec_deg = [deg_c01(i) deg_c02(i) deg_c03(i) deg_c04(i) deg_c05(i) deg_c06(i) deg_c07(i) deg_c08(i) deg_c09(i) deg_c10(i) deg_c11(i) deg_c12(i) deg_c13(i) deg_c14(i) deg_c15(i) deg_c16(i) deg_c17(i) deg_c18(i) deg_c19(i) deg_c20(i) deg_c21(i) deg_c22(i) deg_c23(i) deg_c24(i) deg_c25(i) deg_c26(i) deg_c27(i) deg_c28(i) deg_c29(i) deg_c30(i) deg_c31(i) deg_c32(i) deg_c33(i) deg_c34(i) deg_c35(i) deg_c36(i) deg_c37(i) deg_c38(i) deg_c39(i) deg_c40(i)];
    diferencia_deg(i) = CrawfordHowell(deg_PAT(i),control_vec_deg);
end
%csvwrite('Diferencia_clustercoef.csv',diferencia_clustercoef);
figure
imagesc(diferencia_deg);
colorbar
set(gca,'ColorScale','log');
title('Degree Diferencia');



%definición de la función que permite realizar el test Crawford-Howell
function[pval]=CrawfordHowell(paciente,control)
    longitud=length(control);
    tval=(paciente-mean(control))./(std(control).*sqrt((longitud+1)./longitud));
    degfre=longitud-1;
    pval=2*(1-tcdf(abs(tval),degfre));
end