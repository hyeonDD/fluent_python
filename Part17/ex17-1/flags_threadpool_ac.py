from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKES = 20

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    cc_list = cc_list[:5] #1
    with futures.ThreadPoolExecutor(max_workers=3) as executor: #2
        to_do = []
        for cc in sorted(cc_list): #3
            future = executor.submit(download_one, cc) #4
            to_do.append(futures) #5
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future)) #6
        
        results = []
        for future in futures.as_completed(to_do): #7
            res = future.result() #8
            msg = '{} result: {!r}'
            print(msg.format(future, res)) #9
            results.append(res)
    
    return len(results)
    
    

if __name__ == '__main__':
    main(download_many)
