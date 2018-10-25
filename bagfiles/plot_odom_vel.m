clear
M = readtable('./test_drone2/1/out_odom.txt');
M2 = csvread('./test_drone2/1/out_vel.txt', 1,0);
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


subplot(3,1,1);
hold on
plot(time, position_x, 'r');
plot(time, position_y, 'g');
plot(time, position_z, 'b');
plot(time, orientation_z, 'y');
legend('X','Y', 'Z', 'orientacao Z');
xlabel('Time');
ylabel('Position/Orientation');
title('Position/Time');

subplot(3,1,2);
hold on
plot(time, linear_x, 'r');
plot(time, linear_y, 'g');
plot(time, linear_z, 'b');
plot(time, angular_z, 'y');

legend('linear X','linear Y', 'linear Z', 'angular Z');
xlabel('Time');
ylabel('Speed');
title('Speed/Time');

subplot(3,1,3);
hold on
plot(time2, cv_linear_x, 'r');
plot(time2, cv_linear_y, 'g');
plot(time2, cv_linear_z, 'b');
plot(time2, cv_angular_z, 'y');

legend('cv_linear X','cv_linear Y', 'cv_linear Z', 'cv_angular Z');
xlabel('Time');
ylabel('cmd_vel');
title('cmd_vel/Time');

