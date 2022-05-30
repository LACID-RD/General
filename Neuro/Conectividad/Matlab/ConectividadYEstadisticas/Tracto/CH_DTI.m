%Cargar y graficar matriz paciente (después cambiar el nombre del archivo
%donde se va a guardar según cada paciente
UmbralConect=0;%Para evitar falsos positivos
A=load('Lopez_fdt_network_matrix');
Waytotal=load('Lopez_waytotal');
[mm,nn]=size(A);
Aaver=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if A(i,j)>UmbralConect
                Aaver(i,j)=A(i,j)/Waytotal(i);
        else
            Aaver(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver(i,j)=(Aaver(i,j)+Aaver(j,i))/2;
        Aaver(j,i)=Aaver(i,j);
        if i==j
            Aaver(i,j)=1;
        end
    end
end
%csvwrite('EPI_fdt_network_matrix.csv',Aaver);

%Cargar matrices de controles
control1=load('CON048_fdt_network_matrix');
control1_waytotal=load('CON048_waytotal');

[mm,nn]=size(control1);
Aaver_c1=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control1(i,j)>UmbralConect
                Aaver_c1(i,j)=control1(i,j)/control1_waytotal(i);
        else
            Aaver_c1(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c1(i,j)=(Aaver_c1(i,j)+Aaver_c1(j,i))/2;
        Aaver_c1(j,i)=Aaver_c1(i,j);
        if i==j
            Aaver_c1(i,j)=1;
        end
    end
end
%csvwrite('control1_fdt_network_matrix.csv',Aaver_c1);

control2=load('CON049_fdt_network_matrix');
control2_waytotal=load('CON049_waytotal');

[mm,nn]=size(control2);
Aaver_c2=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control2(i,j)>UmbralConect
                Aaver_c2(i,j)=control2(i,j)/control2_waytotal(i);
        else
            Aaver_c2(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c2(i,j)=(Aaver_c2(i,j)+Aaver_c2(j,i))/2;
        Aaver_c2(j,i)=Aaver_c2(i,j);
        if i==j
            Aaver_c2(i,j)=1;
        end
    end
end
%csvwrite('control2_fdt_network_matrix.csv',Aaver_c2);

control3=load('CON052_fdt_network_matrix');
control3_waytotal=load('CON052_waytotal');

[mm,nn]=size(control3);
Aaver_c3=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control3(i,j)>UmbralConect
                Aaver_c3(i,j)=control3(i,j)/control3_waytotal(i);
        else
            Aaver_c3(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c3(i,j)=(Aaver_c3(i,j)+Aaver_c3(j,i))/2;
        Aaver_c3(j,i)=Aaver_c3(i,j);
        if i==j
            Aaver_c3(i,j)=1;
        end
    end
end
%csvwrite('control3_fdt_network_matrix.csv',Aaver_c3);

control4=load('CON054_fdt_network_matrix');
control4_waytotal=load('CON054_waytotal');

[mm,nn]=size(control4);
Aaver_c4=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control4(i,j)>UmbralConect
                Aaver_c4(i,j)=control4(i,j)/control4_waytotal(i);
        else
            Aaver_c4(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c4(i,j)=(Aaver_c4(i,j)+Aaver_c4(j,i))/2;
        Aaver_c4(j,i)=Aaver_c4(i,j);
        if i==j
            Aaver_c4(i,j)=1;
        end
    end
end
%csvwrite('control4_fdt_network_matrix.csv',Aaver_c4);

control5=load('CON055_fdt_network_matrix');
control5_waytotal=load('CON055_waytotal');

[mm,nn]=size(control5);
Aaver_c5=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control5(i,j)>UmbralConect
                Aaver_c5(i,j)=control5(i,j)/control5_waytotal(i);
        else
            Aaver_c5(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c5(i,j)=(Aaver_c5(i,j)+Aaver_c5(j,i))/2;
        Aaver_c5(j,i)=Aaver_c5(i,j);
        if i==j
            Aaver_c5(i,j)=1;
        end
    end
end
%csvwrite('control5_fdt_network_matrix.csv',Aaver_c5);

control6=load('CON056_fdt_network_matrix');
control6_waytotal=load('CON056_waytotal');

[mm,nn]=size(control6);
Aaver_c6=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control6(i,j)>UmbralConect
                Aaver_c6(i,j)=control6(i,j)/control6_waytotal(i);
        else
            Aaver_c6(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c6(i,j)=(Aaver_c6(i,j)+Aaver_c6(j,i))/2;
        Aaver_c6(j,i)=Aaver_c6(i,j);
        if i==j
            Aaver_c6(i,j)=1;
        end
    end
end
%csvwrite('control6_fdt_network_matrix.csv',Aaver_c6);

control7=load('CON057_fdt_network_matrix');
control7_waytotal=load('CON057_waytotal');

[mm,nn]=size(control7);
Aaver_c7=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control7(i,j)>UmbralConect
                Aaver_c7(i,j)=control7(i,j)/control7_waytotal(i);
        else
            Aaver_c7(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c7(i,j)=(Aaver_c7(i,j)+Aaver_c7(j,i))/2;
        Aaver_c7(j,i)=Aaver_c7(i,j);
        if i==j
            Aaver_c7(i,j)=1;
        end
    end
end
%csvwrite('control7_fdt_network_matrix.csv',Aaver_c7);

control8=load('CON058_fdt_network_matrix');
control8_waytotal=load('CON058_waytotal');

[mm,nn]=size(control8);
Aaver_c8=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control8(i,j)>UmbralConect
                Aaver_c8(i,j)=control8(i,j)/control8_waytotal(i);
        else
            Aaver_c8(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c8(i,j)=(Aaver_c8(i,j)+Aaver_c8(j,i))/2;
        Aaver_c8(j,i)=Aaver_c8(i,j);
        if i==j
            Aaver_c8(i,j)=1;
        end
    end
end
%csvwrite('control8_fdt_network_matrix.csv',Aaver_c8);

control9=load('CON059_fdt_network_matrix');
control9_waytotal=load('CON059_waytotal');

[mm,nn]=size(control9);
Aaver_c9=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control9(i,j)>UmbralConect
                Aaver_c9(i,j)=control9(i,j)/control9_waytotal(i);
        else
            Aaver_c9(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c9(i,j)=(Aaver_c9(i,j)+Aaver_c9(j,i))/2;
        Aaver_c9(j,i)=Aaver_c9(i,j);
        if i==j
            Aaver_c9(i,j)=1;
        end
    end
end
%csvwrite('control9_fdt_network_matrix.csv',Aaver_c9);

control10=load('AR_F17_CN_108_fdt_network_matrix');
control10_waytotal=load('AR_F17_CN_108_waytotal');

[mm,nn]=size(control10);
Aaver_c10=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control10(i,j)>UmbralConect
                Aaver_c10(i,j)=control10(i,j)/control10_waytotal(i);
        else
            Aaver_c10(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c10(i,j)=(Aaver_c10(i,j)+Aaver_c10(j,i))/2;
        Aaver_c10(j,i)=Aaver_c10(i,j);
        if i==j
            Aaver_c10(i,j)=1;
        end
    end
end
%csvwrite('control10_fdt_network_matrix.csv',Aaver_c10);

control11=load('AR_F17_CN_110_fdt_network_matrix');
control11_waytotal=load('AR_F17_CN_110_waytotal');

[mm,nn]=size(control11);
Aaver_c11=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control11(i,j)>UmbralConect
                Aaver_c11(i,j)=control11(i,j)/control11_waytotal(i);
        else
            Aaver_c11(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c11(i,j)=(Aaver_c11(i,j)+Aaver_c11(j,i))/2;
        Aaver_c11(j,i)=Aaver_c11(i,j);
        if i==j
            Aaver_c11(i,j)=1;
        end
    end
end
%csvwrite('control11_fdt_network_matrix.csv',Aaver_c11);

control12=load('AR_F17_CN_111_fdt_network_matrix');
control12_waytotal=load('AR_F17_CN_111_waytotal');

[mm,nn]=size(control12);
Aaver_c12=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control12(i,j)>UmbralConect
                Aaver_c12(i,j)=control12(i,j)/control12_waytotal(i);
        else
            Aaver_c12(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c12(i,j)=(Aaver_c12(i,j)+Aaver_c12(j,i))/2;
        Aaver_c12(j,i)=Aaver_c12(i,j);
        if i==j
            Aaver_c12(i,j)=1;
        end
    end
end
%csvwrite('control12_fdt_network_matrix.csv',Aaver_c12);

control13=load('AR_F17_CN_112_fdt_network_matrix');
control13_waytotal=load('AR_F17_CN_112_waytotal');

[mm,nn]=size(control13);
Aaver_c13=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control13(i,j)>UmbralConect
                Aaver_c13(i,j)=control13(i,j)/control13_waytotal(i);
        else
            Aaver_c13(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c13(i,j)=(Aaver_c13(i,j)+Aaver_c13(j,i))/2;
        Aaver_c13(j,i)=Aaver_c13(i,j);
        if i==j
            Aaver_c13(i,j)=1;
        end
    end
end
%csvwrite('control13_fdt_network_matrix.csv',Aaver_c13);

control14=load('AR_F17_CN_113_fdt_network_matrix');
control14_waytotal=load('AR_F17_CN_113_waytotal');

[mm,nn]=size(control14);
Aaver_c14=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control14(i,j)>UmbralConect
                Aaver_c14(i,j)=control14(i,j)/control14_waytotal(i);
        else
            Aaver_c14(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c14(i,j)=(Aaver_c14(i,j)+Aaver_c14(j,i))/2;
        Aaver_c14(j,i)=Aaver_c14(i,j);
        if i==j
            Aaver_c14(i,j)=1;
        end
    end
end
%csvwrite('control14_fdt_network_matrix.csv',Aaver_c14);

control15=load('AR_F17_CN_114_fdt_network_matrix');
control15_waytotal=load('AR_F17_CN_114_waytotal');

[mm,nn]=size(control15);
Aaver_c15=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control15(i,j)>UmbralConect
                Aaver_c15(i,j)=control15(i,j)/control15_waytotal(i);
        else
            Aaver_c15(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c15(i,j)=(Aaver_c15(i,j)+Aaver_c15(j,i))/2;
        Aaver_c15(j,i)=Aaver_c15(i,j);
        if i==j
            Aaver_c15(i,j)=1;
        end
    end
end
%csvwrite('control15_fdt_network_matrix.csv',Aaver_c15);

control16=load('AR_F17_CN_115_fdt_network_matrix');
control16_waytotal=load('AR_F17_CN_115_waytotal');

[mm,nn]=size(control16);
Aaver_c16=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control16(i,j)>UmbralConect
                Aaver_c16(i,j)=control16(i,j)/control16_waytotal(i);
        else
            Aaver_c16(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c16(i,j)=(Aaver_c16(i,j)+Aaver_c16(j,i))/2;
        Aaver_c16(j,i)=Aaver_c16(i,j);
        if i==j
            Aaver_c16(i,j)=1;
        end
    end
end
%csvwrite('control16_fdt_network_matrix.csv',Aaver_c16);

control17=load('CH_F17_CN_101_fdt_network_matrix');
control17_waytotal=load('CH_F17_CN_101_waytotal');

[mm,nn]=size(control17);
Aaver_c17=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control17(i,j)>UmbralConect
                Aaver_c17(i,j)=control17(i,j)/control17_waytotal(i);
        else
            Aaver_c17(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c17(i,j)=(Aaver_c17(i,j)+Aaver_c17(j,i))/2;
        Aaver_c17(j,i)=Aaver_c17(i,j);
        if i==j
            Aaver_c17(i,j)=1;
        end
    end
end
%csvwrite('control17_fdt_network_matrix.csv',Aaver_c17);

control18=load('CH_F17_CN_149_fdt_network_matrix');
control18_waytotal=load('CH_F17_CN_149_waytotal');

[mm,nn]=size(control18);
Aaver_c18=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control18(i,j)>UmbralConect
                Aaver_c18(i,j)=control18(i,j)/control18_waytotal(i);
        else
            Aaver_c18(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c18(i,j)=(Aaver_c18(i,j)+Aaver_c18(j,i))/2;
        Aaver_c18(j,i)=Aaver_c18(i,j);
        if i==j
            Aaver_c18(i,j)=1;
        end
    end
end
%csvwrite('control18_fdt_network_matrix.csv',Aaver_c18);

control19=load('CH_F17_CN_148_fdt_network_matrix');
control19_waytotal=load('CH_F17_CN_148_waytotal');

[mm,nn]=size(control19);
Aaver_c19=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control19(i,j)>UmbralConect
                Aaver_c19(i,j)=control19(i,j)/control19_waytotal(i);
        else
            Aaver_c19(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c19(i,j)=(Aaver_c19(i,j)+Aaver_c19(j,i))/2;
        Aaver_c19(j,i)=Aaver_c19(i,j);
        if i==j
            Aaver_c19(i,j)=1;
        end
    end
end
%csvwrite('control19_fdt_network_matrix.csv',Aaver_c19);

control20=load('CH_F17_CN_146_fdt_network_matrix');
control20_waytotal=load('CH_F17_CN_146_waytotal');

[mm,nn]=size(control20);
Aaver_c20=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control20(i,j)>UmbralConect
                Aaver_c20(i,j)=control20(i,j)/control20_waytotal(i);
        else
            Aaver_c20(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c20(i,j)=(Aaver_c20(i,j)+Aaver_c20(j,i))/2;
        Aaver_c20(j,i)=Aaver_c20(i,j);
        if i==j
            Aaver_c20(i,j)=1;
        end
    end
end
%csvwrite('control20_fdt_network_matrix.csv',Aaver_c20);

control21=load('AR_F17_CN_116_fdt_network_matrix');
control21_waytotal=load('AR_F17_CN_116_waytotal');

[mm,nn]=size(control21);
Aaver_c21=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control21(i,j)>UmbralConect
                Aaver_c21(i,j)=control21(i,j)/control21_waytotal(i);
        else
            Aaver_c21(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c21(i,j)=(Aaver_c21(i,j)+Aaver_c21(j,i))/2;
        Aaver_c21(j,i)=Aaver_c21(i,j);
        if i==j
            Aaver_c21(i,j)=1;
        end
    end
end
%csvwrite('control21_fdt_network_matrix.csv',Aaver_c21);

control22=load('AR_F17_CN_117_fdt_network_matrix');
control22_waytotal=load('AR_F17_CN_117_waytotal');

[mm,nn]=size(control22);
Aaver_c22=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control22(i,j)>UmbralConect
                Aaver_c22(i,j)=control22(i,j)/control22_waytotal(i);
        else
            Aaver_c22(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c22(i,j)=(Aaver_c22(i,j)+Aaver_c22(j,i))/2;
        Aaver_c22(j,i)=Aaver_c22(i,j);
        if i==j
            Aaver_c22(i,j)=1;
        end
    end
end
%csvwrite('control22_fdt_network_matrix.csv',Aaver_c22);

control23=load('AR_F17_CN_118_fdt_network_matrix');
control23_waytotal=load('AR_F17_CN_118_waytotal');

[mm,nn]=size(control23);
Aaver_c23=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control23(i,j)>UmbralConect
                Aaver_c23(i,j)=control23(i,j)/control23_waytotal(i);
        else
            Aaver_c23(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c23(i,j)=(Aaver_c23(i,j)+Aaver_c23(j,i))/2;
        Aaver_c23(j,i)=Aaver_c23(i,j);
        if i==j
            Aaver_c23(i,j)=1;
        end
    end
end
%csvwrite('control23_fdt_network_matrix.csv',Aaver_c23);

control24=load('AR_F17_CN_119_fdt_network_matrix');
control24_waytotal=load('AR_F17_CN_119_waytotal');

[mm,nn]=size(control24);
Aaver_c24=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control24(i,j)>UmbralConect
                Aaver_c24(i,j)=control24(i,j)/control24_waytotal(i);
        else
            Aaver_c24(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c24(i,j)=(Aaver_c24(i,j)+Aaver_c24(j,i))/2;
        Aaver_c24(j,i)=Aaver_c24(i,j);
        if i==j
            Aaver_c24(i,j)=1;
        end
    end
end
%csvwrite('control24_fdt_network_matrix.csv',Aaver_c24);

control25=load('AR_F17_CN_120_fdt_network_matrix');
control25_waytotal=load('AR_F17_CN_120_waytotal');

[mm,nn]=size(control25);
Aaver_c25=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control25(i,j)>UmbralConect
                Aaver_c25(i,j)=control25(i,j)/control25_waytotal(i);
        else
            Aaver_c25(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c25(i,j)=(Aaver_c25(i,j)+Aaver_c25(j,i))/2;
        Aaver_c25(j,i)=Aaver_c25(i,j);
        if i==j
            Aaver_c25(i,j)=1;
        end
    end
end
%csvwrite('control25_fdt_network_matrix.csv',Aaver_c25);

control26=load('AR_F17_CN_121_fdt_network_matrix');
control26_waytotal=load('AR_F17_CN_121_waytotal');

[mm,nn]=size(control26);
Aaver_c26=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control26(i,j)>UmbralConect
                Aaver_c26(i,j)=control26(i,j)/control26_waytotal(i);
        else
            Aaver_c26(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c26(i,j)=(Aaver_c26(i,j)+Aaver_c26(j,i))/2;
        Aaver_c26(j,i)=Aaver_c26(i,j);
        if i==j
            Aaver_c26(i,j)=1;
        end
    end
end
%csvwrite('control26_fdt_network_matrix.csv',Aaver_c26);

control27=load('AR_F17_CN_122_fdt_network_matrix');
control27_waytotal=load('AR_F17_CN_122_waytotal');

[mm,nn]=size(control27);
Aaver_c27=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control27(i,j)>UmbralConect
                Aaver_c27(i,j)=control27(i,j)/control27_waytotal(i);
        else
            Aaver_c27(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c27(i,j)=(Aaver_c27(i,j)+Aaver_c27(j,i))/2;
        Aaver_c27(j,i)=Aaver_c27(i,j);
        if i==j
            Aaver_c27(i,j)=1;
        end
    end
end
%csvwrite('control27_fdt_network_matrix.csv',Aaver_c27);

control28=load('CH_F17_CN_116_fdt_network_matrix');
control28_waytotal=load('CH_F17_CN_116_waytotal');

[mm,nn]=size(control28);
Aaver_c28=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control28(i,j)>UmbralConect
                Aaver_c28(i,j)=control28(i,j)/control28_waytotal(i);
        else
            Aaver_c28(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c28(i,j)=(Aaver_c28(i,j)+Aaver_c28(j,i))/2;
        Aaver_c28(j,i)=Aaver_c28(i,j);
        if i==j
            Aaver_c28(i,j)=1;
        end
    end
end
%csvwrite('control28_fdt_network_matrix.csv',Aaver_c28);

control29=load('CH_F17_CN_118_fdt_network_matrix');
control29_waytotal=load('CH_F17_CN_118_waytotal');

[mm,nn]=size(control29);
Aaver_c29=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control29(i,j)>UmbralConect
                Aaver_c29(i,j)=control29(i,j)/control29_waytotal(i);
        else
            Aaver_c29(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c29(i,j)=(Aaver_c29(i,j)+Aaver_c29(j,i))/2;
        Aaver_c29(j,i)=Aaver_c29(i,j);
        if i==j
            Aaver_c29(i,j)=1;
        end
    end
end
%csvwrite('control29_fdt_network_matrix.csv',Aaver_c29);

control30=load('CH_F17_CN_144_fdt_network_matrix');
control30_waytotal=load('CH_F17_CN_144_waytotal');

[mm,nn]=size(control30);
Aaver_c30=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control30(i,j)>UmbralConect
                Aaver_c30(i,j)=control30(i,j)/control30_waytotal(i);
        else
            Aaver_c30(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c30(i,j)=(Aaver_c30(i,j)+Aaver_c30(j,i))/2;
        Aaver_c30(j,i)=Aaver_c30(i,j);
        if i==j
            Aaver_c30(i,j)=1;
        end
    end
end
%csvwrite('control30_fdt_network_matrix.csv',Aaver_c30);

control31=load('CH_F17_CN_145_fdt_network_matrix');
control31_waytotal=load('CH_F17_CN_145_waytotal');

[mm,nn]=size(control31);
Aaver_c31=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control31(i,j)>UmbralConect
                Aaver_c31(i,j)=control31(i,j)/control31_waytotal(i);
        else
            Aaver_c31(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c31(i,j)=(Aaver_c31(i,j)+Aaver_c31(j,i))/2;
        Aaver_c31(j,i)=Aaver_c31(i,j);
        if i==j
            Aaver_c31(i,j)=1;
        end
    end
end
%csvwrite('control31_fdt_network_matrix.csv',Aaver_c31);

control32=load('AR_F17_CN_123_fdt_network_matrix');
control32_waytotal=load('AR_F17_CN_123_waytotal');

[mm,nn]=size(control32);
Aaver_c32=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control32(i,j)>UmbralConect
                Aaver_c32(i,j)=control32(i,j)/control32_waytotal(i);
        else
            Aaver_c32(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c32(i,j)=(Aaver_c32(i,j)+Aaver_c32(j,i))/2;
        Aaver_c32(j,i)=Aaver_c32(i,j);
        if i==j
            Aaver_c32(i,j)=1;
        end
    end
end
%csvwrite('control32_fdt_network_matrix.csv',Aaver_c32);

control33=load('AR_F17_CN_125_fdt_network_matrix');
control33_waytotal=load('AR_F17_CN_125_waytotal');

[mm,nn]=size(control33);
Aaver_c33=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control33(i,j)>UmbralConect
                Aaver_c33(i,j)=control33(i,j)/control33_waytotal(i);
        else
            Aaver_c33(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c33(i,j)=(Aaver_c33(i,j)+Aaver_c33(j,i))/2;
        Aaver_c33(j,i)=Aaver_c33(i,j);
        if i==j
            Aaver_c33(i,j)=1;
        end
    end
end
%csvwrite('control33_fdt_network_matrix.csv',Aaver_c33);

control34=load('CH_F17_CN_119_fdt_network_matrix');
control34_waytotal=load('CH_F17_CN_119_waytotal');

[mm,nn]=size(control34);
Aaver_c34=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control34(i,j)>UmbralConect
                Aaver_c34(i,j)=control34(i,j)/control34_waytotal(i);
        else
            Aaver_c34(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c34(i,j)=(Aaver_c34(i,j)+Aaver_c34(j,i))/2;
        Aaver_c34(j,i)=Aaver_c34(i,j);
        if i==j
            Aaver_c34(i,j)=1;
        end
    end
end
%csvwrite('control34_fdt_network_matrix.csv',Aaver_c34);

control35=load('CH_F17_CN_121_fdt_network_matrix');
control35_waytotal=load('CH_F17_CN_121_waytotal');

[mm,nn]=size(control35);
Aaver_c35=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control35(i,j)>UmbralConect
                Aaver_c35(i,j)=control35(i,j)/control35_waytotal(i);
        else
            Aaver_c35(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c35(i,j)=(Aaver_c35(i,j)+Aaver_c35(j,i))/2;
        Aaver_c35(j,i)=Aaver_c35(i,j);
        if i==j
            Aaver_c35(i,j)=1;
        end
    end
end
%csvwrite('control35_fdt_network_matrix.csv',Aaver_c35);

control36=load('CH_F17_CN_122_fdt_network_matrix');
control36_waytotal=load('CH_F17_CN_122_waytotal');

[mm,nn]=size(control36);
Aaver_c36=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control36(i,j)>UmbralConect
                Aaver_c36(i,j)=control36(i,j)/control36_waytotal(i);
        else
            Aaver_c36(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c36(i,j)=(Aaver_c36(i,j)+Aaver_c36(j,i))/2;
        Aaver_c36(j,i)=Aaver_c36(i,j);
        if i==j
            Aaver_c36(i,j)=1;
        end
    end
end
%csvwrite('control36_fdt_network_matrix.csv',Aaver_c36);

control37=load('CH_F17_CN_126_fdt_network_matrix');
control37_waytotal=load('CH_F17_CN_126_waytotal');

[mm,nn]=size(control37);
Aaver_c37=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control37(i,j)>UmbralConect
                Aaver_c37(i,j)=control37(i,j)/control37_waytotal(i);
        else
            Aaver_c37(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c37(i,j)=(Aaver_c37(i,j)+Aaver_c37(j,i))/2;
        Aaver_c37(j,i)=Aaver_c37(i,j);
        if i==j
            Aaver_c37(i,j)=1;
        end
    end
end
%csvwrite('control37_fdt_network_matrix.csv',Aaver_c37);

control38=load('CH_F17_CN_143_fdt_network_matrix');
control38_waytotal=load('CH_F17_CN_143_waytotal');

[mm,nn]=size(control38);
Aaver_c38=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control38(i,j)>UmbralConect
                Aaver_c38(i,j)=control38(i,j)/control38_waytotal(i);
        else
            Aaver_c38(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c38(i,j)=(Aaver_c38(i,j)+Aaver_c38(j,i))/2;
        Aaver_c38(j,i)=Aaver_c38(i,j);
        if i==j
            Aaver_c38(i,j)=1;
        end
    end
end
%csvwrite('control38_fdt_network_matrix.csv',Aaver_c38);


control39=load('CH_F17_CN_141_fdt_network_matrix');
control39_waytotal=load('CH_F17_CN_141_waytotal');

[mm,nn]=size(control39);
Aaver_c39=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control39(i,j)>UmbralConect
                Aaver_c39(i,j)=control39(i,j)/control39_waytotal(i);
        else
            Aaver_c39(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c39(i,j)=(Aaver_c39(i,j)+Aaver_c39(j,i))/2;
        Aaver_c39(j,i)=Aaver_c39(i,j);
        if i==j
            Aaver_c39(i,j)=1;
        end
    end
end
%csvwrite('control39_fdt_network_matrix.csv',Aaver_c39);

control40=load('AR_F17_CN_126_fdt_network_matrix');
control40_waytotal=load('AR_F17_CN_126_waytotal');

[mm,nn]=size(control40);
Aaver_c40=zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if control40(i,j)>UmbralConect
                Aaver_c40(i,j)=control40(i,j)/control40_waytotal(i);
        else
            Aaver_c40(i,j)=0;            
        end
    end
end
for i=1:mm
    for j=i:nn
        Aaver_c40(i,j)=(Aaver_c40(i,j)+Aaver_c40(j,i))/2;
        Aaver_c40(j,i)=Aaver_c40(i,j);
        if i==j
            Aaver_c40(i,j)=1;
        end
    end
end

Diferencia=zeros(mm,nn); %Matriz que almacenará los p-valores resultantes del Crawford-Howell test

%Realiza el Crawford-Howell test entre el elemento i,j de la matriz de
%conectividad del paciente y los elementos i,j de las matrices de control
for i=1:mm
    for j=1:nn
        control_vec=[Aaver_c1(i,j) Aaver_c2(i,j) Aaver_c3(i,j) Aaver_c4(i,j) Aaver_c5(i,j) Aaver_c6(i,j) Aaver_c7(i,j) Aaver_c8(i,j) Aaver_c9(i,j) Aaver_c10(i,j) Aaver_c11(i,j) Aaver_c12(i,j) Aaver_c13(i,j) Aaver_c14(i,j) Aaver_c15(i,j) Aaver_c16(i,j) Aaver_c17(i,j) Aaver_c18(i,j) Aaver_c19(i,j) Aaver_c20(i,j) Aaver_c21(i,j) Aaver_c22(i,j) Aaver_c23(i,j) Aaver_c24(i,j) Aaver_c25(i,j) Aaver_c26(i,j) Aaver_c27(i,j) Aaver_c28(i,j) Aaver_c29(i,j) Aaver_c30(i,j) Aaver_c31(i,j) Aaver_c32(i,j) Aaver_c33(i,j) Aaver_c34(i,j) Aaver_c35(i,j) Aaver_c36(i,j) Aaver_c37(i,j) Aaver_c38(i,j) Aaver_c39(i,j) Aaver_c40(i,j)];
        Diferencia(i,j)=CrawfordHowell(Aaver(i,j),control_vec);
    end
end
csvwrite('diferencia_14',Diferencia); %cambiar según el paciente

figure
imagesc(Diferencia); %grafica la matriz que contiene los p-valores
colorbar
set(gca,'ColorScale','log');%escala de colores logarítmica 
title('Structural contrast matrix')

%Imprimir valores menores a un p=0.05
cont = 0
for i=1:120
    for j=1:120
        if Diferencia(i,j) < 0.11
            fprintf("p menor a 0.11 en %i,%i \n",i,j);
            %cont = cont+1
        end
    end
end

%definición de la función que permite realizar el test Crawford-Howell
function[pval]=CrawfordHowell(paciente,control)
    longitud=length(control);
    tval=(paciente-mean(control))./(std(control).*sqrt((longitud+1)./longitud));
    degfre=longitud-1;
    pval=2*(1-tcdf(abs(tval),degfre));
end