from movement import Movement

if __name__ == '__main__':
    m = Movement()
    m.move_idle()
    input('Press any key to stop')
    m.stop()
