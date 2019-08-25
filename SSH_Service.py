import os
import socket
import time

from GPIO_Init import getAnyKeyEvent

__author__ = "Hsuan Han Lai (Edward Lai)"
__date__ = "2019-04-02"

workDir = os.path.dirname(os.path.realpath(__file__))


class SSH_Service:
    def __init__(self):
        pass

    def get_ip_address(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    def get_current_connected(self):
        # from wireless import Wireless
        # wireless = Wireless()
        # print(wireless.current())
        # return wireless.current()
        return None

    def multiprocess_key_interrupt(self, server_process):
        print("in interrupt")
        getAnyKeyEvent()
        server_process.terminate()
        return None

    def start_SSH_Service(self):
        print(self.get_ip_address(), self.get_current_connected())
        # from multiprocessing import Process
        # interrupt = Process(target=self.multiprocess_key_interrupt())
        # interrupt.start()
        # interrupt.join()
        # app.run('0.0.0.0', 8000, debug=False)
        # server = Process(target=app.run('0.0.0.0', 8000, threaded=True, debug=False))
        # print(server, "Server Started")
        # print("Press any key to exit")
        # server.start()

        # time.sleep(1)

        # print("I am here 1")
        # getAnyKeyEvent()


        # import signal
        # import subprocess

        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        # pro = subprocess.Popen('python Server/file_server.py', stdout=subprocess.PIPE,
        #                        shell=True, preexec_fn=os.setsid)
        #
        # getAnyKeyEvent()
        # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
