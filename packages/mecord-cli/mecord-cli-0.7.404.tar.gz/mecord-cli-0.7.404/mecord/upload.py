import time
from urllib.parse import *
from mecord.utils import directDomain
import os
thisFileDir = os.path.dirname(os.path.abspath(__file__))
proxy_autodl = os.path.join(thisFileDir, f"proxy_autodl")

def AutoDl_proxy():
    os.environ["http_proxy"] = "http://172.20.0.19:12798"
    os.environ["https_proxy"] = "http://172.20.0.19:12798"
    os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"
    os.environ["SSL_CERT_FILE"] = "/etc/ssl/certs/ca-certificates.crt"
    os.environ["no_proxy"] = "localhost,127.0.0.1,modelscope.com,aliyuncs.com,tencentyun.com,wisemodel.cn"

def addtionExif(srcFile, taskUUID):
    if taskUUID == None or len(taskUUID) == 0:
        return
    try:
        from pathlib import Path
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        if ext in [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".gif"]:
            from PIL import Image
            img = Image.open(srcFile)
            exif_dict = {
                "0th": { }, 
                "Exif": { }, 
                "1st": { },
                "thumbnail": None, 
                "GPS": { }
            }
            import piexif
            if taskUUID:
                exif_dict["0th"] = { 
                    piexif.ImageIFD.Software: f'make with mecord({taskUUID})'.encode(),
                    piexif.ImageIFD.Copyright: f'xinyu'.encode(),
                }
                exif_dict["Exif"] = {
                    piexif.ExifIFD.UserComment: f'make with mecord({taskUUID})'.encode(),
                }
            exif_dat = piexif.dump(exif_dict)
            img.save(srcFile, "webp", quality=90, exif=exif_dat)
        # elif ext in [".mp4",".mov",".avi",".wmv",".mpg",".mpeg",".rm",".ram",".flv",".swf",".ts"]:
        #     params = {}
        # elif ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
        #     params = {}
        # else:
        #     params = {}
    except:
        return

def transcode(srcFile):
    try:
        from pathlib import Path
        from PIL import Image
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
            image = Image.open(srcFile, "r")
            format = image.format
            if format.lower() != "webp":
                fname = Path(srcFile).name
                newFile = srcFile.replace(fname[fname.index("."):], ".webp")
                image.save(newFile, "webp", quality=90)
                image.close()
                return True, newFile
    except Exception as e:
        pass
    return False, srcFile

def additionalUrl(srcFile, ossUrl):
    from pathlib import Path
    from PIL import Image
    try:
        params = {}
        if len(srcFile) > 0:
            file_name = Path(srcFile).name
            ext = file_name[file_name.index("."):].lower()
            if ext in [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".gif"]:
                img = Image.open(srcFile)
                params["width"] = img.width
                params["height"] = img.height
            elif ext in [".mp4",".mov",".avi",".wmv",".mpg",".mpeg",".rm",".ram",".flv",".swf",".ts"]:
                params = {}
            elif ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
                params = {}
            else:
                params = {}
        parsed_url = urlparse(ossUrl)
        updated_query_string = urlencode(params, doseq=True)
        final_url = parsed_url._replace(query=updated_query_string).geturl()
        return final_url
    except:
        return ossUrl

def upload(src, taskUUID, _country=None, timeout=300, region=''):
    import os
    from mecord import store
    from pathlib import Path
    from mecord import taskUtils
    from mecord import xy_pb
    import requests
    if os.path.exists(src) == False:
        raise Exception(f"upload file not found")
    if os.path.exists(proxy_autodl):
        AutoDl_proxy()
    country = _country
    if not country:
        if store.is_multithread() or taskUUID != None:
            country = taskUtils.taskCountryWithUUID(taskUUID)
        else:
            firstTaskUUID, country = taskUtils.taskInfoWithFirstTask()
    if country is None:
        country = "sg"

    needDeleteSrc, newSrc = transcode(src)
    addtionExif(newSrc, taskUUID)
    file_name = Path(newSrc).name
    ossurl = ''
    content_type = ''
    getossurl_time = int(time.time()*1000)
    if os.path.getsize(newSrc) < 10:
        raise Exception(f'The file {newSrc} is less than 10 bytes.')
    for j in range(1, 4):
        ossurl, content_type = xy_pb.GetOssUrl(country, os.path.splitext(file_name)[-1][1:], region)
        if len(ossurl) == 0:
            if j == 3:
                raise Exception(f"oss server is not avalid, msg = {content_type}")
            else:
                print(f"GetOssUrl failed. Resending...+{j}")
                continue
        if len(ossurl) > 0:
            break
    ossurl = ossurl.replace('\\u0026', '&')
    print(f'{taskUUID} === getossurl_time: {int(time.time()*1000) - getossurl_time}ms')
    print(f'{taskUUID} === accelerate ossurl: {ossurl}')
    headers = dict()
    headers['Content-Type'] = content_type
    # requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False
    start_time = int(time.time()*1000)
    with open(newSrc, 'rb') as f:
        data = f.read()
    read_time = int(time.time()*1000) - start_time
    res = s.put(ossurl, data=data, headers=headers, timeout=timeout)
    end_time = int(time.time()*1000)
    put_time = end_time - start_time - read_time
    total_time = end_time - start_time
    request_id = res.headers.get('x-oss-request-id')
    print(f'加速链接上传 {ossurl} === x-oss-request-id:{request_id}  file_read_time: {read_time}ms  file_put_time: {put_time}ms  total_time: {total_time}ms')

    s.close()
    if res.status_code == 200:
        ossurl = additionalUrl(newSrc, ossurl)
        if needDeleteSrc:
            os.remove(newSrc)
        return ossurl
    elif str(res.status_code).startswith('5'):
        ossurl = directDomain(ossurl)
        print(f'{taskUUID} === direct ossurl: {ossurl}')
        s = requests.session()
        s.keep_alive = False
        start_time2 = int(time.time()*1000)
        _res = s.put(ossurl, data=data, headers=headers, timeout=timeout)
        end_time2 = int(time.time()*1000)
        put_time2 = end_time2 - start_time2
        total_time2 = put_time2 + read_time
        request_id2 = res.headers.get('x-oss-request-id')
        print(f'直连链接上传 {ossurl} === x-oss-request-id:{request_id2}  file_read_time: {read_time}ms  file_put_time: {put_time2}ms  total_time: {total_time2}ms')
        s.close()
        if _res.status_code == 200:
            ossurl = additionalUrl(newSrc, ossurl)
            if needDeleteSrc:
                os.remove(newSrc)
            return ossurl
        else:
            raise Exception(f"upload file fail! (Direct link) res({res.status_code}) = {_res}")
    else:
        raise Exception(f"upload file fail! res({res.status_code}) = {res}")

def upload_byte(byte, suffix, taskUUID, _country=None, timeout=300, region=''):
    from mecord import store
    from mecord import taskUtils
    from mecord import xy_pb
    import requests
    country = _country
    if not country:
        if store.is_multithread() or taskUUID != None:
            country = taskUtils.taskCountryWithUUID(taskUUID)
        else:
            firstTaskUUID, country = taskUtils.taskInfoWithFirstTask()
    if country is None:
        country = "test"

    ossurl = ''
    content_type = ''
    for j in range(4):
        ossurl, content_type = xy_pb.GetOssUrl(country, suffix, region)
        if len(ossurl) == 0:
            if j == 3:
                raise Exception(f"oss server is not avalid, msg = {content_type}")
            else:
                print(f"GetOssUrl failed. Resending...+{j}")
                time.sleep(1)
                continue
        if len(ossurl) > 0:
            break
    ossurl = ossurl.replace('\\u0026', '&')
    headers = dict()
    headers['Content-Type'] = content_type
    # requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False
    res = s.put(ossurl, data=byte, headers=headers, timeout=timeout)

    s.close()
    if res.status_code == 200:
        ossurl = additionalUrl("", ossurl)
        return ossurl
    elif str(res.status_code).startswith('5'):
        ossurl = directDomain(ossurl)
        s = requests.session()
        s.keep_alive = False
        _res = s.put(ossurl, data=byte, headers=headers, timeout=timeout)
        s.close()
        if _res.status_code == 200:
            ossurl = additionalUrl("", ossurl)
            return ossurl
        else:
            raise Exception(f"upload file fail! (Direct link) res({res.status_code}) = {_res}")
    else:
        raise Exception(f"upload file fail! res({res.status_code}) = {res}")

def uploadWidget(src, widgetid, timeout=300):
    from mecord import xy_pb
    import requests
    ossurl, content_type = xy_pb.GetWidgetOssUrl(widgetid)
    if len(ossurl) == 0:
        raise Exception("oss server is not avalid")

    i = 0
    while True:
        headers = dict()
        headers['Content-Type'] = content_type
        requests.adapters.DEFAULT_RETRIES = 3
        s = requests.session()
        s.keep_alive = False
        res = s.put(ossurl, data=open(src, 'rb').read(), headers=headers, timeout=timeout)
        s.close()
        if res.status_code == 200:
            ossurl = additionalUrl(src, ossurl)
            checkid = xy_pb.WidgetUploadEnd(ossurl)
            if checkid > 0:
                return ossurl, checkid
            else:
                raise Exception("check fail!")
        elif i >= 3:
            raise Exception(f"failed more than 3 times, upload file fail! res = {res}")
        else:
            i += 1
            print(f"Sending failed. Resending...+{i}")
            time.sleep(0.5)

def uploadModel(name, cover, model_url, type, taskUUID):
    from mecord import taskUtils
    from mecord import xy_pb
    from mecord import store
    realTaskUUID = taskUUID
    country = None
    if store.is_multithread() or taskUUID != None:
        country = taskUtils.taskCountryWithUUID(taskUUID)
    else:
        firstTaskUUID, country = taskUtils.taskInfoWithFirstTask()
        if realTaskUUID == None:
            realTaskUUID = firstTaskUUID
    if country == None:
        country = "test"
    return xy_pb.UploadMarketModel(country, name, cover, model_url, type, realTaskUUID)
