from concurrent import futures

from flags import save_flag, get_flag, show, main #1

MAX_WORKES = 20 #2

def download_one(cc): #3
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKES, len(cc_list)) #4
    with futures.ThreadPoolExecutor(workers) as excutor: #5
        res = excutor.map(download_one, sorted(cc_list)) #6
    
    return len(list(res)) #7

if __name__ == '__main__':
    main(download_many) #8
