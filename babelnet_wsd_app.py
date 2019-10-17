
from wsd import WSD
import os
BABELNET_TOKEN = os.environ["BABELNET_TOKEN"]

WSD("wsd.json", BABELNET_TOKEN, "stop_words", "EXTENDED")