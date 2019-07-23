from Queue import Queue
from threading import Thread

from CwController import CwController
from CwEffect import CwEffect
from CwRestController import CwRestController
from CwRunService import CwRunService
from Settings import Settings

VALVE_COUNT = 8

if __name__ == '__main__':
    queue = Queue()

    # Start effect
    run_service = CwRunService(queue, VALVE_COUNT)
    server_thread = Thread(target=run_service.run)
    server_thread.start()

    # Start rest controller
    rest_controller = CwRestController(queue)
    rest_controller.run()
