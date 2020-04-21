"""CPU Information module for rtl_sdr_fm_player"""
import subprocess
import threading
import time

class CPUInfo:
    """Displays current CPU usage info in a tkinter label"""
    def __init__(self, tk_cpu_label):
        self.cpu_utilisation = ''
        self.cpu_temp = ''
        self.cpu_text = tk_cpu_label

    # credit https://rosettacode.org/wiki/Linux_CPU_utilization
    def _cpu_utilisation(self):
        """Calculate CPU utilisation"""
        last_idle = last_total = 0
        while True and self.cpu_utilisation is not None:
            with open('/proc/stat') as proc_stat:
                fields = [float(column) for column in proc_stat.readline().strip().split()[1:]]
            idle, total = fields[3], sum(fields)
            idle_delta, total_delta = idle - last_idle, total - last_total
            last_idle, last_total = idle, total
            utilisation = 100.0 * (1.0 - idle_delta / total_delta)
            self.cpu_utilisation = ('%5.1f%%' % utilisation)
            time.sleep(2)

    def _cpu_info(self):
        """Update displayed CPU information"""
        get_temp = subprocess.check_output(["vcgencmd", "measure_temp"])
        self.cpu_temp = get_temp.decode('utf-8').lstrip('temp=').replace("'", "°")
        self.cpu_text.config(text='CPU %s %s' % (self.cpu_temp, self.cpu_utilisation))
        self.cpu_text.after(2000, self._cpu_info)

    def start(self):
        """Start daemon and label updater"""
        cpu_thread = threading.Thread(target=self._cpu_utilisation)
        cpu_thread.daemon = True
        cpu_thread.start()
        self._cpu_info()

    def get_cpu_utilisation(self):
        """Return CPU utilisation string"""
        return self.cpu_utilisation

    def get_cpu_temp(self):
        """Return CPU temperature string"""
        return self.cpu_temp
