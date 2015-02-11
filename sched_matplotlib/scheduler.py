
import config,time,sched

class Scheduler:
    '''
    Scheduler class
    '''

    def __init__(self, name, delay, callback, *args):
        self._name = name
        self._delay = delay
        self._callback = callback
        self._args = args
        self._cancelled = False
        self._sched = sched.scheduler(time.time, time.sleep)
        self._id = -1

    def run(self):
        while not self._cancelled:
            now = time.gmtime(time.time())
            delay = self._delay - (now.tm_min%(self._delay/60)) * 60 - now.tm_sec
            self._id = self._sched.enter(delay, 1, self._callback, self._args)
            self._sched.run()
        print "Scheduler func run returns"

    def cancel(self):
		self._cancelled = True
		try:
			self._sched.cancel(self._id)
		except ValueError:
			pass
		
