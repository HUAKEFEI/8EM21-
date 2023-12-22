import rospy
from std_msgs.msg import Float64MultiArray

def talker():




    pub = rospy.Publisher('youbot_base/joints_vel_controller/command', Float64MultiArray, queue_size=10)

    rospy.init_node('pubListener', anonymous=False)

    rate = rospy.Rate(10) # 10hz

    ay = 0.33
    ax = 0.15
    R = 0.05
    v = 0.8
    r = 1
    w = v / r

    kp = 0.8
    ki = 0.1
    kd = 0.05

    error_sum_x = 0
    error_sum_y = 0
    last_error_x = 0
    last_error_y = 0

    while not rospy.is_shutdown():

        error_x = r - 1
        error_y = r - 1

        error_sum_x += error_x  
        error_sum_y += error_y

        delta_error_x = error_x - last_error_x
        delta_error_y = error_y - last_error_y

        linear_vel_x = kp * error_x + ki * error_sum_x + kd * delta_error_x #Скорость линии x
        linear_vel_y = kp * error_y + ki * error_sum_y + kd * delta_error_y #Скорость линии y

        angular_vel = w  # Угловая скорость

        # 计算各个轮子的转速	Рассчитаем скорость каждого колеса.
        # Мы используем только два колеса.
        f1_t = 0
        f2_t = 1/R*(-linear_vel_x+linear_vel_y) + angular_vel * (ax+ay)
        f3_t = 0
        f4_t = 1/R*(linear_vel_x+linear_vel_y) + angular_vel * (ax+ay)

        # 创建消息对象并设置数据
        msg = Float64MultiArray()
        msg.data = [f1_t, f2_t, f3_t, f4_t]
        
        # 发布消息
        pub.publish(msg)

        # 更新上一次误差
        last_error_x = error_x
        last_error_y = error_y
        # 控制发布频率
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass