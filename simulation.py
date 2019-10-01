import argparse
import urllib.request
import csv
import collections

class Server: 
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining - 1 
            if self.time_remaining <= 0:
                self.current_request = None

    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False

    def start_next(self,new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_ptime()

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

class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self): 
        return self.items == []
    def enqueue(self, item): 
        self.items.insert(0,item)
    def dequeue(self): 
        return self.items.pop()
    def size(self): 
        return len(self.items)

def simulateOneServer(file):
    
    server = Server()
    request_queue = Queue()
    waiting_times = []

    for sec in range(max(file.keys())):

        if file[sec]:
            for x in file[sec]:
                request = Request(sec,x)
                request_queue.enqueue(request)

        if (not server.busy()) and (not request_queue.is_empty()):
            next_request = request_queue.dequeue() 
            waiting_times.append(next_request.wait_time(sec)) 
            server.start_next(next_request)
        
        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs with %3d tasks remaining." %(average_wait, request_queue.size()))

def simulateManyServers(file, servers):
    
    server_list = []
    request_queue = Queue()
    waiting_times = []
    
    for x in range(servers):
        server_list.append(Server())
        waiting_times.append([])

    for sec in range(max(file.keys())):

        if file[sec]:
            for x in file[sec]:
                request = Request(sec,x)
                request_queue.enqueue(request)

        for serv in range(len(server_list)):
            if (not server_list[serv].busy()) and (not request_queue.is_empty()):
                next_request = request_queue.dequeue() 
                waiting_times[serv].append(next_request.wait_time(sec)) 
                server_list[serv].start_next(next_request)
    
            server_list[serv].tick()

    avg_wait = []
    requests = []
    for x in range(servers):
        avg_wait.append(sum(waiting_times[x]) / len(waiting_times[x]))
        requests.append(request_queue.size())
    print("Average Wait %6.2f secs with %3d tasks remaining." %(sum(avg_wait)/len(avg_wait), sum(requests)))

def main():
    
    parse = argparse.ArgumentParser()
    parse.add_argument('url')
    parse.add_argument('servers', nargs='?', default=1)
    args = parse.parse_args()

    rawFile = urllib.request.urlopen(args.url).read()
    file = csv.reader(rawFile.decode('utf-8').splitlines())
    result = collections.defaultdict(list)
    for row in file:
        result[int(row[0])].append(int(row[2]))

    servers = int(args.servers)
    if servers == 1:
        simulateOneServer(result)     
    else:
        simulateManyServers(result, servers)

if __name__  == '__main__':
    main()