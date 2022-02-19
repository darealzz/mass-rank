import json

class Data:
    @staticmethod
    async def get_data(key):
        with open('./dumps.json', 'r') as f:
            try:
                return json.load(f)[key]
            except:
                return None

    @staticmethod
    async def dump_data(key, value):

        with open('./dumps.json', 'r') as f:
            data = json.load(f)

        with open('./dumps.json', 'w') as f:
            data[key] = f"{value}"
            json.dump(data, f, indent=4)
