import requests
import struct
import threading
import time
import sys
import hashlib

MAX_4BYTE_INT = 4294967295

REQUEST_RETRIES = -1 # -1 - inf
RETRIES_TIMEOUT = 0.2

WORKING_PATH = './logs/'
def parse_args():   
    '''
    must be rewrited with sys.argv
    '''
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} NUMBER_OF_PROCESSES(EX. 4) NUMBER_OF_THREADS_PER_THREAD')
        sys.exit()
    if int(sys.argv[1]) > 500 or int(sys.argv[2])>500:
        print('MAXIMUM IS 500!')
        sys.exit()
    NUMBER_OF_THREADS = int(sys.argv[1])
    NUMBER_OF_THREADS_PER_PROCESS = int(sys.argv[2])
    if NUMBER_OF_THREADS_PER_PROCESS < 0:
        print('AT LEAST 1 THREAD')
        sys.exit()
        
    return NUMBER_OF_THREADS,NUMBER_OF_THREADS_PER_PROCESS

r_thread_work = False

WRONG_HASH = ['976111d30d212e8a177bfc0ea613caf3e14eb5d7',
              'ae65af750b06b3033ad792ab8c10215cfaa15759']

def request(session,stack,rstack):
    while not r_thread_work:
        time.sleep(1)
    while r_thread_work:
        try:
            hash = stack.pop()
        except:
            continue
        counter = REQUEST_RETRIES
        while counter != 0:
            try:
                
                response = requests.get('http://1.gravatar.com/avatar/'+hash)
                break
            except:
                time.sleep(RETRIES_TIMEOUT)
            counter -= 1
        try:
            hash_check = hashlib.sha1(response.content).hexdigest()
            if hash_check not in WRONG_HASH:
                rstack.append(hash)
        except:
            pass

def Brute(start,end,ThreadNumber,n_threads):
    global WRONG_HASH, r_thread_work
    session = requests.Session()
    stack = []
    

    response_stack = []

    threads = []
    for i in range(n_threads):
        threads.append(threading.Thread(target=request,args=(session,stack,response_stack)))
    for i in range(n_threads):
        threads[i].start()

    r_thread_work = True

    #r_thread = threading.Thread(target=request,args=(session,stack,response_stack)).start()
    with open(WORKING_PATH+str(ThreadNumber)+'_out.txt','w') as file:
        for first in range(start,end):
            first_h = struct.pack('I',first).hex()
            for second in range(0,MAX_4BYTE_INT+1):
                second_h = struct.pack('I',second).hex()
                for third in range(0,MAX_4BYTE_INT+1):
                    hash_t =  first_h + second_h + struct.pack('I',third).hex()
                    for fourth in range(0,MAX_4BYTE_INT+1):                        
                        hash = hash_t + struct.pack('I',fourth).hex()
                        stack.append(hash)

                        if fourth % 50 == 0:
                            #print(ThreadNumber,hash)
                            time.sleep(0.5)
                            
                        try:
                            hs = response_stack.pop()
                            #print(hs)
                            file.write(hs+'\n')
                            
                        except:
                            continue
        while True:
            if len(stack)>0:
                time.sleep(1)
            else:
                break
        r_thread_work = False
        for i in range(n_threads):
            threads[i].join()
        #r_thread.join()
        for el in response_stack:
            file.write(el)
                    

def main():
    global MAX_4BYTE_INT
    args = parse_args()
    NThreads = args[0]
    values = []
    

    koef = MAX_4BYTE_INT // NThreads
    

    pool = [None]*NThreads


    for i in range(0,NThreads):
        values.append(koef*(i))
    values.append(MAX_4BYTE_INT+1)
    print(values)
    print(f'\nSTARTING {NThreads} PROCESSES')
    print(f'STARTING {args[1]} THREADS PER PROCESSES')
    print(f'DUMPING TO {WORKING_PATH}')

    for i in range(NThreads):
        pool[i] = multiprocessing.Process(target=Brute,args=(values[i],values[i+1],i,args[1]))
        pool[i].start()

    for process in pool:
        process.join()
    



if __name__ == '__main__':
    import multiprocessing    
    #Brute(0,10000,0,1)
    main()
    

    