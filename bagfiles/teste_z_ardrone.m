Ts = 10*10^-3;
inicio = 700;
fim = 1000;
Y1 = position_z(248);
Y2 = position_z(2167)-0.23;
X1 = time(776);
X2 = time(1572);

cv_linear_z1 = mergeData(cv_linear_z); % dobra daados
cv_linear_z1 = cv_linear_z1(1:length(time))';
position_z1 = position_z ;

cv_linear_z2 = cv_linear_z1(inicio: fim);
position_z2 = position_z1(inicio:fim);
time3 = time(inicio:fim);

dataz1 = iddata(position_z1, cv_linear_z1, Ts);
dataz2 = iddata(position_z2, cv_linear_z2, Ts);

sys_z1 = tfest(dataz1,1,0);
sys_z2 = tfest(dataz2,1,0);

time_ns = time * 10^-9;
t = linspace(0,time_ns(end)-time_ns(1),length(cv_linear_z1));
y1 = lsim(sys_z1*10, cv_linear_z1, t);
y2 = lsim(sys_z2*10, cv_linear_z1, t);

plot(t, position_z1, t, y1 + Y1, t, y2 + Y1);
legend('real', 'sysZ1 p:2 z:0', 'sysZ2 - n amostras');
title('u=vz, y=p');










% % data = iddata(y,u,Ts)
% % sys = tfest(data,np,nz)
% % plot(time2, position_z(3079:5974))
% %if exist('sys_z') == 0
%     position_z2 = position_z(3079:5974)
%     inicio = 3079;
%     fim = 5974;
%     Ts = 10*10^-3;
%     dataz = iddata(position_z(inicio:fim) - position_z(inicio), cv_linear_z, Ts)
%     dataz2 = iddata(position_z2(1200:2200) - position_z2(1200), cv_linear_z(1200:2200), Ts);
%     sys_z = tfest(dataz,2,0);
%     sys_z2 = tfest(dataz,2,0);
% %end
% time_ns = time2 * 10^-9;
% t = linspace(0,time_ns(end)-time_ns(1),length(cv_linear_z));
% y1 = lsim(sys_z, cv_linear_z, t);
% y2 = lsim(sys_z2, cv_linear_z, t);
% plot(t, position_z(inicio: fim) - position_z(inicio), t, y1, t, y2);
% legend('real','planta', 'n amostras planta');
% title('u=vz, y=p');
% % plot(time(inicio: fim), position_z(inicio: fim) - position_z(inicio))


