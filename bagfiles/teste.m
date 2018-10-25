% data = iddata(y,u,Ts)
% sys = tfest(data,np,nz)
time = time * 10^-9;
Ts = 10*10^-3;
if exist('sys_z') == 0
    pv_datax = iddata(position_x,linear_x);
    pv_datay = iddata(position_y,linear_y);
    pv_dataz = iddata(position_z,linear_z);
   
    pcv_datax = iddata(position_x, cv_linear_x);
    pcv_datay = iddata(position_y, cv_linear_y);
    pcv_dataz = iddata(position_z, cv_linear_z);
    %pcv_dataz2 = iddata(position_z(250:600) - position_z(250), cv_linear_z(250:600), Ts);
    pcv_dataz2 = iddata(position_z - position_z(1), cv_linear_z, Ts);
   
    vcv_datax = iddata(linear_x, cv_linear_x);
    vcv_datay = iddata(linear_y, cv_linear_y);
    vcv_dataz = iddata(linear_z, cv_linear_z);
   
    %sys_x = tfest(datax,2,0);
    %sys_y = tfest(datay,2,0);
    pv_sys_z = tfest(pv_dataz,2,0);
    pcv_sys_z = tfest(pcv_dataz,2,0);
    pcv_sys_z2 = tfest(pcv_dataz2,2,0);

    vcv_sys_z = tfest(vcv_dataz,2,0);

    %step(0.00000000009*sys_x)
end
% step(feedback(-sys_z, 1))
subplot(3,1,1)
step(feedback(vcv_sys_z, 1))
title('u=cmd_vel, y=vel');

subplot(3,1,2)
step(feedback(-pcv_sys_z, 1))
title('u=cmd_vel, y=p');

subplot(3,1,3)
step(feedback(-pv_sys_z, 1))
title('u=el, y=p');    

t = linspace(0,time(end)-time(1),length(cv_linear_z));
y2 = lsim(pcv_sys_z2, cv_linear_z)
plot(t, position_z - position_z(1), t, y2, t, y3)

% plot(time2, position_z(3079:5974))1