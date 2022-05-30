%Cargar matriz paciente
Zmat = load('Lopez_conn.csv');
%Zmat = Rococonn;
load('workspace_controles1a70.mat');
UmbralConect=0;%Para evitar falsos positivos
[mm,nn]=size(Zmat);
Znorm=zeros(mm,nn);

for i=1:mm
    for j=1:nn
        if Zmat(i,j)>UmbralConect
                Znorm(i,j)=Zmat(i,j);
        else
            Znorm(i,j)=0;            
        end
    end
end

%Cargar matrices controles

control1_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control1_conn_matrix(i,j)>UmbralConect
                control1_norm(i,j)=control1_conn_matrix(i,j);
        else
            control1_norm(i,j)=0;            
        end
    end
end

control2_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control2_conn_matrix(i,j)>UmbralConect
                control2_norm(i,j)=control2_conn_matrix(i,j);
        else
            control2_norm(i,j)=0;            
        end
    end
end

control3_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control3_conn_matrix(i,j)>UmbralConect
                control3_norm(i,j)=control3_conn_matrix(i,j);
        else
            control3_norm(i,j)=0;            
        end
    end
end

control4_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control4_conn_matrix(i,j)>UmbralConect
                control4_norm(i,j)=control4_conn_matrix(i,j);
        else
            control4_norm(i,j)=0;            
        end
    end
end

control5_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control5_conn_matrix(i,j)>UmbralConect
                control5_norm(i,j)=control5_conn_matrix(i,j);
        else
            control5_norm(i,j)=0;            
        end
    end
end

control6_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control6_conn_matrix(i,j)>UmbralConect
                control6_norm(i,j)=control6_conn_matrix(i,j);
        else
            control6_norm(i,j)=0;            
        end
    end
end

control7_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control7_conn_matrix(i,j)>UmbralConect
                control7_norm(i,j)=control7_conn_matrix(i,j);
        else
            control7_norm(i,j)=0;            
        end
    end
end

control8_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control8_conn_matrix(i,j)>UmbralConect
                control8_norm(i,j)=control8_conn_matrix(i,j);
        else
            control8_norm(i,j)=0;            
        end
    end
end

control9_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control9_conn_matrix(i,j)>UmbralConect
                control9_norm(i,j)=control9_conn_matrix(i,j);
        else
            control9_norm(i,j)=0;            
        end
    end
end

control10_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control10_conn_matrix(i,j)>UmbralConect
                control10_norm(i,j)=control10_conn_matrix(i,j);
        else
            control10_norm(i,j)=0;            
        end
    end
end

control11_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control11_conn_matrix(i,j)>UmbralConect
                control11_norm(i,j)=control11_conn_matrix(i,j);
        else
            control11_norm(i,j)=0;            
        end
    end
end

control12_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control12_conn_matrix(i,j)>UmbralConect
                control12_norm(i,j)=control12_conn_matrix(i,j);
        else
            control12_norm(i,j)=0;            
        end
    end
end

control13_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control13_conn_matrix(i,j)>UmbralConect
                control13_norm(i,j)=control13_conn_matrix(i,j);
        else
            control13_norm(i,j)=0;            
        end
    end
end

control14_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control14_conn_matrix(i,j)>UmbralConect
                control14_norm(i,j)=control14_conn_matrix(i,j);
        else
            control14_norm(i,j)=0;            
        end
    end
end

control15_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control15_conn_matrix(i,j)>UmbralConect
                control15_norm(i,j)=control15_conn_matrix(i,j);
        else
            control15_norm(i,j)=0;            
        end
    end
end

control16_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control16_conn_matrix(i,j)>UmbralConect
                control16_norm(i,j)=control16_conn_matrix(i,j);
        else
            control16_norm(i,j)=0;            
        end
    end
end

control17_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control17_conn_matrix(i,j)>UmbralConect
                control17_norm(i,j)=control17_conn_matrix(i,j);
        else
            control17_norm(i,j)=0;            
        end
    end
end

control18_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control18_conn_matrix(i,j)>UmbralConect
                control18_norm(i,j)=control18_conn_matrix(i,j);
        else
            control18_norm(i,j)=0;            
        end
    end
end

control19_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control19_conn_matrix(i,j)>UmbralConect
                control19_norm(i,j)=control19_conn_matrix(i,j);
        else
            control19_norm(i,j)=0;            
        end
    end
end

control20_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control20_conn_matrix(i,j)>UmbralConect
                control20_norm(i,j)=control20_conn_matrix(i,j);
        else
            control20_norm(i,j)=0;            
        end
    end
end

control21_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control21_conn_matrix(i,j)>UmbralConect
                control21_norm(i,j)=control21_conn_matrix(i,j);
        else
            control21_norm(i,j)=0;            
        end
    end
end

control22_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control22_conn_matrix(i,j)>UmbralConect
                control22_norm(i,j)=control22_conn_matrix(i,j);
        else
            control22_norm(i,j)=0;            
        end
    end
end

control23_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control23_conn_matrix(i,j)>UmbralConect
                control23_norm(i,j)=control23_conn_matrix(i,j);
        else
            control23_norm(i,j)=0;            
        end
    end
end

control24_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control24_conn_matrix(i,j)>UmbralConect
                control24_norm(i,j)=control24_conn_matrix(i,j);
        else
            control24_norm(i,j)=0;            
        end
    end
end

control25_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control25_conn_matrix(i,j)>UmbralConect
                control25_norm(i,j)=control25_conn_matrix(i,j);
        else
            control25_norm(i,j)=0;            
        end
    end
end

control26_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control26conn(i,j)>UmbralConect
                control26_norm(i,j)=control26conn(i,j);
        else
            control26_norm(i,j)=0;            
        end
    end
end

control27_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control27conn(i,j)>UmbralConect
                control27_norm(i,j)=control27conn(i,j);
        else
            control27_norm(i,j)=0;            
        end
    end
end

control28_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control28conn(i,j)>UmbralConect
                control28_norm(i,j)=control28conn(i,j);
        else
            control28_norm(i,j)=0;            
        end
    end
end

control29_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control29conn(i,j)>UmbralConect
                control29_norm(i,j)=control29conn(i,j);
        else
            control29_norm(i,j)=0;            
        end
    end
end

control30_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control30conn(i,j)>UmbralConect
                control30_norm(i,j)=control30conn(i,j);
        else
            control30_norm(i,j)=0;            
        end
    end
end

control31_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control31conn(i,j)>UmbralConect
                control31_norm(i,j)=control31conn(i,j);
        else
            control31_norm(i,j)=0;            
        end
    end
end

control32_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control32conn(i,j)>UmbralConect
                control32_norm(i,j)=control32conn(i,j);
        else
            control32_norm(i,j)=0;            
        end
    end
end

control33_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control33conn(i,j)>UmbralConect
                control33_norm(i,j)=control33conn(i,j);
        else
            control33_norm(i,j)=0;            
        end
    end
end

control34_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control34conn(i,j)>UmbralConect
                control34_norm(i,j)=control34conn(i,j);
        else
            control34_norm(i,j)=0;            
        end
    end
end

control35_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control35conn(i,j)>UmbralConect
                control35_norm(i,j)=control35conn(i,j);
        else
            control35_norm(i,j)=0;            
        end
    end
end

control36_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control36conn(i,j)>UmbralConect
                control36_norm(i,j)=control36conn(i,j);
        else
            control36_norm(i,j)=0;            
        end
    end
end

control37_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control37conn(i,j)>UmbralConect
                control37_norm(i,j)=control37conn(i,j);
        else
            control37_norm(i,j)=0;            
        end
    end
end

control38_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control38conn(i,j)>UmbralConect
                control38_norm(i,j)=control38conn(i,j);
        else
            control38_norm(i,j)=0;            
        end
    end
end

control39_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control39conn(i,j)>UmbralConect
                control39_norm(i,j)=control39conn(i,j);
        else
            control39_norm(i,j)=0;            
        end
    end
end

control40_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control40conn(i,j)>UmbralConect
                control40_norm(i,j)=control40conn(i,j);
        else
            control40_norm(i,j)=0;            
        end
    end
end

control41_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control41conn(i,j)>UmbralConect
                control41_norm(i,j)=control41conn(i,j);
        else
            control41_norm(i,j)=0;            
        end
    end
end

control42_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control42conn(i,j)>UmbralConect
                control42_norm(i,j)=control42conn(i,j);
        else
            control42_norm(i,j)=0;            
        end
    end
end

control43_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control43conn(i,j)>UmbralConect
                control43_norm(i,j)=control43conn(i,j);
        else
            control43_norm(i,j)=0;            
        end
    end
end

control44_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control44conn(i,j)>UmbralConect
                control44_norm(i,j)=control44conn(i,j);
        else
            control44_norm(i,j)=0;            
        end
    end
end

control45_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control45conn(i,j)>UmbralConect
                control45_norm(i,j)=control45conn(i,j);
        else
            control45_norm(i,j)=0;            
        end
    end
end

control46_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control46conn(i,j)>UmbralConect
                control46_norm(i,j)=control46conn(i,j);
        else
            control46_norm(i,j)=0;            
        end
    end
end

control47_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control47conn(i,j)>UmbralConect
                control47_norm(i,j)=control47conn(i,j);
        else
            control47_norm(i,j)=0;            
        end
    end
end

control48_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control48conn(i,j)>UmbralConect
                control48_norm(i,j)=control48conn(i,j);
        else
            control48_norm(i,j)=0;            
        end
    end
end

control49_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control49conn(i,j)>UmbralConect
                control49_norm(i,j)=control49conn(i,j);
        else
            control49_norm(i,j)=0;            
        end
    end
end

control50_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control50conn(i,j)>UmbralConect
                control50_norm(i,j)=control50conn(i,j);
        else
            control50_norm(i,j)=0;            
        end
    end
end

control51_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control51conn(i,j)>UmbralConect
                control51_norm(i,j)=control51conn(i,j);
        else
            control51_norm(i,j)=0;            
        end
    end
end

control52_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control52conn(i,j)>UmbralConect
                control52_norm(i,j)=control52conn(i,j);
        else
            control52_norm(i,j)=0;            
        end
    end
end

control53_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control53conn(i,j)>UmbralConect
                control53_norm(i,j)=control53conn(i,j);
        else
            control53_norm(i,j)=0;            
        end
    end
end

control54_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control54conn(i,j)>UmbralConect
                control54_norm(i,j)=control54conn(i,j);
        else
            control54_norm(i,j)=0;            
        end
    end
end

control55_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control55conn(i,j)>UmbralConect
                control55_norm(i,j)=control55conn(i,j);
        else
            control55_norm(i,j)=0;            
        end
    end
end

control56_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control56conn(i,j)>UmbralConect
                control56_norm(i,j)=control56conn(i,j);
        else
            control56_norm(i,j)=0;            
        end
    end
end

control57_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control57conn(i,j)>UmbralConect
                control57_norm(i,j)=control57conn(i,j);
        else
            control57_norm(i,j)=0;            
        end
    end
end

control58_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control58conn(i,j)>UmbralConect
                control58_norm(i,j)=control58conn(i,j);
        else
            control58_norm(i,j)=0;            
        end
    end
end

control59_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control59conn(i,j)>UmbralConect
                control59_norm(i,j)=control59conn(i,j);
        else
            control59_norm(i,j)=0;            
        end
    end
end

control60_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control60conn(i,j)>UmbralConect
                control60_norm(i,j)=control60conn(i,j);
        else
            control60_norm(i,j)=0;            
        end
    end
end

control61_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control61conn(i,j)>UmbralConect
                control61_norm(i,j)=control61conn(i,j);
        else
            control61_norm(i,j)=0;            
        end
    end
end

control62_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control62conn(i,j)>UmbralConect
                control62_norm(i,j)=control62conn(i,j);
        else
            control62_norm(i,j)=0;            
        end
    end
end

control63_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control63conn(i,j)>UmbralConect
                control63_norm(i,j)=control63conn(i,j);
        else
            control63_norm(i,j)=0;            
        end
    end
end

control64_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control64conn(i,j)>UmbralConect
                control64_norm(i,j)=control64conn(i,j);
        else
            control64_norm(i,j)=0;            
        end
    end
end

control65_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control65conn(i,j)>UmbralConect
                control65_norm(i,j)=control65conn(i,j);
        else
            control65_norm(i,j)=0;            
        end
    end
end

control66_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control66conn(i,j)>UmbralConect
                control66_norm(i,j)=control66conn(i,j);
        else
            control66_norm(i,j)=0;            
        end
    end
end

control67_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control67conn(i,j)>UmbralConect
                control67_norm(i,j)=control67conn(i,j);
        else
            control67_norm(i,j)=0;            
        end
    end
end

control68_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control68conn(i,j)>UmbralConect
                control68_norm(i,j)=control68conn(i,j);
        else
            control68_norm(i,j)=0;            
        end
    end
end

control69_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control69conn(i,j)>UmbralConect
                control69_norm(i,j)=control69conn(i,j);
        else
            control69_norm(i,j)=0;            
        end
    end
end

control70_norm=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control70conn(i,j)>UmbralConect
                control70_norm(i,j)=control70conn(i,j);
        else
            control70_norm(i,j)=0;            
        end
    end
end

Diferencia=zeros(mm,nn); %Matriz que almacenará los p-valores resultantes del Crawford-Howell test

%Realiza el Crawford-Howell test entre el elemento i,j de la matriz de
%conectividad del paciente y los elementos i,j de las matrices de control
for i=1:mm
    for j=1:nn
        control_vec=[control1_norm(i,j) control2_norm(i,j) control3_norm(i,j) control4_norm(i,j) control5_norm(i,j) control6_norm(i,j) control7_norm(i,j) control8_norm(i,j) control9_norm(i,j) control10_norm(i,j) control11_norm(i,j) control12_norm(i,j) control13_norm(i,j) control14_norm(i,j) control15_norm(i,j) control16_norm(i,j) control17_norm(i,j) control18_norm(i,j) control19_norm(i,j) control20_norm(i,j) control21_norm(i,j) control22_norm(i,j) control23_norm(i,j) control24_norm(i,j) control25_norm(i,j) control26_norm(i,j) control27_norm(i,j) control28_norm(i,j) control29_norm(i,j) control30_norm(i,j) control31_norm(i,j) control32_norm(i,j) control33_norm(i,j) control34_norm(i,j) control35_norm(i,j) control36_norm(i,j) control37_norm(i,j) control38_norm(i,j) control39_norm(i,j) control40_norm(i,j) control41_norm(i,j) control42_norm(i,j) control43_norm(i,j) control44_norm(i,j) control45_norm(i,j) control46_norm(i,j) control47_norm(i,j) control48_norm(i,j) control49_norm(i,j) control50_norm(i,j) control51_norm(i,j) control52_norm(i,j) control53_norm(i,j) control54_norm(i,j) control55_norm(i,j) control56_norm(i,j) control57_norm(i,j) control58_norm(i,j) control59_norm(i,j) control60_norm(i,j) control61_norm(i,j) control62_norm(i,j) control63_norm(i,j) control64_norm(i,j) control65_norm(i,j) control66_norm(i,j) control67_norm(i,j) control68_norm(i,j) control69_norm(i,j) control70_norm(i,j)];
        Diferencia(i,j)=CrawfordHowell(Znorm(i,j),control_vec);
    end
end
csvwrite('Diferencia_14_F',Diferencia);

imagesc(Diferencia); %grafica la matriz que contiene los p-valores
colorbar
set(gca,'ColorScale','log') %escala de colores logarítmica 

%definición de la función que permite realizar el test Crawford-Howell
function[pval]=CrawfordHowell(paciente,control)
    longitud=length(control);
    tval=(paciente-mean(control))./(std(control).*sqrt((longitud+1)./longitud));
    degfre=longitud-1;
    pval=2*(1-tcdf(abs(tval),degfre));
end