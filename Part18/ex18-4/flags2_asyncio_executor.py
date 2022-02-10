import asyncio

@asyncio.coroutine
def download_one(cc, base_url, seaphore, verbose):
    try:
        with(yield from semaphore):
            image = yield from get_flag(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        loop = asyncio.get_event_loop() #1
        loop.run_in_executor(None, #2
                save,flag, image, cc.lower() + '.gif') #3
    status = HTTPStatus.ok
    msg = 'OK'

    if verbose and msg:
        print(cc, msg)
    
    return Result(status, cc)