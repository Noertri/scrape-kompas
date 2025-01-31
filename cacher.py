from ext import data_path, counter
from custom_logger import logger


cache_file = data_path.joinpath("urls.cache")


def cached(f):
    def wrapper(session, *, url):
        ret = None
        caches = []

        if cache_file.exists():
            file_obj = cache_file.open("r", encoding="utf-8")
            caches.extend(file_obj.readlines())
            file_obj.close()

        if url not in caches:
            try:
                ret = f(session, url)
            except Exception as error:
                logger.error(f"{error}")

            if ret:
                logger.info(f"{next(counter): 4d} : [SCRAPING] {url}")
                file_obj = cache_file.open("a", encoding="utf-8")
                file_obj.write(url+"\n")
                file_obj.close()
            else:
                logger.info(f"{next(counter): 4d} : [SKIP] {url}")
        
        return ret

    return wrapper
        