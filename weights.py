import cv2
import random
import glob
from math import pow

neurons = []
presets = []
n = 1

class Neuron():

    def __init__(self, input_length):

        self.Xj = []
        self.input_length = input_length
        self.Wj = [random.randint(1, 3) for i in range(input_length)]
        self.e = 0
        
    def result(self, Xj):
        self.S = 0
        self.Xj = Xj
    
        for i in range(self.input_length):
            self.S += self.Xj[i] * self.Wj[i]
        self.res = 1 if self.S >= 0 else 0
        return self.res
    
    def correct_weights_active_inputs(self):
        for i in range(self.input_length):
            self.Wj[i] += n*self.e*self.Xj[i]
    
    def epsilon_calculation(self, di, xi):
        self.result(xi)
        self.e = di - self.res

for index, image in enumerate(glob.iglob('letters/*.png')):
    
    img = cv2.imread(image)
    
    InputsLength = int(pow(len(img), 2))
    neuron = Neuron(InputsLength)
    
    for line in img:
        for pixel in line:
            x = 0
            if not pixel.any():
                x = 1
            neuron.Xj.append(x)
            
    desired = [0 for i in range(26)]
    desired[index] = 1
    
    presets.append({'letter': image[-5], 'inputs': neuron.Xj, 'desired': desired})
    neurons.append(neuron)
  
flag = False

while not flag:

    isCorrect = True
    for preset in presets:
        for indexN, neuron in enumerate(neurons):
    
            neuron.epsilon_calculation(preset['desired'][indexN], preset['inputs'])
            neuron.correct_weights_active_inputs()
            
            if neuron.res != preset['desired'][indexN]:
                isCorrect = False
    if isCorrect:
        flag = True