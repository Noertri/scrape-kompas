from ext import data_path


cache_file = data_path.joinpath("urls.cache")


def cached(f):
    def wrapper(url, *args, **kwargs):
        ret = None
        caches = []

        if cache_file.exists():
            file_obj = cache_file.open("r", encoding="utf-8")
            caches.extend(file_obj.readlines())
            file_obj.close()

        if url not in caches:
            ret = f(url, *args, **kwargs)

            if ret:
                file_obj = cache_file.open("a", encoding="utf-8")
                file_obj.write(url+"\n")
                file_obj.close()
        
        return ret

    return wrapper
        