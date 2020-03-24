# leave boot.py empty

import sys, time, serial, re, os, shutil

rbuffer = ''
system_dir = os.getcwd() + '\\scripts'

# just a simple helper def that transmits errors with a timestamp
# and a nice format
def error(tag:str, msg:str):

    # will exit the program when called upon
    exit('%s | ERROR, %s : %s\nexited.'%(str(round(time.time())), tag, msg))

# this def prints out a guideline for the user
def print_help():
    
    # first is general next is example
    print('\npython3 upload.py <baudrate> <timeout> <serial port> <scripts path>\npython3 upload.py 115200 0.1 COM4 myprogram.txt\n')

def validate_baud(i):
    if i.isdigit(): return int(i)
    print_help()
    error('argv[1]', 'You did not enter a correct baudrate : must be int')

def validate_timeout(i):
    fl = str(i).split('.')
    if fl[0].isdigit() and fl[1].isdigit(): return float(i)
    print_help()
    error('argv[2]', 'You did not enter a correct timeout : must be float separated by "." : e.g 0.1')

def validate_paramters(params):
    if len(params) < 5:
        print_help()
        error('argv', 'You did not enter the requirement input parameters')

def receive(connection, done:bool=False):
    global rbuffer

    # collect return from serial
    while 1:
        data = connection.read(1024)
        if not data:
            break
        else:
            rbuffer += data.decode(encoding='utf-8',errors='?')
    rbuffer = rbuffer.replace('\r','')

    # print return lines
    while '\n' in rbuffer:
        i = rbuffer.index('\n')
        line = rbuffer[:i]
        rbuffer = rbuffer[i+1:]
        print(line)

    # done
    if done:
        print(rbuffer)

def send(conection, string:str=''):
    connection.write([ord(v) for v in string+'\r'])
    receive(connection)

if __name__ == '__main__':
    # validate if input is correct
    validate_paramters(sys.argv)    

    # infer baudratess
    baudrate = validate_baud(sys.argv[1])

    # get timeout
    timeout = validate_timeout(sys.argv[2])

    # get port
    port = str(sys.argv[3])

    # load scripts
    with open(str(sys.argv[4]), 'r') as f:
        scripts = [l.replace('\n', '') for l in f.readlines()]
        scripts = set([os.path.basename(s) for s in scripts])

    # establish connection to serial port
    connection = serial.Serial(port=port,baudrate=baudrate,timeout=timeout)
    connection.flush()
    connection.write([3,3]) # equivalent with CTRL-C
    receive(connection, True)

    print('settings:')
    print('- port: %s, speed: %s, timeout: %s'%(port, baudrate, timeout))
    print('- including scripts: %s\n'%str(scripts))

    print('--- STARTING UPLOAD ---')

    send(connection, 'import os')

    for root, dirs, files in os.walk(system_dir):

        for x in files[:]:
            if scripts and x not in scripts:
                files.remove(x)
            print('')
            print(x)
        
        files.sort()    

        for file in files:
            path1 = os.path.join(root,file)
            infile = open(path1, 'r')
            path2 ='compressed_'+file

            if os.path.splitext(file)[1].lower() == '.py':
                print('ANALYZING', 'PATH {', os.path.splitext(file), '}')
                outfile = open(path2,mode='w')
                for line in infile:
                    line2 = line.strip()
                    if not line2:
                        pass
                    elif line2.startswith('#'):
                        pass
                    else:
                        outfile.write(line.rstrip()+'\n')
                
                outfile.close()
            infile.close()

            path3 = path1.replace(system_dir,'').lstrip('/')
            send(connection, "outfile=None")
            with open(path2, mode='rb') as f:
                while 1:
                    data = f.read(1024)
                    if not data:
                        break
                    send(connection, "outfile=open('{}',mode='wb')".format(path3))
                    time.sleep(0.5)
                    send(connection, "outfile.write({})".format(data))
                    time.sleep(0.5)
                    send(connection, "outfile.close()")
                    time.sleep(0.5)
         
            os.remove(path2)
    
    connection.write([3,3])
    receive(connection, True)
    connection.close()

    print('--- SCRIPT(S) UPLOADED ---')