clear
M = readtable('out_odom.txt');

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
plot(time, linear_x, 'r');
plot(time, linear_y, 'g');
plot(time, linear_z, 'b');
plot(time, angular_z, 'y');

legend('linear X','linear Y', 'linear Z', 'angular Z');
xlabel('Time');
ylabel('Speed');
title('Speed/Time');