### Metadata serveur

**Pour construire l'image**
```Bash
sudo docker build --network host -t <tag> .
```

**Pour lancer le metadata serveur**
```Bash
sudo docker run -d --name metadata_server -p80:8080 <tag>
```
