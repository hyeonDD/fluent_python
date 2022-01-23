charles = {'name': 'Charles L. Dodgson', 'born': 1832} 
lewis = charles #1

if lewis is charles: #2
    print('True')
print(id(charles),id(lewis))
lewis['balance'] = 950 #3
print(charles)