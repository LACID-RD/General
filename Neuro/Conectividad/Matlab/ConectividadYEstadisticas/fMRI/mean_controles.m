load('norm_workspace_1a70.mat');
%Cargar la matriz de conectividad del paciente (cambiar al final también la
%matriz diferencia del paciente y el número en el archivo a guardar):
matriz_pac = load('Lopez_conn.csv');
%matriz_pac=pac09conn;

%Normalizo matriz paciente:
[mm,nn] = size(matriz_pac);
for i=1:mm
    for j=1:nn
        if i==j
            matriz_pac(i,j) = 0;
        end
    end
end

%Media de las matrices de conectividad de los controles:
mean_matrix = zeros(mm,nn);
controles_vector = zeros(1,mm);

for i=1:mm
    for j=1:nn
        controles_vector = [control1_norm(i,j) control2_norm(i,j) control3_norm(i,j) control4_norm(i,j) control5_norm(i,j) control6_norm(i,j) control7_norm(i,j) control8_norm(i,j) control9_norm(i,j) control10_norm(i,j) control11_norm(i,j) control12_norm(i,j) control13_norm(i,j) control14_norm(i,j) control15_norm(i,j) control16_norm(i,j) control17_norm(i,j) control18_norm(i,j) control19_norm(i,j) control20_norm(i,j) control21_norm(i,j) control22_norm(i,j) control23_norm(i,j) control24_norm(i,j) control25_norm(i,j) control26_norm(i,j) control27_norm(i,j) control28_norm(i,j) control29_norm(i,j) control30_norm(i,j) control31_norm(i,j) control32_norm(i,j) control33_norm(i,j) control34_norm(i,j) control35_norm(i,j) control36_norm(i,j) control37_norm(i,j) control38_norm(i,j) control39_norm(i,j) control40_norm(i,j) control41_norm(i,j) control42_norm(i,j) control43_norm(i,j) control44_norm(i,j) control45_norm(i,j) control46_norm(i,j) control47_norm(i,j) control48_norm(i,j) control49_norm(i,j) control50_norm(i,j) control51_norm(i,j) control52_norm(i,j) control53_norm(i,j) control54_norm(i,j) control55_norm(i,j) control56_norm(i,j) control57_norm(i,j) control58_norm(i,j) control59_norm(i,j) control60_norm(i,j) control61_norm(i,j) control62_norm(i,j) control63_norm(i,j) control64_norm(i,j) control65_norm(i,j) control66_norm(i,j) control67_norm(i,j) control68_norm(i,j) control69_norm(i,j) control70_norm(i,j)];
        mean_matrix(i,j) = mean(controles_vector);
    end
end

%Comparación entre la conectividad del paciente y la media de los controles
%para ver si es mayor o menor:

matriz_comparacion = zeros(mm,nn);
for i=1:mm
    for j=1:nn
        if matriz_pac(i,j) > mean_matrix(i,j)
            matriz_comparacion(i,j) = 1;
        elseif matriz_pac(i,j) == mean_matrix(i,j)
            matriz_comparacion(i,j) = 0;
        else
            matriz_comparacion(i,j) = -1;
        end
    end
end

%figure
%imagesc(matriz_comparacion);
%colorbar
%title('Matriz comparación de mayor o menor: 1 es mayor la conectividad del paciente; 0 es menor o igual la conectividad del paciente.');


%Multiplicación de signo con la matriz diferencia:

%Cargo matriz diferencia del paciente:
matriz_diferencia = load('Diferencia_14');
matriz_diferencia_signo = zeros(mm,nn);
for i=1:mm
    for j=1:nn
        matriz_diferencia_signo(i,j) = matriz_comparacion(i,j) * matriz_diferencia(i,j);
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%ORDENO LA MATRIZ DIFERENCIA SIGNO PARA LLEVARLA AL ESPACIO DE LA TRACTO%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

a=120;
VectorComun=zeros(1,a);
MatrizOrdenada=zeros(a,a); %donde almacenamos la matriz ordenada de la funcional

for i=1:a
    for j=1:a
        MatrizOrdenada(i,j) = 10000;
    end
end

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
        MatrizOrdenada(i,j)=matriz_diferencia_signo(VectorComun(i),VectorComun(j));
    end
end

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
        if matriz_diferencia_signo(VectorComun(i),VectorComun(j))<MatrizOrdenada(i,j)
            MatrizOrdenada(i,j)=matriz_diferencia_signo(VectorComun(i),VectorComun(j));
        end
    end
end

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
        if matriz_diferencia_signo(VectorComun(i),VectorComun(j))<MatrizOrdenada(i,j)
            MatrizOrdenada(i,j)=matriz_diferencia_signo(VectorComun(i),VectorComun(j));
        end
    end
end

VectorComun(43)=105;
VectorComun(44)=104;
VectorComun(59)=75;
VectorComun(60)=74;

for i=1:a
    for j=1:a
        if matriz_diferencia_signo(VectorComun(i),VectorComun(j))<MatrizOrdenada(i,j)
            MatrizOrdenada(i,j)=matriz_diferencia_signo(VectorComun(i),VectorComun(j));
        end
    end
end

matriz_funcion = zeros(120,120);
for i=1:120
    for j=1:120
        matriz_funcion(i,j)=1/(MatrizOrdenada(i,j));
    end
end

csvwrite('ordenada_signo_funcion_14_F',matriz_funcion);

%figure
%imagesc(matriz_funcion);
%colorbar
%set(gca,'ColorScale','log') %escala de colores logarítmica 
%title('Matriz diferencia que contempla el signo de la diferencia con los controles y que tiene aplicada la función 1/x');

% for i=1:120
%     for j=1:120
%         if matriz_funcion(i,j)>20 
%             fprintf('Dio mayor que 20 en %i,%i \n',i,j);
%         elseif matriz_funcion(i,j)<-20
%             fprintf('Dio menor que -20 en %i,%i \n',i,j);
%         end
%     end
% end



%figure
%imagesc(matriz_diferencia_signo);
%colorbar
%set(gca,'ColorScale','log') %escala de colores logarítmica 
%title('Matriz diferencia que contempla el signo de la diferencia con los controles');