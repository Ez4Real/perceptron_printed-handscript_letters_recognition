import cv2
import glob
from math import pow, e
from weights import neurons as neurons3, presets as presets3

neurons = []
n = 1
presets = []
epoch = 0

class Neuron():

    def __init__(self, input_length):

        self.iterations = 0
        self.Xj = []
        self.input_length = input_length
        self.delta = 1
        self.epsilon = 1
        
    def result(self, Xj):
        self.S = 0
        self.Xj = Xj
    
        for i in range(self.input_length):
            self.S += self.Xj[i] * self.Wj[i]
        self.res = 1/(1+pow(e, -self.S))
        return self.res
    
    def correct_weights_active_inputs(self):
        for i in range(self.input_length):
            self.Wj[i] += n*self.delta*self.Xj[i]
            
    def epsilon_calculation(self, di):
        self.epsilon = di - self.res
    
    def delta_calculation(self):
        self.delta = self.res*(1-self.res)*self.epsilon

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
  
    
for index, neuron3 in enumerate(neurons3):
    neurons[index].Wj = neuron3.Wj
    
    
flag = False

while not flag:

    isCorrect = True
    for preset in presets:
        print(f'\nLetter: {preset["letter"]}----------------------')
        e_list = list()
        for indexN, neuron in enumerate(neurons):
            
            neuron.result(preset['inputs'])    
            neuron.epsilon_calculation(preset['desired'][indexN])
            neuron.delta_calculation()
            
            neuron.correct_weights_active_inputs()
             
            neuron.iterations += 1
            
            e_list.append(pow(neuron.epsilon, 2))
            
        error = sum(e_list)/2      
        if error > 0.05:
            isCorrect = False
        
        print(f'Error: {round(error, 3)} - Ireration: {neuron.iterations}')
        
    epoch += 1
    
    if isCorrect:
        flag = True

