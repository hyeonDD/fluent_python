charles = {'name': 'Charles L. Dodgson', 'born': 1832} 
lewis = charles #1

if lewis is charles: #2    
    # print('True')
    pass
# print(id(charles),id(lewis))
lewis['balance'] = 950 #3
# print(charles)

alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950} 
if alex == charles:
    print('True')
if alex is not charles:
    print('True')
