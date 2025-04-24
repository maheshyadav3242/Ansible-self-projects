import requests
response = requests.get("https://api.github.com/maheshyadav32422/terraform-eks")
if response.ok:
     data =response.json()
       print( data["public_repos"])
