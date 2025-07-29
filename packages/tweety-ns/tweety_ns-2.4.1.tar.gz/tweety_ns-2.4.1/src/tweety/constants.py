
class ProxyType:
    SOCKS4 = 1
    SOCKS5 = 2
    HTTP = 3

class HomeTimelineTypes:
    FOR_YOU = "HomeTimeline"
    FOLLOWING = "HomeLatestTimeline"

class InboxPageTypes:
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"

class MediaTypes:
    VIDEO = "video"
    GIF = "animated_gif"
    IMAGE = PHOTO = "photo"


class InboxCallType:
    AUDIO = "AUDIO_ONLY"
    VIDEO = "AUDIO_AND_VIDEO"

class UploadTypes:
    TWEET_IMAGE = "tweet_image"
    DM_IMAGE = "dm_image"
    BANNER_IMAGE = "banner_image"

REQUEST_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
REQUEST_USER_AGENT_CH = '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"'
REQUEST_PLATFORMS = ['Linux']
DEFAULT_BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
AUTH_ACTION_REQUIRED_KEYS = ("LoginTwoFactorAuthChallenge", "LoginAcid", "LoginEnterAlternateIdentifierSubtask")
LIKES_ARE_PRIVATE_NOW_WARNING = "User Likes are now private , you can only see the Likes of authenticated User"

LOGIN_SITE_KEY = "2F4F0B28-BC94-4271-8AD7-A51662E3C91C"
GENERAL_SITE_KEY = "0152B4EB-D2DC-460A-89A1-629838B529C9"

ITERABLE_TYPES = (list, tuple)
# GENERAL_SITE_KEY = "50706BFE-942C-4EEC-B9AD-03F7CD268FB1"


# JA3_FINGERPRINTS = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,51-18-10-5-35-0-45-65037-65281-23-43-11-17513-13-27-16,25497-29-23-24,0"
JA3_FINGERPRINTS = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,13-23-18-27-51-0-45-5-17513-65281-65037-43-10-16-35-11,25497-29-23-24,0"
AKAMAI_FINGERPRINTS = "1:65536;2:0;4:6291456;6:262144|15663105|0|m,a,s,p"
HTTP2_SETTINGS = "1:65536;2:0;4:6291456;6:262144"
TLS_OPTIONS = {
    "tls_signature_algorithms": [
        "ecdsa_secp256r1_sha256",
        "rsa_pss_rsae_sha256",
        "rsa_pkcs1_sha256",
        "ecdsa_secp384r1_sha384",
        "rsa_pss_rsae_sha384",
        "rsa_pkcs1_sha384",
        "rsa_pss_rsae_sha512",
        "rsa_pkcs1_sha512"
    ],
    "tls_cert_compression": "brotli",
    "tls_grease": True,
}

# Constants for backward compatibility
PROXY_TYPE_SOCKS4 = SOCKS4 = ProxyType.SOCKS4
PROXY_TYPE_SOCKS5 = SOCKS5 = ProxyType.SOCKS5
PROXY_TYPE_HTTP = HTTP = ProxyType.HTTP
HOME_TIMELINE_TYPE_FOR_YOU = HomeTimelineTypes.FOR_YOU
HOME_TIMELINE_TYPE_FOLLOWING = HomeTimelineTypes.FOLLOWING
INBOX_PAGE_TYPE_TRUSTED = InboxPageTypes.TRUSTED
INBOX_PAGE_TYPE_UNTRUSTED = InboxPageTypes.UNTRUSTED
INBOX_PAGE_TYPES = (InboxPageTypes.TRUSTED, InboxPageTypes.UNTRUSTED)
MEDIA_TYPE_VIDEO = MediaTypes.VIDEO
MEDIA_TYPE_GIF = MediaTypes.GIF
MEDIA_TYPE_IMAGE = MEDIA_TYPE_PHOTO = MediaTypes.IMAGE
UPLOAD_TYPE_TWEET_IMAGE = UploadTypes.TWEET_IMAGE
