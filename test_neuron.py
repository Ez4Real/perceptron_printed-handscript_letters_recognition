from main import *

test_presets = []

for index, image in enumerate(glob.iglob('test/*.png')):
    
    img = cv2.imread(image)
    
    InputsLength = int(pow(len(img), 2))
    inputs = []
    
    for line in img:
        for pixel in line:
            x = 0
            if not pixel.any():
                x = 1
            inputs.append(x)
            
    desired = [0 for i in range(26)]
    desired[index] = 1
    
    test_presets.append({'letter': image[-5], 'inputs': inputs, 'desired': desired})
    
for preset in test_presets:
    print(f'\nLetter: {preset["letter"]}\n-----------------------------------')
    for indexN, neuron in enumerate(neurons):
        
        neuron.result(preset['inputs'])
        
        print(f'Neuron-{indexN} | Desired: {preset["desired"][indexN]} | Result: {round(neuron.res, 3)}  ')