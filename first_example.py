import redis

# Because I don't using Windows machine - I don't have to explicitly received the ip address
r = redis.Redis()

r.set("fname", "Noaa")

name_bytes = r.get("fname")

name = name_bytes.decode('utf-8')

msg = f"My name is {name}"

print(msg)