import time

class Timer:
    def __init__(self) -> None:
        self.time = time.time()
        self.prev_time = self.time
        self.finished = False
        self.started = False
        self.desired_duration = -1

    def update(self, delta_time: float) -> None:
        self.time = time.time()
        if self.time - self.prev_time >= self.desired_duration:
            self.finished = True
            self.started = False
            self.desired_duration = -1
        if self.started: return
        
        self.prev_time = self.time
        # oppure self.time += delta_time

    def start(self, desired_duration: float):
        if not self.started:
            self.started = True
            self.finished = False
            self.desired_duration = desired_duration

if __name__ == "__main__":
    t = Timer()
    t.start(5)
    print(t.desired_duration)
    while not t.finished:
        t.update(0.1)
    print("Finished")
