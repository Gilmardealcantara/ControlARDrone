echo "takeoff"
rostopic pub /ardrone/takeoff std_msgs/Empty "{}" &; 
read a;
echo "land";
rostopic pub /ardrone/land std_msgs/Empty "{} &;
rostopic pub /ardrone/land std_msgs/Empty "{} &;
