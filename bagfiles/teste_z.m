% data = iddata(y,u,Ts)
% sys = tfest(data,np,nz)
% if exist('sys_z') == 0
    inicio = 250;
    fim = 600;
    Ts = 10*10^-3;
    dataz = iddata(position_z - position_z(1), cv_linear_z, Ts);
    dataz1 = iddata(position_z(inicio:fim) - position_z(inicio), cv_linear_z(inicio:fim), Ts);
    sys_z = tfest(dataz,2,0);
    sys_z1 = tfest(dataz1,2,0);
% end
time_ns = time * 10^-9;
t = linspace(0,time_ns(end)-time_ns(1),length(cv_linear_z));
y = lsim(sys_z, cv_linear_z, t);
y1 = lsim(sys_z1, cv_linear_z, t);
plot(t, position_z - position_z(1), t, y, t, y1);
legend('real','planta','planta n amostrans');
title('u=vz, y=p');
% plot(time(inicio: fim), position_z(inicio: fim) - position_z(inicio))


