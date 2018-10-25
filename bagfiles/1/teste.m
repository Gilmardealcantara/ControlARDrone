px = position_x(81:size(linear_x) + 80);
py = position_y(81:size(linear_y) + 80);
pz = position_z(81:size(linear_z) + 80);

datax = iddata(px,linear_x);
datay = iddata(py,linear_y);
dataz = iddata(pz,linear_z);

sys_x = tfest(datax,2,0)
sys_y = tfest(datay,2,0)
sys_z = tfest(dataz,2,0)
step(0.00000000009*sys_x)
step(0.0071*sys_y)