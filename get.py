import urllib.request, json 
with urllib.request.urlopen("http://at04w.otf.cloud/listedata?collection=meunier") as url:
    data = json.loads(url.read().decode())
    print(data)
