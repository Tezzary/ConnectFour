import requests
import utils

response = requests.get("https://connect4.gamesolver.org/solve?pos=4")
print(response.text)
                        