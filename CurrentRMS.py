import math
import numpy 
import matplotlib.pyplot as plot

plot.axis([0,10,0,1])
current = numpy.arange(0,10,0.0002)
amplitude = 5*numpy.sin(current*50)
counter = 0;
for i in current:
    
    plot.scatter(i,amplitude[counter])
    plot.pause(0.05)
    counter=counter+1
plot.show()

""""


current = numpy.arange(0,10,0.02)
amplitude = 5*numpy.sin(current*50)
max = 0

for i in amplitude:
    if i > max:
        max = i
    
    
rms = max/math.sqrt(2)



print("I max = ",max)
print("I rms = ",rms)
print("amplituda = ",amplitude[-1])
plot.plot(current,amplitude)
plot.title('Sine wave')
plot.show()
"""