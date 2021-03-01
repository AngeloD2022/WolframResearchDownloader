
WR_ALIAS = "https://d2sm7pvcpl7kby.cloudfront.net/aliases.json"

WR_CDN = "https://files.wolframcdn.com/pub/RE/Mathematica/"

pattern = r"M-(OSX|WIN)?-([A-Z]+)-([0-9]+\.+[0-9]+\.[0-9])"
# Digest -> From b64 -> to hex -> that's the url parameter.
