import requests


url = "http://localhost:11434/api/embed"

list_of_pets = ["dog", "cat", "hamster", "rabbit", "parrot", "goldfish", "turtle", "ferret", "guinea pig", "chinchilla", "hedgehog", "sugar glider", "tarantula", "snake", "lizard", "frog", "newt", "axolotl", "hermit crab", "ant farm"]
list_of_wild_animals = ["lion", "tiger", "bear", "elephant", "giraffe", "zebra", "monkey", "panda", "koala", "kangaroo", "hippopotamus", "rhinoceros", "crocodile", "alligator", "leopard", "cheetah", "wolf", "fox", "deer", "moose"]

def embed_text(text, dimensions=1024):
    data = {
        "model": "granite4.1:3b",
        "input": text,
        "dimensions": dimensions # default is 2560 for granite4.1:3b
    }

    response = requests.post(url, json=data)

    print("response status code: ", response.status_code)
    if response.status_code == 200:
        return response.json()['embeddings'][0]
    else:
        return "Error:", text, response.status_code

if __name__ == "__main__":
    for pet in list_of_pets:
        print(embed_text(pet))