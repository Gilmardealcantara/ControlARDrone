clear
format longEng
M = readtable('./test_drone2/getDataok2/out_odom.txt');
M2 = csvread('./test_drone2/getDataok2/out_vel.txt', 1,0);
time2 = M2(:,1);
cv_linear_x = M2(:,2);
format longEng
M = readtable('./test_drone2/getDataok2/out_odom.txt');
M2 = csvread('./test_drone2/getDataok2/out_vel.txt', 1,0);
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


subplot(2,1,1);
hold on
Y1 = position_z(248);
Y2 = position_z(2167)-0.195;
X1 = time(776);
X2 = time(1572);
plot(time(248),position_z(248), 'mo')
plot(time(2167),position_z(2167), 'mo')
plot(time(776),position_z(776), 'ro')
plot(time(1572),position_z(1572), 'ro')

%plot(time, position_x, 'r');
%plot(time, position_y, 'g');
plot(time, position_z, 'b');
%plot(time, orientation_z, 'y');
legend('Y1', 'Y2', 'X1', 'X2', 'Position');
xlabel('Time');
ylabel('Position');
title('Position/Time');
grid

subplot(2,1,2);
hold on
% plot(time, linear_x, 'r');
% plot(time, linear_y, 'g');
% plot(time, linear_z, 'b');
%plot(time, angular_z, 'y');
% plot(time2, cv_linear_x, 'r');
% plot(time2, cv_linear_y, 'g');
plot(time2, cv_linear_z, 'b');
% plot(time2, cv_angular_z, 'y');

% legend('v_linear X','v_linear Y', 'v_linear Z', 'v_angular Z');
xlabel('Time');
ylabel('Speed command');
title('Speed command/Time');
grid

% find(position_z == Y1)
% find(position_z == Y2)

