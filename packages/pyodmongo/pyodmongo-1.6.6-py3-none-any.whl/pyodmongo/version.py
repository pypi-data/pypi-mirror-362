import pydantic
import platform
import sys
import pymongo
import motor


VERSION = "1.6.6"

info = {
    "PyODMongo version": VERSION,
    "Pydantic version": pydantic.version.VERSION,
    "Pymongo version": pymongo.__version__,
    "Motor version": motor._version.version,
    "Python version": sys.version,
    "Platform": platform.platform(),
}
response = "\n".join([f"{key}: {value}" for key, value in info.items()])
print(response)
