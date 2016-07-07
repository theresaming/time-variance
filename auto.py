import gzip, datetime, sys

def countLines(filename):
    f = gzip.open(filename, 'r')
    i = 0
    for i, line in enumerate(f):
        pass
    print i+1
    f.close()
    
        
def progressBar(iteration, total, prefix = 'Progress: ', suffix = 'Complete', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int) 
        barLength   - Optional  : character length of bar (Int) 
    """
    filledLength = int(round(barLength * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix))
    sys.stdout.flush()
    if iteration == total:
        print('\n')
        
def mean(arr):
    if len(arr) == 0:
        return -1
    else:
        return float(sum(arr)) / float(len(arr))
        

"""
EXAMPLE
# Initial call to print 0% progress
printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
for item in items:
    # Do stuff...
    # Update Progress Bar
    i += 1
    printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
"""

def variance(mylist):
    average = mean(mylist)
    v = sum((average - value) ** 2 for value in mylist) / len(mylist)
    return v
    
def fileAnalysis(filename):
    limit = 50000
    #filename: conn.12_00_00-13_00_00.log.gz
    #separator: \x09
    f = gzip.open(filename, 'r')

    #variable initialization
    ipArr = [] #ipsrc and dest array
    time = [] #2d time array
    data = {} #time increments dictionary matches --- ex dict = {"ipsrc ipdest:" [time arr]}
    counter = 0 #line counter
    intervals = []
    progressBar(counter, limit, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
    for line in f: #gather data
        if counter >= limit: #tester
            break
        #data needed: srcip, destip, duration
        #output COUNT, DURATION, VARIANCE, MEAN
        #calc variance: pvariance(array)
        #top 20 instances??????

        ############################################################
        """
        if counter == 6: # print header row
            print line
        """
        ############################################################
        if counter > 7: #this file starts at line 8
            temp = line.split('\x09')
            #srcip: temp[2] destip: temp[4]
            s = temp[2] + ' ' + temp[4] #ip
            temp[0] = datetime.datetime.fromtimestamp(float(temp[0]))
            #temp[0]= datetime.datetime.strftime(temp[0], '%Y-%m-%d %H:%M:%S')
            #temp[0] = datetime.datetime.fromtimestamp(float(temp[0])).strftime('%Y-%m-%d %H:%M:%S')
            
            currTime = temp[0] #current time of the line
            
            if s not in ipArr: #if new src and dest
                ipArr.append(s) #list of all source and dest ips combos
                time.append([]) #same index as ipArr
                ind = ipArr.index(s) # save index
                time[ind].append(currTime) #match with time index
                data[s] = time #change to array
            else: #if exists
                ind = ipArr.index(s)
                time[ind].append(currTime)
                data[s] = time
    
        progressBar(counter, limit, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        counter+=1 #increment counter
    for i in range(0,len(time)):
        if len(time[i]) > 1:
            time[i].sort()
            #change to time intervals
            for j in range(0,len(time[i]) - 1):
                #print((time[i][j+1]-time[i][j]).seconds)
                intervals.append(int((time[i][j+1]-time[i][j]).seconds)) #converts to seconds
            time[i] = intervals
            del time[i][-1]
        else:
            time[i] = []
        intervals = []
    #PERFORM ANALYSIS
    results = [] #count, duration, variance, mean same length as time
    #instantiate all elements to 0
    for i in range(0,len(time)):
        results.append([0])
    #print (time)
    for k in range(0,len(time)):
        if len(time[k]) > 0:
            #print(time[k])
            instances = len(time[k]) + 1
            m = mean(time[k])
            v = variance(time[k])
            #print (mean(time[k]))
            #print (variance(time[k]))
            results[k]= [ipArr[k],instances,m,v] #ips, instances, mean, variance
    #LOWEST VARIANCE AND HIGH COUNT
    #find means w round numbers
    val = True
    while val:
        varianceThreshold = input("\n\nEnter an upper variance threshold: ")
        countThreshold = input("Enter a lower count threshold: ")
        num = input("Enter how many elements to view: ")
        numCount = 0

        #sort by lowest variance
        #get rid of [0] elements
        newResults = []
        for i in results:
            if i != [0]:
                newResults.append(i)
                
        #sort by lowest variance
        newResults = sorted(newResults, key= lambda x: x[3])

        for element in newResults:
            if element[1]>=countThreshold and element[3]<=varianceThreshold and numCount < num:
                print element,'\n'
                numCount+=1
        looper = input("\nWould you like to continue? y/n: ")
        if looper == 'y':
            val = True
        else:
            val = False    

    """
    for element in results:
        if element != [0]:
            print element,'\n'
    """
    f.close()   

if __name__ == '__main__':
    filename = "conn.12_00_00-13_00_00.log.gz"

    #RUN ONCE
    #countLines(filename)
    #this file has 34,984,873 lines
    
    fileAnalysis(filename)
    
