

def convert():

    # open raw values
    with open('logs/raw_log.txt', 'r') as f:

        # read next line in file
        line = f.readline()
        while 1:

            # break when last line is handled
            if not line:
                break
            
            # split the reading to get [timestamp, value]
            reading = line.replace('\n', '').split(',')

            # assign value to variable
            value = float(reading[1])

            # apply conversion
            # value = formula

            # append converted value to new file
            # auto close when done
            with open('converted_log.txt', 'a') as g:

                # write to file
                g.write('%s,%s\n'%(reading[0], str(value)))

            # read next line    
            line = f.readline()