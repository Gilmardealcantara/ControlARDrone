clear
M2 = readtable('out_odom_1110.txt');

time = table2array(M2(:,1));
position_x = table2array(M2(:,6));
position_y = table2array(M2(:,7));
position_z = table2array(M2(:,8));
orientation_z = table2array(M2(:,11));

hold on
plot(time, position_x, 'r');
plot(time, position_y, 'g');
plot(time, position_z, 'b');
plot(time, orientation_z, 'y');
legend('X','Y', 'Z', 'orientacao Z');

xlabel('tempo')
ylabel('Posicao/Orientacao')

