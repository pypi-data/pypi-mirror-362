import asyncio
import base64
import datetime
import inspect
import json
import os.path
import string
import subprocess
import sys
import uuid
import warnings
from functools import wraps
from io import BytesIO
from dateutil import parser as date_parser
from urllib.parse import urlparse, parse_qs
from .exceptions import AuthenticationRequired
from .filters import Language
import re
import random
import hashlib
from typing import Union, List

GUEST_TOKEN_REGEX = re.compile("gt=(.*?);")
MIGRATION_REGEX = re.compile(r"""(http(?:s)?://(?:www\.)?(twitter|x){1}\.com(/x)?/migrate([/?])?tok=[a-zA-Z0-9%\-_]+)+""", re.VERBOSE)
MIME_TYPES = {
    "png": ("image/png", [b"\x89PNG\r\n\x1a\n"]),
    "jpg": ("image/jpeg", [b"\xFF\xD8\xFF"]),
    "jpeg": ("image/jpeg", [b"\xFF\xD8\xFF"]),
    "jfif": ("image/jpeg", [b"\xFF\xD8\xFF\xE0", b"\xFF\xD8\xFF\xE1"]),
    "gif": ("image/gif", [b"GIF87a", b"GIF89a"]),
    "webp": ("image/webp", [b"RIFF"]),
    "mp4": ("video/mp4", [b"\x00\x00\x00\x18ftypisom", b"\x00\x00\x00\x18ftypmp42",
                          b"\x00\x00\x00\x18ftypisom", b"\x00\x00\x00\x18ftypMSNV",
                          b"\x00\x00\x00\x18ftypmp41"]),
    "mov": ("video/quicktime", [b"\x00\x00\x00\x14ftypqt"]),
    "m4v": ("video/x-m4v", [b"\x00\x00\x00\x18ftypM4V", b"\x00\x00\x00\x20ftypM4V"])
}

WORKBOOK_HEADERS = ['Date', 'Author', 'id', 'text', 'is_retweet', 'is_reply', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']

SENSITIVE_MEDIA_TAGS = ['adult_content', 'graphic_violence', 'other']
def Warn(text, category=DeprecationWarning):
    this_text = text
    this_category = category

    def decorator(method):
        if inspect.iscoroutinefunction(method):
            @wraps(method)
            async def async_wrapper(self, *args, **kwargs):
                warnings.warn(message=this_text, category=this_category)
                return await method(self, *args, **kwargs)

            return async_wrapper
        else:
            @wraps(method)
            def sync_wrapper(self, *args, **kwargs):
                warnings.warn(message=this_text, category=this_category)
                return method(self, *args, **kwargs)

            return sync_wrapper
    return decorator

def DictRequestData(cls):

    def method_wrapper_decorator(func):
        request_keys = ["method", "url", "params", "json", "data"]

        def wrapper(self, *args, **kwargs):
            request_data = func(self, *args, **kwargs)

            request = {"headers": {}}
            for index, data in enumerate(request_data):
                this_key = request_keys[index]
                request[this_key] = data
            return request

        return wrapper

    if inspect.isclass(cls):
        for name, method in vars(cls).items():
            if name != "__init__" and callable(method):
                setattr(cls, name, method_wrapper_decorator(method))
        return cls
    return method_wrapper_decorator(cls)


def AuthRequired(cls):
    def method_async_wrapper_decorator(func):
        async def wrapper(self, *args, **kwargs):
            if self.me is None:
                raise AuthenticationRequired(200, "GenericForbidden", None)

            return await func(self, *args, **kwargs)
        return wrapper

    def method_wrapper_decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.me is None:
                raise AuthenticationRequired(200, "GenericForbidden", None)

            return func(self, *args, **kwargs)
        return wrapper

    if inspect.isclass(cls):
        for name, method in vars(cls).items():
            if name != "__init__" and callable(method):
                if "iter_" in name:
                    setattr(cls, name, method_wrapper_decorator(method))
                else:
                    setattr(cls, name, method_async_wrapper_decorator(method))
        return cls

    if "iter_" in cls.__name__:
        return method_wrapper_decorator(cls)
    return method_async_wrapper_decorator(cls)

def mime_from_buffer(file_buffer_or_bytes):
    try:
        import magic
        mime_detector = magic.Magic(mime=True)
        return mime_detector.from_buffer(file_buffer_or_bytes)
    except ImportError:
        for file_type, (mime_type, this_file_headers) in MIME_TYPES.items():
            for header in this_file_headers:
                if file_buffer_or_bytes.startswith(header):
                  return mime_type


    return None



def get_running_loop():
    if sys.version_info >= (3, 7):
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
            # return asyncio.get_event_loop_policy().get_event_loop()
    else:
        return asyncio.get_event_loop()


async def async_list(generator_base_object):
    async for _ in generator_base_object.generator():
        pass
    return generator_base_object


def float_to_hex(x):
    result = []
    quotient = int(x)
    fraction = x - quotient

    while quotient > 0:
        quotient = int(x / 16)
        remainder = int(x - (float(quotient) * 16))

        if remainder > 9:
            result.insert(0, chr(remainder + 55))
        else:
            result.insert(0, str(remainder))

        x = float(quotient)

    if fraction == 0:
        return ''.join(result)

    result.append('.')

    while fraction > 0:
        fraction *= 16
        integer = int(fraction)
        fraction -= float(integer)

        if integer > 9:
            result.append(chr(integer + 55))
        else:
            result.append(str(integer))

    return ''.join(result)


def is_odd(num: Union[int, float]):
    if num % 2:
        return -1.0
    return 0.0


def base64_encode(this_string):
    this_string = this_string.encode() if isinstance(this_string, str) else this_string
    return base64.b64encode(this_string).decode()


def base64_decode(this_input):
    try:
        data = base64.b64decode(this_input)
        return data.decode()
    except Exception: # noqa
        return list(bytes(this_input, "utf-8"))


def replace_between_indexes(original_string, from_index, to_index, replacement_text):
    new_string = original_string[:from_index] + replacement_text + original_string[to_index:]
    return new_string


def decodeBase64(encoded_string):
    return base64.b64decode(encoded_string).decode("utf-8")


def bar_progress(filename, total, current, width=80):
    progress_message = f"[{filename}] Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def parse_wait_time(wait_time):
    if not wait_time:
        return 0

    if isinstance(wait_time, (tuple, list)):

        if len(wait_time) == 1:
            return int(wait_time[0])

        wait_time = [int(i) for i in wait_time[:2]]
        return random.randint(*wait_time)

    return int(wait_time)


def get_next_index(iterable, current_index, __default__=None):
    try:
        _ = iterable[current_index + 1]
        return current_index + 1
    except IndexError:
        return __default__


def custom_json(self, **kwargs):
    try:
        return json.loads(self.content, **kwargs)
    except:
        return None


def create_request_id():
    return str(uuid.uuid1())

def create_conversation_id(sender, receiver):
    sender = int(sender)
    receiver = int(receiver)

    if sender > receiver:
        return f"{receiver}-{sender}"
    else:
        return f"{sender}-{receiver}"


def create_query_id():
    return get_random_string(22)


def check_if_file_is_supported(file):
    if isinstance(file, str) and not str(file).startswith("https://") and not os.path.exists(file):
        raise ValueError("Path {} doesn't exists".format(file))

    if isinstance(file, bytes):
        file = file
        file_mime = mime_from_buffer(file)
    elif isinstance(file, BytesIO):
        file = file.getvalue()
        file_mime = mime_from_buffer(file)
    elif str(file.__class__.__name__) == "Gif":
        file_extension = "gif"
        file_mime = MIME_TYPES.get(file_extension)
    else:
        file = file.split("?")[0]
        file_extension = file.split(".")[-1]
        file_mime = MIME_TYPES.get(file_extension)[0]

    if file_mime not in [i[0] for i in list(MIME_TYPES.values())]:
        raise ValueError("File Extension is not supported. Use any of {}".format(list(MIME_TYPES.keys())))

    return file_mime


def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=int(length)))


def calculate_md5(file_path):
    if str(file_path).startswith("https://"):
        return None

    md5_hash = hashlib.md5()
    if isinstance(file_path, bytes):
        md5_hash.update(file_path)
    else:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
    return md5_hash.hexdigest()


def create_media_entities(files):
    entities = []
    for file in files:
        media_id = file.media_id if hasattr(file, "media_id") else file
        entities.append({
            "media_id": media_id,
            "tagged_users": []
        })

    return entities


def check_sensitive_media_tags(tags):
    return [tag for tag in tags if tag in SENSITIVE_MEDIA_TAGS]


def find_objects(obj, key, value, recursive=True, none_value=None):
    results = []

    def find_matching_objects(_obj, _key, _value):
        if isinstance(_obj, dict):
            if _key in _obj:
                found = False
                if _value is None:
                    found = True
                    results.append(_obj[_key])
                elif (isinstance(_value, list) and _obj[_key] in _value) or _obj[_key] == _value:
                    found = True
                    results.append(_obj)

                if not recursive and found:
                    return results[0]

            for sub_obj in _obj.values():
                find_matching_objects(sub_obj, _key, _value)
        elif isinstance(_obj, list):
            for item in _obj:
                find_matching_objects(item, _key, _value)

    find_matching_objects(obj, key, value)

    if len(results) == 1:
        return results[0]

    if len(results) == 0:
        return none_value

    if not recursive:
        return results[0]

    return results


def create_pool(duration: int, *choices):
    data = {
        "twitter:long:duration_minutes": duration,
        "twitter:api:api:endpoint": "1",
        "twitter:card": f"poll{len(choices)}choice_text_only"
    }

    for index, choice in enumerate(choices, start=1):
        key = f"twitter:string:choice{index}_label"
        data[key] = choice

    return data


def parse_time(time):
    if not time:
        return None

    if isinstance(time, (datetime.datetime, datetime.date)):
        return time

    if isinstance(time, float):
        time = int(time)

    if isinstance(time, int) or str(time).isdigit():
        try:
            return datetime.datetime.fromtimestamp(int(time))
        except (OSError, ValueError):
            return datetime.datetime.fromtimestamp(int(time) / 1000)

    return date_parser.parse(time)


async def get_user_from_typehead(target_username, users):
    for user in users:
        if str(user.username).lower() == str(target_username).lower():
            return user
    return None


def get_tweet_id(tweet_identifier):
    if str(tweet_identifier.__class__.__name__) == "Tweet":
        return tweet_identifier.id
    else:
        return urlparse(str(tweet_identifier)).path.split("/")[-1]


def is_tweet_protected(raw):
    protected = find_objects(raw, "__typename", ["TweetUnavailable", "TweetTombstone"], recursive=False)

    if protected is None:
        is_not_dummy_object = find_objects(raw, "tweet_results", None, recursive=False)
        if isinstance(is_not_dummy_object, dict) and len(is_not_dummy_object) == 0:
            return True

    return protected


def check_translation_lang(lang):
    for k, v in vars(Language).items():
        if not str(k).startswith("_"):
            if str(k).lower() == str(lang).lower() or str(v).lower() == str(lang).lower():
                return v

    raise ValueError(f"Language {lang} is not supported")


def iterable_to_string(__iterable__: Union[list, tuple], __delimiter__: str = ",", __attr__: str = None):
    if not isinstance(__iterable__, (list, tuple)) or len(__iterable__) == 0:
        return ""

    if __attr__:
        __iterable__ = [str(getattr(i, __attr__)) for i in __iterable__]

    return __delimiter__.join(__iterable__)


def dict_to_string(__dict__: dict, __object_delimiter__: str = "=", __end_delimiter__: str = ";"):
    actual_string = ""
    for key, value in __dict__.items():
        actual_string += f"{key}{__object_delimiter__}{value}{__end_delimiter__}"

    return actual_string


def get_url_parts(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    url_parts = {
        "scheme": parsed_url.scheme,
        "netloc": parsed_url.netloc,
        "path": parsed_url.path,
        "params": parsed_url.params,
        "query": query_params,
        "fragment": parsed_url.fragment,
        "host": f"{parsed_url.scheme}://{parsed_url.netloc}"
    }

    return url_parts


def unpack_proxy(proxy_dict):
    username, password, host, port = None, None, None, None
    if str(proxy_dict.__class__.__name__) == "Proxy":
        proxy_dict = proxy_dict.get_dict()

    proxy = proxy_dict.get("http://") or proxy_dict.get("https://")
    scheme, url = proxy.split("://")
    creds, host_with_port = None, None
    url_split = url.split("@")
    if len(url_split) == 2:
        creds, host_with_port = url_split
    else:
        host_with_port = url_split[0]

    host, port = host_with_port.split(":")
    if creds is not None:
        username, password = creds.split(":")

    return {
        "type": scheme,
        "host": host,
        "port": port,
        "username": username,
        "password": password
    }


def run_command(command):
    try:
        if isinstance(command, (list, tuple)):
            command = " ".join(command)

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command '{command}' failed with error: {e.stderr.decode('utf-8')}")


def encode_audio_message(input_filename, ffmpeg_path=None):
    """
    Encode the mp3 or audio file to Twitter Audio Message Format

    :param input_filename: Filename of mp3/ogg or audio file
    :param ffmpeg_path: Path of 'ffmpeg' binary for your platform
    :return: str (`encoded_filename`)
    """

    if not ffmpeg_path:
        ffmpeg_path = "ffmpeg"

    _input_filename = f'"{input_filename}"'
    _output_aac_filename = f'"{input_filename}.aac"'
    output_filename = f'"{input_filename}.mp4"'

    commands = [
        [ffmpeg_path, "-y", "-i", _input_filename, "-c:a", "aac", "-b:a", "65k", "-ar", "44100", "-ac", "1", _output_aac_filename],
        [ffmpeg_path, "-y", "-f", "lavfi", "-i", "color=c=black:s=854x480", "-i", _output_aac_filename, "-c:v", "libx264", "-c:a", "copy", "-shortest", output_filename]
    ]

    for command in commands:
        run_command(command)

    try:
        # Attempt to delete aac audio file in order to save disk space
        os.remove(_output_aac_filename)
    except:
        pass

    return output_filename[1:-1]


def tweet_id_to_datetime(tweet_id: int):
    return datetime.datetime.fromtimestamp(((tweet_id >> 22) + 1288834974657) / 1000.0)

def json_stringify(json_data):
    return str(json.dumps(json_data, separators=(",", ":")))

def create_search_query(
        search_term=None,
        from_users=None,
        to_users=None,
        mentioning_these_users=None,
        exact_word=None,
        none_of_these_words=None,
        language=None,
        include_replies=True,
        only_replies=False,
        include_links=True,
        only_links=False,
        minimum_replies=None,
        minimum_likes=None,
        minimum_reposts=None,
        from_date=None,
        to_date=None
):
    date_format = "%Y-%m-%d"
    new_search_term = ""

    if search_term:
        new_search_term += f" {search_term} "

    if exact_word:
        new_search_term += f' "{exact_word}" '

    if from_users:
        if not isinstance(from_users, list):
            from_users = [from_users]

        from_users = [f"from:{i}" for i in from_users]
        from_users = " OR ".join(from_users)
        new_search_term += f" ({from_users}) "

    if to_users:
        if not isinstance(to_users, list):
            to_users = [to_users]

        to_users = [f"to:{i}" for i in to_users]
        to_users = " OR ".join(to_users)
        new_search_term += f" ({to_users}) "

    if mentioning_these_users:
        if not isinstance(mentioning_these_users, list):
            mentioning_these_users = [mentioning_these_users]

        mentioning_these_users = [f"@{i}" for i in mentioning_these_users]
        mentioning_these_users = " OR ".join(mentioning_these_users)
        new_search_term += f" ({mentioning_these_users}) "

    if none_of_these_words:
        if not isinstance(none_of_these_words, list):
            none_of_these_words = [none_of_these_words]

        none_of_these_words = ",".join(none_of_these_words)
        new_search_term += f" -{none_of_these_words} "

    if language:
        new_search_term += f" lang:{language} "

    if not include_replies:
        new_search_term += " -filter:replies "
    elif include_replies and only_replies:
        new_search_term += " filter:replies "

    if not include_links:
        new_search_term += " -filter:links "
    elif include_links and only_links:
        new_search_term += " filter:links "

    if minimum_likes:
        new_search_term += f" min_faves:{minimum_likes} "

    if minimum_replies:
        new_search_term += f" min_replies:{minimum_replies} "

    if minimum_reposts:
        new_search_term += f" min_retweets:{minimum_reposts} "

    if from_date:
        if isinstance(from_date, (datetime.datetime, datetime.date)):
            from_date = from_date.strftime(date_format)
        elif isinstance(from_date, str):
            from_date = parse_time(from_date).strftime(date_format)
        new_search_term += f" since:{from_date} "

    if to_date:
        if isinstance(to_date, (datetime.datetime, datetime.date)):
            to_date = to_date.strftime(date_format)
        elif isinstance(to_date, str):
            to_date = parse_time(to_date).strftime(date_format)
        new_search_term += f" until:{to_date} "

    return new_search_term
