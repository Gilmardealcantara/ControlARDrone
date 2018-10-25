clear
M2 = readtable('out_odom_1110.txt');
M = csvread('out_vell_1110.txt', 1,0);
% M2 = readtable('out_odom.txt');
% M = csvread('out_vel.txt', 1,0);

time = table2array(M2(:,1));
position_x = table2array(M2(:,6));
position_y = table2array(M2(:,7));
position_z = table2array(M2(:,8));
orientation_z = table2array(M2(:,11));

time2 = M(:,1);
linear_x = M(:,2);
linear_y = M(:,3);
linear_z = M(:,4);
angular_x = M(:,5);
angular_y = M(:,6);
angular_z = M(:,7);


subplot(2,1,1);
hold on
plot(time, position_x, 'r');
plot(time, position_y, 'g');
plot(time, position_z, 'b');
plot(time, orientation_z, 'y');
legend('X','Y', 'Z', 'orientacao Z');
xlabel('Time');
ylabel('Position/Orientation');
title('Position/Time');

subplot(2,1,2);
hold on
plot(time2, linear_x, 'r');
plot(time2, linear_y, 'g');
plot(time2, linear_z, 'b');
plot(time2, angular_z, 'y');

legend('linear X','linear Y', 'linear Z', 'angular Z');
xlabel('Time');
ylabel('Speed');
title('Speed/Time');
