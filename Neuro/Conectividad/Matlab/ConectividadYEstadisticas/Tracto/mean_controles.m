UmbralConect=0;%Para evitar falsos positivos
%Cargar matrices de controles
load('Aaver_controles.mat');

%Cargar matriz de conectividad del paciente y normalizarla (Fijarse también
%de cambiar en los últimos pasos el nombre al momento de cargar la matriz
%diferencia y al guardar el archivo final
A = load('Lopez_fdt_network_matrix');
Waytotal = load('Lopez_waytotal');

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
matriz_pac = Aaver;


%Media de las matrices de conectividad de los controles:
mean_matrix = zeros (mm,nn);
controles_vector = zeros (1,mm);
for i = 1:mm
    for j = 1:nn
        controles_vector = [Aaver_c1(i,j) Aaver_c2(i,j) Aaver_c3(i,j) Aaver_c4(i,j) Aaver_c5(i,j) Aaver_c6(i,j) Aaver_c7(i,j) Aaver_c8(i,j) Aaver_c9(i,j) Aaver_c10(i,j) Aaver_c11(i,j) Aaver_c12(i,j) Aaver_c13(i,j) Aaver_c14(i,j) Aaver_c15(i,j) Aaver_c16(i,j) Aaver_c17(i,j) Aaver_c18(i,j) Aaver_c19(i,j) Aaver_c20(i,j) Aaver_c21(i,j) Aaver_c22(i,j) Aaver_c23(i,j) Aaver_c24(i,j) Aaver_c25(i,j) Aaver_c26(i,j) Aaver_c27(i,j) Aaver_c28(i,j) Aaver_c29(i,j) Aaver_c30(i,j) Aaver_c31(i,j) Aaver_c32(i,j) Aaver_c33(i,j) Aaver_c34(i,j) Aaver_c35(i,j) Aaver_c36(i,j) Aaver_c37(i,j) Aaver_c38(i,j) Aaver_c39(i,j) Aaver_c40(i,j)];
        mean_matrix(i,j)= mean(controles_vector);
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

%Multiplicación de signo con la matriz diferencia:

%Cargo matriz diferencia del paciente:
matriz_diferencia = load('diferencia_14');
matriz_diferencia_signo = zeros(mm,nn);
for i=1:mm
    for j=1:nn
        matriz_diferencia_signo(i,j) = matriz_comparacion(i,j) * matriz_diferencia(i,j);
    end
end

%Aplico la función 1/x a cada p-valor de la matriz con signo, 
%para darle mayor peso a los valores cercanos a cero, pero manteniendo 
%el signo para saber si la diferencia es positiva o negativa

% matriz_funcion = zeros(mm,nn);
% for i=1:mm
%     for j=1:nn
%         matriz_funcion(i,j)=1/(matriz_diferencia_signo(i,j));
%     end
% end

csvwrite('diferencia_signo_14_T', matriz_diferencia_signo);

% figure
% imagesc(matriz_funcion);
% colorbar
% set(gca,'ColorScale','log') %escala de colores logarítmica 
% title('Matriz diferencia que contempla el signo de la diferencia con los controles y que tiene aplicada la función 1/x');

% for i=1:mm
%     for j=1:nn
%         if matriz_funcion(i,j)>20 
%             fprintf('Dio mayor que 20 en %i,%i \n',i,j);
%         elseif matriz_funcion(i,j)<-20
%             fprintf('Dio menor que -20 en %i,%i \n',i,j);
%         end
%     end
% end

%%%IMPORTO LA MATRIZ ORDENADA DE LA FUNCIONAL CON SIGNO CON LA FUNCIÓN
%%%APLICADA PARA COMPARAR

%mat_funcional=load('Matriz_ordenada_signo_función_aplicada_pac03(funcional)');

% mat_suma = zeros(120,120);
% 
% for i=1:120
%     for j=1:120
%         mat_suma(i,j) = matriz_funcion(i,j)+ mat_funcional(i,j);
%     end
% end
% 
% figure
% imagesc(mat_suma);
% colorbar
% set(gca,'ColorScale','log') %escala de colores logarítmica 
% title('Total contrast matrix');
% 
% for i=1:120
%      for j=1:120
%          if mat_suma(i,j)> 10^14
%              fprintf('Suma dio mayor que 200 en %i,%i \n',i,j);
%          elseif mat_suma(i,j)<-10^14
%              fprintf('Suma dio menor que -200 en %i,%i \n',i,j);
%          end
%      end
% end

%MAX_matsuma=max(mat_suma);
%fprintf('El máximo valor en la matriz es %i\n',MAX_matsuma);

% figure
% imagesc(mat_suma);
% colorbar
% set(gca,'ColorScale','log') %escala de colores logarítmica 
%title('Matriz diferencia que contempla el signo de la diferencia con los controles');
