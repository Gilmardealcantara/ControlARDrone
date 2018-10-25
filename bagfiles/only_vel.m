clear
M2 = csvread('./test_drone2/1/out_vel.txt', 1,0);
time = M2(:,1);
cv_linear_x = M2(:,2);
cv_linear_y = M2(:,3);
cv_linear_z = M2(:,4);
cv_angular_x = M2(:,5);
cv_angular_y = M2(:,6);
cv_angular_z = M2(:,7);
hold on
plot(time, cv_linear_x, 'r');
hold on
plot(time, cv_linear_y, 'g');
hold on
plot(time, cv_linear_z, 'b');
hold on
plot(time, cv_angular_z, 'y');

legend('v_linear X','v_linear Y', 'v_linear Z', 'v_angular Z');
xlabel('Time');
ylabel('cmd_vel/vel');
title('cmd_vel-vel/Time');

