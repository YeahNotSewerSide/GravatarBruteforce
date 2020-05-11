import requests
import struct
import threading
import time
import sys

MAX_4BYTE_INT = 4294967295

WORKING_PATH = './logs/'
def parse_args():   
    '''
    must be rewrited with sys.argv
    '''
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} NUMBER_OF_THREAD(EX. 4)')
        sys.exit()
    if int(sys.argv[1]) > 500:
        print('MAXIMUM IS 500!')
        sys.exit()
    NUMBER_OF_THREADS = int(sys.argv[1])
    return NUMBER_OF_THREADS

r_thread_work = True

def request(session,stack,rstack):
    while r_thread_work:
        try:
            hash = stack.pop()
        except:
            continue
        response = session.get('https://www.gravatar.com/'+hash)
        if response.status_code == 200:
            rstack.append(hash)

def Brute(start,end,ThreadNumber):
    session = requests.Session()
    stack = []
    
    response_stack = []
    r_thread = threading.Thread(target=request,args=(session,stack,response_stack)).start()
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
                            time.sleep(1)
                            #print(hash)
                        try:
                            hs = response_stack.pop()
                            print(hs)
                            file.write(hs+'\n')
                            
                        except:
                            continue
        while True:
            if len(stack)>0:
                time.sleep(1)
            else:
                break
        r_thread_work = False
        r_thread.join()
        for el in response_stack:
            file.write(el)
                    

def main():
    global MAX_4BYTE_INT
    NThreads = parse_args()
    values = []
    

    koef = MAX_4BYTE_INT // NThreads
    

    pool = [None]*NThreads


    for i in range(0,NThreads):
        values.append(koef*(i))
    values.append(MAX_4BYTE_INT+1)
    print(values)
    print(f'\nSTARTING {NThreads} PROCESSES')
    print(f'DUMPING TO {WORKING_PATH}')

    for i in range(NThreads):
        pool[i] = multiprocessing.Process(target=Brute,args=(values[i],values[i+1],i))
        pool[i].start()

    for process in pool:
        process.join()
    



if __name__ == '__main__':
    import multiprocessing    
    
    main()
    

    
