def escape_url(url):
    try:
        import urllib.parse
    except ImportError:
        # 2.7
        return urllib.quote_plus(url)
    else:
        # 3.5
        return urllib.parse.quote_plus(url)
