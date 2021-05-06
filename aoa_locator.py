import serial
import serial.tools.list_ports
import threading
from parse import parse
from EventNotifier import Notifier

class Locator:
    '''Class managing communication with the AoA locator'''

    notifier = Notifier(["Error", "IQ_Event", "SW_Event", "RR_Event", "SS_Event", "FR_Event", "ME_Event", "MA_Event", "KE_Event", "KA_Event"])
    is_port_open = False
    thread = None
    stop_thread = False
    is_IQ_Event_subscribed = False
    is_SW_Event_subscribed = False
    is_RR_Event_subscribed = False
    is_SS_Event_subscribed = False
    is_FR_Event_subscribed = False
    is_ME_Event_subscribed = False
    is_MA_Event_subscribed = False
    is_KE_Event_subscribed = False
    is_KA_Event_subscribed = False
    
    def __init__(self, port=0, baudrate=38400, timeout=1, error_subscriber = ""):
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = 'COM'+str(port)
        self.ser.timeout = timeout
        self.notifier.subscribe("Error", error_subscriber)

    def get_port_config(self):
        """Function for getting the configuration of the COM port"""
        print("Port:", self.ser.port)
        print("Baudrate:", self.ser.baudrate)
        print("Timeout:", self.ser.timeout)

    def set_port_config(self, baudrate, port, timeout):
        """Function for setting the configuration of the COM port"""
        self.ser.baudrate = baudrate
        if isinstance(port, int):
            self.ser.port = 'COM'+str(port)
        else:
            self.ser.port = port
        self.ser.timeout = timeout

    def subscribe_event(self, event_name, subscriber):
        """Function for subscribing of one of the possible event"""
        if event_name == 'IQ':
            self.notifier.subscribe("IQ_Event", subscriber)
            self.is_IQ_Event_subscribed = True
        elif event_name == 'SW':
            self.notifier.subscribe("SW_Event", subscriber)
            self.is_SW_Event_subscribed = True
        elif event_name == 'RR':
            self.notifier.subscribe("RR_Event", subscriber)
            self.is_RR_Event_subscribed = True
        elif event_name == 'SS':
            self.notifier.subscribe("SS_Event", subscriber)
            self.is_SS_Event_subscribed = True
        elif event_name == 'FR':
            self.notifier.subscribe("FR_Event", subscriber)
            self.is_FR_Event_subscribed = True
        elif event_name == 'ME':
            self.notifier.subscribe("ME_Event", subscriber)
            self.is_ME_Event_subscribed = True
        elif event_name == 'MA':
            self.notifier.subscribe("MA_Event", subscriber)
            self.is_MA_Event_subscribed = True
        elif event_name == 'KE':
            self.notifier.subscribe("KE_Event", subscriber)
            self.is_KE_Event_subscribed = True
        elif event_name == 'KA':
            self.notifier.subscribe("KA_Event", subscriber)
            self.is_KA_Event_subscribed = True
        else:
            raise NameError('Unknown event name')

    def unsubscribe_event(self, event_name):
        """Function for unsubscribing of an event"""
        if event_name == 'IQ':
            self.notifier.remove_subscribers_by_event_name("IQ_Event")
            self.is_IQ_Event_subscribed = False
        elif event_name == 'SW':
            self.notifier.remove_subscribers_by_event_name("SW_Event")
            self.is_SW_Event_subscribed = False
        elif event_name == 'RR':
            self.notifier.remove_subscribers_by_event_name("RR_Event")
            self.is_RR_Event_subscribed = False
        elif event_name == 'SS':
            self.notifier.remove_subscribers_by_event_name("SS_Event")
            self.is_SS_Event_subscribed = False
        elif event_name == 'FR':
            self.notifier.remove_subscribers_by_event_name("FR_Event")
            self.is_FR_Event_subscribed = False
        elif event_name == 'ME':
            self.notifier.remove_subscribers_by_event_name("ME_Event")
            self.is_ME_Event_subscribed = False
        elif event_name == 'MA':
            self.notifier.remove_subscribers_by_event_name("MA_Event")
            self.is_MA_Event_subscribed = False
        elif event_name == 'KE':
            self.notifier.remove_subscribers_by_event_name("KE_Event")
            self.is_KE_Event_subscribed = False
        elif event_name == 'KA':
            self.notifier.remove_subscribers_by_event_name("KA_Event")
            self.is_KA_Event_subscribed = False
        else:
            raise NameError('Unknown event name')
            
    def open_port(self):
        """Function for starting the open/read/close port in a thread"""
        self.thread = threading.Thread(target=self.read_from_port, args =(lambda : self.stop_thread,)) 
        self.thread.start()

    def close_port(self):
        """Function for closing the COM port"""
        try:
            self.stop_thread = True
            self.thread.join()
        except AttributeError:
            self.notifier.raise_event("Error", 0, "COM Port not open")

    def get_port_list(self):
        """Function for getting a list of avalaible COM port"""
        ports = serial.tools.list_ports.comports()
        short_ports = []
        for element in ports:
            short_ports.append(element.device)
        return short_ports
        
    def read_from_port(self, stop):
        """Function for opening then reading data in a loop and then closing the port"""
        try:
            #open port
            self.ser.open()
        except Exception:
            self.notifier.raise_event("Error", 1, "Cannot open COM port")

        self.is_port_open = True
            
        while True:
            #read data from COM port
            try:
                reading = self.ser.readline().decode('utf-8')
                if reading:
                    #data present, parse it
                    parsed_data = parse('{}:{}', reading)
                    if parsed_data:
			#parse OK, raise correct event
                        if parsed_data[0] == 'IQ' and self.is_IQ_Event_subscribed == True:
                            self.notifier.raise_event("IQ_Event", parsed_data[1])
                        elif parsed_data[0] == 'SW' and self.is_SW_Event_subscribed == True:
                            self.notifier.raise_event("SW_Event", parsed_data[1])
                        elif parsed_data[0] == 'RR' and self.is_RR_Event_subscribed == True:
                            self.notifier.raise_event("RR_Event", parsed_data[1])
                        elif parsed_data[0] == 'SS' and self.is_SS_Event_subscribed == True:
                            self.notifier.raise_event("SS_Event", parsed_data[1])
                        elif parsed_data[0] == 'FR' and self.is_FR_Event_subscribed == True:
                            self.notifier.raise_event("FR_Event", parsed_data[1])
                        elif parsed_data[0] == 'ME' and self.is_ME_Event_subscribed == True:
                            self.notifier.raise_event("ME_Event", parsed_data[1])
                        elif parsed_data[0] == 'MA' and self.is_MA_Event_subscribed == True:
                            self.notifier.raise_event("MA_Event", parsed_data[1])
                        elif parsed_data[0] == 'KE' and self.is_KE_Event_subscribed == True:
                            self.notifier.raise_event("KE_Event", parsed_data[1])
                        elif parsed_data[0] == 'KA' and self.is_KA_Event_subscribed == True:
                            self.notifier.raise_event("KA_Event", parsed_data[1])
            except Exception:
                self.notifier.raise_event("Error", 0, "Error in received data")							
            if stop():
                break
            
        #close port   
        self.ser.close()
        self.is_port_open = False


        
