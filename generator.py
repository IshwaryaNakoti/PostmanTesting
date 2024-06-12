# gen_exp = (x * x for x in range(3))
# print(next(gen_exp))  # Output: 0
# print(next(gen_exp))  # Output: 1
# print(next(gen_exp))  # Output: 4

class User():
    def __init__(self, name, username):
        self.name = name
        self.username = username

import json
your_json = {"name":"Ishu", "username":"Nakoti"}
# j = json.loads(your_json)
u = User(**your_json)

print(u.name)
