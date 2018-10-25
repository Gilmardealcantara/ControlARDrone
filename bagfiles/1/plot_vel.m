M = csvread('out_vel.txt', 1,0)
time = M(:,1)
linear_x = M(:,2);
linear_y = M(:,3);
linear_z = M(:,4);
angular_x = M(:,5);
angular_y = M(:,6);
angular_z = M(:,7);

hold on
plot(time, linear_x, 'r');
plot(time, linear_y, 'g');
plot(time,linear_z, 'b');
plot(time, angular_z, 'y');

legend('linear X','linear Y', 'linear Z', 'angular Z');