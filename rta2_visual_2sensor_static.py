from importlib.metadata import metadata
import json
from operator import truediv
import pygame,clock
data_dict=[]
# Opening JSON file
with open('/Users/shubham/Desktop/TestRecording-LBackpack.json') as json_file:
    data = json.load(json_file)
 
    # Print the data of dictionary
    print(data.keys())
    print(data['sensors'])
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(data['walkwayConfig'])
    for i in data['frames']:

        num_ob=i['sensorMessage']['metadata']['numOfDetectedObjects']

        timestamp=((i['sensorMessage']['metadata']['timeStamp']))
        
        for j in range(num_ob):
            s=dict()
            s['sensorId']=(i['sensorMessage']['object']['detectedPoints'][j]['sensorId'])
            s['x']=i['sensorMessage']['object']['detectedPoints'][j]['x']
            s['y']=i['sensorMessage']['object']['detectedPoints'][j]['y']
            s['timestamp']=timestamp
            data_dict=data_dict+[s]


def insertionSort(data_dict):
  
    # Traverse through 1 to len(data_dict)
    for i in range(1, len(data_dict)):
  
        key = data_dict[i]
  
        # Move elements of data_dict[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >= 0 and key['timestamp'] < data_dict[j]['timestamp'] :
                data_dict[j + 1] = data_dict[j]
                j -= 1
        data_dict[j + 1] = key
    

insertionSort(data_dict)
offset=0.6
for i in data_dict:
    i['x']=int((i['x']+325)*offset)
    i['y']=int((i['y']+(595)*offset))


print(data_dict[0:6])

import pandas as pd

df = pd.DataFrame.from_dict(data_dict) 
df.to_csv (r'/Users/shubham/Desktop/readings_rta2.csv', index = False, header=True)


# visual code


pygame.init()
# create a screen:
offset=0.6
screen = pygame.display.set_mode((int(650*offset),int(1190*offset)))
done = False
x_whole=int(650*offset)
ywhole=int(1190*offset)


# (red,green,blue)
c = (255,255,255)

# never ending loop now:
def gridmaker():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for x in range(0,x_whole,int(10*offset)):

        pygame.draw.line(screen,c,(x,1),(x,ywhole), 1)
 
    for y in range(0,ywhole,int(10*offset)):
        pygame.draw.line(screen,c,(1,y),(x_whole,y), 1)       



t=data_dict[0]['timestamp']
cond = True
sensor1=[]
t1=0
t2=0
sensor2=[]
while True and cond:
    screen.fill((0,0,0))
    gridmaker()    
    
    for i in range(len(data_dict)):
        

        if t<data_dict[i]['timestamp']:
            t2=data_dict[i]['timestamp']
        


            break
        elif t==data_dict[i]['timestamp']:
            if data_dict[i]['sensorId']==1:
                if len(sensor1)>=1 and sensor1[-1]['timestamp']<t :
                    sensor1=[]
                sensor1=sensor1+[(data_dict[i])]
                t1=t
            else:
                if len(sensor2)>=1 and sensor2[-1]['timestamp']<t:
                    sensor2=[]
                sensor2=sensor2+[(data_dict[i])]
                t2=t
            #pygame.draw.circle(screen,(255,0,0),(data_dict[i]['x'],data_dict[i]['y']),4)

            
        
        if i == len(data_dict)-1:
            cond = False
        
        if len(sensor1)>=1:
            for i in sensor1:
                pygame.draw.circle(screen,(255,0,0),(i['x'],i['y']),4)
        if len(sensor2)>=1:

            for i in sensor2:
                pygame.draw.circle(screen,(255,0,0),(i['x'],i['y']),4)        
        
    difference=t2-t
    t=t2    
    clock = pygame.time.Clock()

  
    pygame.display.update()
    print(t)
    clock.tick(difference)
   
