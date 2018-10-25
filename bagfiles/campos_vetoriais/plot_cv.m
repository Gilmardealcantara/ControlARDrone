clear
format longEng
M = readtable('./out_odom.txt');
M2 = csvread('./out_vel.txt', 1,0);
time2 = M2(:,1);
cv_linear_x = M2(:,2);
cv_linear_y = M2(:,3);
cv_linear_z = M2(:,4);
cv_angular_x = M2(:,5);
cv_angular_y = M2(:,6);
cv_angular_z = M2(:,7);


time = table2array(M(:,1));
position_x = table2array(M(:,6));
position_y = table2array(M(:,7));
position_z = table2array(M(:,8));
orientation_z = table2array(M(:,11));
linear_x = table2array(M(:,49));
linear_y = table2array(M(:,50));
linear_z = table2array(M(:,51));
angular_x = table2array(M(:,52));
angular_y = table2array(M(:,53));
angular_z = table2array(M(:,54));

title('Deslocamento no plano XY');

plot(position_y, position_x);
