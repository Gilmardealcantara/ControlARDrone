
if exist('sys_z') == 0
    datax = iddata(position_x,linear_x);
    datay = iddata(position_y,linear_y);
    dataz = iddata(position_z,linear_z);

    sys_x = tfest(datax,2,0);
    sys_y = tfest(datay,2,0);
    sys_z = tfest(dataz,2,0);
    %step(0.00000000009*sys_x)
end
step(feedback(sys_z, -1))

    