     
import os
import random
import shutil
 
classes = set()
files = {}
 
def compute_classification(counter, train, test):
    if counter in train:
        return 'train'
    elif counter in test:
        return 'test'
 
directory = 'dataset/'
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith('.png'):
            name = filename.split(' ', 1)[0]
            if not name in files:
                files[name] = list()
            
            files[name].append(filename)
            classes.add(name)
 
train_path = os.path.join('lego_dataset', 'train')
test_path = os.path.join('lego_dataset', 'test')
dirpath = 'dataset'
 
for e in classes:
    os.makedirs(os.path.join('lego_dataset', 'train', e), exist_ok=True)
    os.makedirs(os.path.join('lego_dataset', 'test', e), exist_ok=True)
    test = random.sample(range(0,800),200)
    train = [number for number in range(0,800) if number not in test]
    for counter, image in enumerate(files[e]):
        dest = compute_classification(counter, train, test)
        if dest == 'train':
            shutil.copy(os.path.join(dirpath, image), os.path.join(train_path, e, image))
        elif dest == 'test':
            shutil.copy(os.path.join(dirpath, image), os.path.join(test_path, e, image))
    #count_train = os.popen('ls -1 {} | wc -l'.format(os.path.join(train_path, e))).read()
    #count_test = os.popen('ls -1 {} | wc -l'.format(os.path.join(test_path, e))).read()
    #print('Class', e, '--> train', count_train, 'test', count_test)
