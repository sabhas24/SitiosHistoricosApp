clear all
clc
D=load('P2_datos.txt');%cotiene los datos de la corriente
t=D(:,1);%tiempo
i=D(:,2); %corriente  f(tk)
n=length(t);
L=4;%inductancia

ftprim=zeros(n,1);
Vl=zeros(n,1);
h=0.05;
for k=1:n
   if k <= n-2
    ftprim(k)= (-3*i(k)+4*i(k+1)-i(k+2))/(2*h); %adelantada
     elseif k >= n-1
      ftprim(k)=(3*i(k)-4*i(k-1)+i(k-2))/(2*h);%atrasada
  end

Vl(k)= L*ftprim(k); %guardo la dif de pontecial en cada unst de tiempo
end
figure(1)
plot(t,Vl,'-b')
xlabel('tiempo tk [s]')
ylabel(' Vl(tk)')
title('Caida de tesnion vs t')
grid on

iL(1)=0 %primer valor de la corriente  aproximada
for k=2:n
    Int= (h*0.5)*(Vl(k-1)+Vl(k) ); %trapecio simple
    iL(k) =i(k-1) + (-1/L)*Int;
end
iL=iL';
display(iL)
Eabs=abs(i-iL)

Erel= Eabs/abs(i);

figure(2)
plot(t,Eabs,'ob')
xlabel('t')
ylabel('Eabs')
title('Error absoluto tiempo a tiempo')
grid on

figure(3)
plot(t,Erel,'or')
xlabel('tiempo')
ylabel('Erelativo')
title('Error relativo tiempo a tiempo')
grid on

