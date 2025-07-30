def speed(distance, time):
    return distance / time

def distance(speed, time):
    return speed * time

def time(distance, speed):
    return distance / speed

def acceleration(final_velocity, initial_velocity, time):
    return (final_velocity - initial_velocity) / time

def force(mass, acceleration):
    return mass * acceleration

def weight(mass, gravity=9.8):
    return mass * gravity

