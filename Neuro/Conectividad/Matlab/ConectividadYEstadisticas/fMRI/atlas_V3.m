diferencia_funcional = load('Diferencia_14');
load('diferencia_metricas_14.mat');
%load('tracto_04');

a=120;
VectorComun=zeros(1,a);
MatrizComun=zeros(a,a);
BC_comun=zeros(1,a);
clustercoef_comun=zeros(1,a);
deg_comun=zeros(1,a);
distancematrix_comun=zeros(a,a);
edgesdistance_comun=zeros(a,a);
localeff_comun=zeros(1,a);
str_comun=zeros(1,a);


for i=1:a
    for j=1:a
        MatrizComun(i,j) = 10000;
        BC_comun(i)=10000;
        clustercoef_comun(i)=10000;
        deg_comun(i)=10000;
        distancematrix_comun(i,j)=10000;
        edgesdistance_comun(i,j)=10000;
        localeff_comun(i)=10000;
        str_comun(i)=10000;
    end
end
%MatrizMean=zeros(a,a);

VectorComun(1)=14;
VectorComun(2)=13;
VectorComun(3)=6;
VectorComun(4)=5;
VectorComun(5)=8;
VectorComun(6)=7;
VectorComun(7)=12;
VectorComun(8)=11;
VectorComun(9)=10;
VectorComun(10)=9;
VectorComun(11)=10;
VectorComun(12)=9;
VectorComun(13)=77;%79 Y 81
VectorComun(14)=76;%78 Y 80
VectorComun(15)=51;
VectorComun(16)=50;
VectorComun(17)=2;
VectorComun(18)=1;
VectorComun(19)=49;
VectorComun(20)=49;
VectorComun(21)=61;
VectorComun(22)=60;
VectorComun(23)=61;
VectorComun(24)=60;
VectorComun(25)=61;
VectorComun(26)=60;
VectorComun(27)=61;
VectorComun(28)=60;
VectorComun(29)=61;
VectorComun(30)=60;
VectorComun(31)=61;
VectorComun(32)=60;
VectorComun(33)=4;
VectorComun(34)=3;
VectorComun(35)=54;%55
VectorComun(36)=53;%55
VectorComun(37)=54;
VectorComun(38)=53;
VectorComun(39)=56;
VectorComun(40)=56;
VectorComun(41)=101;%106
VectorComun(42)=100;%106
VectorComun(43)=63;%65, 52, 105
VectorComun(44)=62;%64, 52, 104
VectorComun(45)=103;
VectorComun(46)=102;
VectorComun(47)=48;%89
VectorComun(48)=47;%88
VectorComun(49)=59;
VectorComun(50)=58;
VectorComun(51)=67;
VectorComun(52)=66;
VectorComun(53)=44;
VectorComun(54)=43;
VectorComun(55)=44;
VectorComun(56)=43;
VectorComun(57)=46;%91
VectorComun(58)=45;%90
VectorComun(59)=69;%71, 73, 75
VectorComun(60)=68;%70, 72, 74
VectorComun(61)=34;
VectorComun(62)=33;
VectorComun(63)=36;
VectorComun(64)=35;
VectorComun(65)=36;
VectorComun(66)=35;
VectorComun(67)=38;% 40
VectorComun(68)=37;% 39
VectorComun(69)=42;
VectorComun(70)=41;
VectorComun(71)=57;
VectorComun(72)=57;
VectorComun(73)=57;
VectorComun(74)=57;
VectorComun(75)=95;
VectorComun(76)=94;
VectorComun(77)=97;
VectorComun(78)=96;
VectorComun(79)=99;
VectorComun(80)=98;
VectorComun(81)=93;
VectorComun(82)=92;
VectorComun(83)=85;%83
VectorComun(84)=84;%82
VectorComun(85)=18;% 20, 87
VectorComun(86)=17;%19, 86
VectorComun(87)=16;
VectorComun(88)=15;
VectorComun(89)=22;%24 Y 26
VectorComun(90)=21;%23 Y 25
VectorComun(91)=16;
VectorComun(92)=15;
VectorComun(93)=28;%30 Y 32
VectorComun(94)=27;% 29 Y 31
VectorComun(95)=107;
VectorComun(96)=108;
VectorComun(97)=109;
VectorComun(98)=110;
VectorComun(99)=111;
VectorComun(100)=112;
VectorComun(101)=113;
VectorComun(102)=114;
VectorComun(103)=115;
VectorComun(104)=116;
VectorComun(105)=117;
VectorComun(106)=118;
VectorComun(107)=119;
VectorComun(108)=120;
VectorComun(109)=121;
VectorComun(110)=122;
VectorComun(111)=123;
VectorComun(112)=124;
VectorComun(113)=125;
VectorComun(114)=126;
VectorComun(115)=127;
VectorComun(116)=128;
VectorComun(117)=129;
VectorComun(118)=130;
VectorComun(119)=131;
VectorComun(120)=132;

for i=1:120
    for j=1:120
        MatrizComun(i,j)=diferencia_funcional(VectorComun(i),VectorComun(j));
        distancematrix_comun(i,j)=diferencia_distancematrix(VectorComun(i),VectorComun(j));
        edgesdistance_comun(i,j)=diferencia_edgesdistance(VectorComun(i),VectorComun(j));
    end
end
for i=1:120
    BC_comun(i)=diferencia_BC(VectorComun(i));
    clustercoef_comun(i)=diferencia_clustercoef(VectorComun(i));
    deg_comun(i)=diferencia_deg(VectorComun(i));
    localeff_comun(i)=diferencia_localeff(VectorComun(i));
    str_comun(i)=diferencia_str(VectorComun(i));
end
% figure
% imagesc(MatrizComun); %grafica la matriz que contiene los p-valores
% colorbar
% set(gca,'ColorScale','log'); %escala de colores logar�tmica
% title('Functional contrast matrix');

VectorComun(13)=79;%81
VectorComun(14)=78;% 80
VectorComun(35)=55;
VectorComun(36)=55;
VectorComun(41)=106;
VectorComun(42)=106;
VectorComun(43)=65;%52, 105
VectorComun(44)=64;%52, 104
VectorComun(47)=89;
VectorComun(48)=88;
VectorComun(57)=91;
VectorComun(58)=90;
VectorComun(59)=71;% 73, 75
VectorComun(60)=70;% 72, 74
VectorComun(67)=40;
VectorComun(68)=39;
VectorComun(83)=83;
VectorComun(84)=82;
VectorComun(85)=20;% 87
VectorComun(86)=19;% 86
VectorComun(89)=24;% 26
VectorComun(90)=23;% 25
VectorComun(93)=30;% 32
VectorComun(94)=29;% 31

for i=1:120
    for j=1:120
        if diferencia_funcional(VectorComun(i),VectorComun(j))<MatrizComun(i,j)
            MatrizComun(i,j)=diferencia_funcional(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_distancematrix(VectorComun(i),VectorComun(j))<distancematrix_comun(i,j)
            distancematrix_comun(i,j)=diferencia_distancematrix(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_edgesdistance(VectorComun(i),VectorComun(j))<edgesdistance_comun(i,j)
            edgesdistance_comun(i,j)=diferencia_edgesdistance(VectorComun(i),VectorComun(j));
        end
    end
end
            

for i=1:a
    if diferencia_BC(VectorComun(i)) < BC_comun(i)
        BC_comun(i)=diferencia_BC(VectorComun(i));
    end
end

for i=1:a
    if diferencia_clustercoef(VectorComun(i)) < clustercoef_comun(i)
        clustercoef_comun(i)=diferencia_clustercoef(VectorComun(i));
    end
end

for i=1:a
    if diferencia_deg(VectorComun(i)) < deg_comun(i)
        deg_comun(i)=diferencia_deg(VectorComun(i));
    end
end

for i=1:a
    if diferencia_localeff(VectorComun(i)) < localeff_comun(i)
        localeff_comun(i)=diferencia_localeff(VectorComun(i));
    end
end
    
for i=1:a
    if diferencia_str(VectorComun(i)) < str_comun(i)
        str_comun(i)=diferencia_str(VectorComun(i));
    end
end
    
%figure
%imagesc(MatrizComun); %grafica la matriz que contiene los p-valores
%colorbar
%set(gca,'ColorScale','log'); %escala de colores logar�tmica
%title('DFV');

VectorComun(13)=81;
VectorComun(14)=80;
VectorComun(43)=52;%105
VectorComun(44)=52;% 104
VectorComun(59)=73;%  75
VectorComun(60)=72;% 74
VectorComun(85)=87;
VectorComun(86)=86;
VectorComun(89)=26;
VectorComun(90)=25;
VectorComun(93)=32;
VectorComun(94)=31;

for i=1:120
    for j=1:120
        if diferencia_funcional(VectorComun(i),VectorComun(j))<MatrizComun(i,j)
            MatrizComun(i,j)=diferencia_funcional(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_distancematrix(VectorComun(i),VectorComun(j))<distancematrix_comun(i,j)
            distancematrix_comun(i,j)=diferencia_distancematrix(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_edgesdistance(VectorComun(i),VectorComun(j))<edgesdistance_comun(i,j)
            edgesdistance_comun(i,j)=diferencia_edgesdistance(VectorComun(i),VectorComun(j));
        end
    end
end
            

for i=1:a
    if diferencia_BC(VectorComun(i)) < BC_comun(i)
        BC_comun(i)=diferencia_BC(VectorComun(i));
    end
end

for i=1:a
    if diferencia_clustercoef(VectorComun(i)) < clustercoef_comun(i)
        clustercoef_comun(i)=diferencia_clustercoef(VectorComun(i));
    end
end

for i=1:a
    if diferencia_deg(VectorComun(i)) < deg_comun(i)
        deg_comun(i)=diferencia_deg(VectorComun(i));
    end
end

for i=1:a
    if diferencia_localeff(VectorComun(i)) < localeff_comun(i)
        localeff_comun(i)=diferencia_localeff(VectorComun(i));
    end
end
    
for i=1:a
    if diferencia_str(VectorComun(i)) < str_comun(i)
        str_comun(i)=diferencia_str(VectorComun(i));
    end
end
%figure
%imagesc(MatrizComun); %grafica la matriz que contiene los p-valores
%colorbar
%set(gca,'ColorScale','log'); %escala de colores logar�tmica
%title('DFV');

VectorComun(43)=105;
VectorComun(44)=104;
VectorComun(59)=75;
VectorComun(60)=74;

for i=1:120
    for j=1:120
        if diferencia_funcional(VectorComun(i),VectorComun(j))<MatrizComun(i,j)
            MatrizComun(i,j)=diferencia_funcional(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_distancematrix(VectorComun(i),VectorComun(j))<distancematrix_comun(i,j)
            distancematrix_comun(i,j)=diferencia_distancematrix(VectorComun(i),VectorComun(j));
        end
    end
end

for i=1:120
    for j=1:120
        if diferencia_edgesdistance(VectorComun(i),VectorComun(j))<edgesdistance_comun(i,j)
            edgesdistance_comun(i,j)=diferencia_edgesdistance(VectorComun(i),VectorComun(j));
        end
    end
end
            

for i=1:a
    if diferencia_BC(VectorComun(i)) < BC_comun(i)
        BC_comun(i)=diferencia_BC(VectorComun(i));
    end
end

for i=1:a
    if diferencia_clustercoef(VectorComun(i)) < clustercoef_comun(i)
        clustercoef_comun(i)=diferencia_clustercoef(VectorComun(i));
    end
end

for i=1:a
    if diferencia_deg(VectorComun(i)) < deg_comun(i)
        deg_comun(i)=diferencia_deg(VectorComun(i));
    end
end

for i=1:a
    if diferencia_localeff(VectorComun(i)) < localeff_comun(i)
        localeff_comun(i)=diferencia_localeff(VectorComun(i));
    end
end
    
for i=1:a
    if diferencia_str(VectorComun(i)) < str_comun(i)
        str_comun(i)=diferencia_str(VectorComun(i));
    end
end

csvwrite('Funcional_ordenada_14', MatrizComun);
csvwrite('BC_ordenada_14',BC_comun);
csvwrite('clustercoef_ordenada_14',clustercoef_comun);
csvwrite('deg_ordenada_14',deg_comun);
csvwrite('distancematrix_ordenada_14',distancematrix_comun);
csvwrite('edgesdistance_ordenada_14',edgesdistance_comun);
csvwrite('localeff_ordenada_14',localeff_comun);
csvwrite('str_ordenada_14',str_comun);

figure
imagesc(MatrizComun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Functional contrast matrix');

figure
imagesc(BC_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('BC ordenada');

figure
imagesc(clustercoef_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Cluster coefficient ordenada');

figure
imagesc(deg_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Degree ordenada');

figure
imagesc(distancematrix_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Distance matrix ordenada');

figure
imagesc(edgesdistance_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Edges distance (contrast)');

figure
imagesc(localeff_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Local efficiency (contrast)');

figure
imagesc(str_comun); 
colorbar
set(gca,'ColorScale','log'); %escala de colores logarítmica
title('Str ordenada');

%Control para ver si quedó algún valor grande por error:
for i=1:120
    for j=1:120
        if MatrizComun(i,j) == 10000
            fprintf('Error: Quedó un valor 10000 en %i, %i \n', i, j);
        end
    end
end

%Thresholds:

% Matriz_threshold = zeros(a,a);
% for i=1:a
%     for j=1:a
%         if MatrizComun(i,j) < 0.05
%             Matriz_threshold(i,j)=1;
%         else
%             Matriz_threshold(i,j)=0;
%         end
%     end
% end
% 
% figure
% imagesc(Matriz_threshold); 
% colorbar
% set(gca,'ColorScale','log'); %escala de colores logarítmica
% title('Conectividad funcional ordenada con threshold en p<0.05');
% 
% distancematrix_thr = zeros(a,a);
% for i=1:a
%     for j=1:a
%         if distancematrix_comun(i,j) < 0.05
%             distancematrix_thr(i,j)=1;
%         else
%             distancematrix_thr(i,j)=0;
%         end
%     end
% end
% 
% figure
% imagesc(distancematrix_thr); 
% colorbar
% set(gca,'ColorScale','log'); %escala de colores logarítmica
% title('Distance matrix ordenada con threshold en p<0.05');
% 
% edgesdistance_thr = zeros(a,a);
% for i=1:a
%     for j=1:a
%         if edgesdistance_comun(i,j) < 0.05
%             edgesdistance_thr(i,j)=1;
%         else
%             edgesdistance_thr(i,j)=0;
%         end
%     end
% end
% 
% figure
% imagesc(edgesdistance_thr); 
% colorbar
% set(gca,'ColorScale','log'); %escala de colores logarítmica
% title('Edges distance ordenada con threshold en p<0.05');
% 
% BC_threshold=zeros(1,a);
% for i=1:a
%     if BC_comun(i) < 0.05
%         BC_threshold(i) = 1;
%         fprintf('BC - pvalor < 0.05 en: %i \n', i);
%     else
%         BC_threshold(i) = 0;
%     end
% end
% 
% %figure
% %imagesc(BC_threshold); 
% %colorbar
% %set(gca,'ColorScale','log'); %escala de colores logarítmica
% %title('BC ordenada con threshold en p<0.05, paciente 01');
% 
% clustercoef_threshold=zeros(1,a);
% for i=1:a
%     if clustercoef_comun(i) < 0.05
%         clustercoef_threshold(i) = 1;
%         fprintf('Cluster coefficient - pvalor < 0.05 en: %i \n', i);
%     else
%         clustercoef_threshold(i) = 0;
%     end
% end
% 
% deg_threshold=zeros(1,a);
% for i=1:a
%     if deg_comun(i) < 0.05
%         deg_threshold(i) = 1;
%         fprintf('Degree - pvalor < 0.05 en: %i \n', i);
%     else
%         deg_threshold(i) = 0;
%     end
% end
% 
% localeff_threshold=zeros(1,a);
% for i=1:a
%     if localeff_comun(i) < 0.05
%         localeff_threshold(i) = 1;
%         fprintf('Local efficiency - pvalor < 0.05 en: %i \n', i);
%     else
%         localeff_threshold(i) = 0;
%     end
% end
% 
% str_threshold=zeros(1,a);
% for i=1:a
%     if str_comun(i) < 0.05
%         str_threshold(i) = 1;
%         fprintf('Str - pvalor < 0.05 en: %i \n', i);
%     else
%         str_threshold(i) = 0;
%     end
% end
