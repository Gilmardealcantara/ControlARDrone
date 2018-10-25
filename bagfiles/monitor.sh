rosbag record -O subset /ground_truth/state /cmd_vel
rosbag info subset.bag
rostopic echo -b subset.bag -p /ground_truth/state > out_odom.txt
rostopic echo -b subset.bag -p /cmd_vel > out_vel.txt
