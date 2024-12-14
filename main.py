from DJITelloPy.djitellopy import Tello

tello = Tello()
tello.connect()
tello.takeoff()
time.sleep(5)
tello.land()
tello.end()