class Server: 
    def __init__(self, server_name=None):
        self.current_task = None
        self.time_remaining = 0
        self.server_name = server_name

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1 
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_ptime() * 60 / new_task.ptime

class Request:
    def __init__(self, time, ptime):
        self.timestamp = time
        self.ptime = ptime

    def get_stamp(self):
        return self.timestamp

    def get_ptime(self):
        return self.ptime

    def wait_time(self, current_time):
        return current_time - self.timestamp

def simulateOneServer(file):
    
    server = Server()
    waiting_times = []
    
    for current_second in range(max(file)):
    
        if (not server.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue() 
            waiting_times.append(next_task.wait_time(current_second)) 
            lab_printer.start_next(next_task)
    
        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, print_queue.size()))

def simulateManyServers(file, servers):
    
    server = Server()
    waiting_times = []
    
    for current_second in range(max(file)):
    
        if (not server.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue() 
            waiting_times.append(next_task.wait_time(current_second)) 
            lab_printer.start_next(next_task)
    
        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." %(average_wait, print_queue.size()))

def main():
    
    parse = argparse.ArgumentParser()
    parse.add_argument('url')
    parse.add_argument('servers', nargs='?', default=1)
    args = parse.parse_args()

    rawFile = urllib.request.urlopen(args.url).read()
    file = csv.reader(rawFile.decode('utf-8').splitlines())
    result = [row for row in file]

    servers = int(args.servers)
    if servers == 1:
        simulateOneServer(result)     
    else:
        simulateManyServers(result, servers)

if __name__  == '__main__':
    main()