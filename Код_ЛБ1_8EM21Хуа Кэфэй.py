import rospy
from std_msgs.msg import Float64MultiArray


def talker():
    pub = rospy.Publisher('youbot_base/joints_vel_controller/command', Float64MultiArray, queue_size=10)
    rospy.init_node('pubListener', anonymous=False)
    rate = rospy.Rate(10)  # 10hz

    v = 0.6
    vy = 0
    vx = 0
    R = 0.05
    ay = 0.33
    ax = 0.15
    r = 1
    w = v / r

    while not rospy.is_shutdown():
        # 计算各个轮子的转速 Рассчитаем скорость каждого колеса.
        # Мы используем только два колеса.
        f1_t = 0
        f2_t = 1 / R * (-vx + vy) + w * (ax + ay)
        f3_t = 0
        f4_t = 1 / R * (vx + vy) + w * (ax + ay)

        msg = Float64MultiArray()
        msg.data = [f1_t, f2_t, f3_t, f4_t]

        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
