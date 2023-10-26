import redis

# Because I don't using Windows machine - I don't have to explicitly received the ip address
r = redis.Redis()

r.set("fname", "Noaa")

name_val = r.get("fname")

print(name_val)