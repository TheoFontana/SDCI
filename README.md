<div align="center">
  <a href="https://www.insa-toulouse.fr/">
    <img src="./report/asset/logo-insa.jpg" alt="logo" width="300px" >
  </a>
  <br/>
  <br/>
  <h3 align="center"> Software Defined Communication Infrastructure </h3>
  <h4 align="center"> Systèmes distribués et big data - INSA Toulouse - 2023 </h3>
  <a href="https://www.github.com/TheoFontana">Théo Fontana</a>
  <span>, </span>
  <a href="https://www.github.com/jodorganistaca">Jose Organista</a>
</div>

<!-- ABOUT THE PROJECT -->
## Presentation du Projet
Ce projet est réalisé dans le cadre de la mineure SDCI en dernière année de l'école d'ingénieur INSA en spécialité systèmes distribués et big data.

## Objectifs

* Déployer dynamiquement et de façon transparente des fonctions de réseau virtuelles (VNF)
permettant de répondre aux besoins fonctionnels et/ou non fonctionnels d’applications distribuées relevant d’une activité de l’Internet des objets (IoT)
en appliquant les concepts et techniques relevant de la virtualisation de fonctions de réseau (NFV) et des réseaux pilotables par le logiciel (SDN)
* Développer une approche de gestion autonome de la mise en œuvre des VNF ciblées via le concept de l’Autonomic Computing (AC)

## Activité IoT ciblée

Nous ciblons une activité de supervision/intervention à distance sur différentes zones dotées de capteurs / actionneurs, par le biais d’applications

![](./report/asset/IoT_environnement.png)

En cas d'incident dans une zone du trafic supplémentaire est généré par ses capteurs / actionneurs.
Ceci peut entrainer la saturation de la gateway intermédiaire (GI) générant ainsi une baisse de performances incompatible avec les besoins en QoS des applications

Une phase d'adaptation est alors nécessaire pour rétablir les performances. Plusieurs stratégies peuvent être adoptées :
* Déployer une seconde gateway sous forme de VNF et rediriger le trafic provenant de la zone 1 (ou des zones 2 et 3) vers cette gateway.
* Déployer une VNF d'ordonnancement différencié priorisant le trafic issu de GF1.
* Supprimer les flux de données en provenance de la zone 2 et 3.
* Déployer d'un loadbalancer sous forme de VNF.

### Vision IT de l'activité ciblée

Hypothèse sur l'infrastructure IT 

* GI, GF et DC sont connectés via un réseau grande distance (WAN) géré par un opérateur dont la portée d’action inclut : les nœuds internes du réseau (switch), les nœuds midlleware (GI et GF) et le DC
* Un orchestrateur de VNF (VNF-ORCH) est connecté au WAN : il permet de déployer des VNF sur le DC et de gérer leur cycle de vie.
* Le WAN est doté de capacités SDN :
  * Ses nœuds internes sont des switch SDN programmables via Open Flow
  * Il inclut un contrôleur SDN interagissant avec les switch SDN via Open Flow

![](./report/asset/IT_vision.png)

### Plateforme et outils mis à disposition 

* Plateforme d’émulation de réseau : [ContainerNet](https://github.com/containernet/containernet)
* Contrôleur SDN : [RYU](https://ryu-sdn.org)
  * [Documentation API](https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html)
* MANO standardisé ETSI NFV : [OSM](https://osm.etsi.org)
  * [Documentation API vim-emu](https://github.com/containernet/vim-emu/wiki/APIs)
* Middleware IoT/M2M en NodeJS (see [Middelware](https://github.com/TheoFontana/SDCI/tree/main/middleware))

### Travail demandé

Mettre en place l'adaptation requise lorsque la gateway intermédiaire est saturée, suivant le cadre de l’Autonomic Computing

## Use cases étudiées

Notre groupe avait pour mission de monitorer la gateway intermédiaire pour surveiller sa charge à partir de métriques systèmes telles que la charge du CPU.

![](report/asset/monitoring_strategy.png)

Nous devions ensuite, en cas de dégradation des performances, déployer une nouvelle gateway et rediriger le trafic en provenance de la zone 1 vers cette dernière. Le trafic de la zone 2 et 3 continuant d'utiliser la gateway initiale.
![](report/asset/adaptation_stretegy.png)

## Conception des solutions

### Composants en jeu
Nous disposons d'un Mano qui nous expose un service permettant de déployer et d'arrêter des VNF dans un datacenter via des requêtes sur son API REST.

Nous avons également un contrôleur SDN qui nous permet de mettre à jour les tables SDN des différents switch de notre réseau via son API REST.

Les interactions entre notre general controller, le MANO et le SND controller sont résumés dans le diagramme de structure composite suivant

![](./report/asset/composition.png)
*Diagramme de structure composite*
### Monitoring

Pour le monitoring nous proposons de déployer la VNF de monitoring au démarage du general controller. Une fois que celui ci à eu la confirmation que la VNF est correctement déployé, il l'interooge periodiquement pour recupérer les informations système de la gateway intermediaire. Il verifie à chaque iteration que le système n'est pas en surcharge.

![](./report/asset/monitoring_sequence.png)
*Diagramme de séquence du monitoring*
### Adaptation
Pour l'adaptation, notre general controller devra demander le déploiment d'une nouvelle gateway dans le datacenter via l'API du MANO. Si ce deploiment s'est bien déroulé, il demande la redirection du trafic de la zone 1 en direction de cette VNF grace à l'API du controlleur SDN.

![](./report/asset/adapation_sequence.png)
*Diagramme de séquence de l'adpatation*

## Choix d'implémentation
### Topologie déployée
Nous avons choisi de déployer le réseau suivant
![](report/asset/general_topology.png)

Le réseau bleu est le réseau émulé mininet. Nous avons choisi de représenter les différentes zones avec un switch simulant un LAN. 

Le réseau vert représente le réseau VLAN Docker reliant tous nos containers. Il est utilisé pour assurer la communication entre : 
* les nœuds middleware et le metadata serveur
* le GC, le Mano, le contrôleur SDN et les VNFs 

Pour le déploiement des différents nœuds middleware, nous avons créé un unique Dockerfile permettant de créer l'image associée au nœud. 
Celui-ci récupère d'identifiant de l'instance à déployer en variable d'environnement et lance un script de démarrage spécifique en fonction du type d'instance lorsque le container est lancé.

```Dockerfile
FROM ubuntu:trusty

ARG SCRIPT
ARG NODE_VERSION=14
ENV INSTANCE_ID=''
...
ADD $SCRIPT .
...
ENTRYPOINT sh /componnent/$SCRIPT && /bin/sh
```
*Extrait du  [Dockerfile](./nodes/Dockerfile)*

Le scrpit de démarrage est chargé de récupérer la configuration de l'instance sur le matadata serveur pour pouvoir lancer le service avec les bons paramètres.

```bash
curl -o conf.json metadata_server/$INSTANCE_ID

LOCAL_NAME=`cat conf.json | jq '.local_name'`
LOCAL_PORT=`cat conf.json | jq -r '.local_port'`
LOCAL_IP=`cat conf.json | jq '.local_ip'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`

curl -LO $FILE_URL
node server.js --local_ip $LOCAL_IP --local_port $LOCAL_PORT --local_name $LOCAL_NAME
```
*Exemple de script de démarrage pour le serveur [start_server.sh](nodes/start_server.sh)*
### Metadata serveur
Nous avons réalisé le metadata serveur en Node.js. Il renvoie la configuration de l'instance à déployer suite à une requête ```GET``` sur l'identifiant de l'instance souhaitée.

```js
app.get('/:id', function(req, res) {
  var id = req.params.id;
    var conf_instance = config[id];
    if (conf_instance)
        res.status(E_OK).send(JSON.stringify(conf_instance));
    else
        res.sendStatus(E_NOT_FOUND);
});
```
*Extrait de [metadata_server.js](./metadata_server/metadata_server.js)*

L'ensemble des configurations est stocké dans un fichier général de configuration json.

```json
{
...
"gwf_1": {
        "local_ip": "10.1.0.11",
        "local_port": 8282,
        "local_name": "gwf_1",
        "remote_ip": "10.1.0.10",
        "remote_port": 8181,
        "remote_name": "gwi",
        "file_URL":"https://homepages.laas.fr/smedjiah/tmp/mw/gateway.js"
    },
...
}
```
*Extarit de  [config.json](./metadata_server/config.json)*

### General Controller

Nous avons choisi de ne pas utiliser le squelette de general controller fourni, mais de développer nous-mêmes un prototype plus simple en Python afin de nous faciliter le  développement et les tests.

### Monitoring
Notre stratégie de monitoring est pour l'instant assez simple. Lorsque notre VNF reçoit une requête ```GET``` de la part du general controller, elle interroge la gateway sur son endpoint ```/health``` et retourne la réponse reçue au GC. Cette stratégie nous permet de déplacer le traitement de la réponse au niveau du GC celui-ci peut donc choisir à quel rythme monitorer, ce qui peut potentiellement réduire la charge sur la gateway.

```JS
app.get('/monitor', function(req, res) {
    request({method: 'GET', uri: `http://10.1.0.10:8181/health`}, (error, response, body) => {
        if (!error && response.statusCode == 200){
            res.send(body);
        } else {
            res.send(error);
        }
    });
});
```
*Extarit de  [monitor.js](./VNF/Monitoring/monitor.js)*

Pour deployer la VNF, nous utilsons l'API REST de vim-emu 
```Python
def start_monitoring():
    # URL to add new vnf
    url = 'http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitor'
    headers = {'Content-type': 'application/json'}
    d = {"image":"vnf_monitor:0.2", "network":"(id=vnf_monitor,ip=10.1.0.100/24)"}
    r = requests.put(url, headers = headers, data = json.dumps(d))
    return r.status_code, r.json()
```
*Extarit de  [controller.py](./GeneralController/controller.py)*

Nous avons choisi de baser notre monitoring sur la métrique ```currentLoadSystem``` car c'est celle qui variait le plus rapidement lorsque nous simulions une charge sur la gateway durant nos tests. Lorque celle-ci dépasse le seuil fixé, nous devons déployer notre VNF d'adaptation.

###  Adaptation
La première étape de l'adaptation est de déployer une nouvelle gateway intermédiaire dans le datacenter en utilisant l'API REST de vim-emu. L'image de la gateway intermédiaire précédemment construite a dû être légèrement modifiée pour qu'elle convienne aux exigences de vim-emu :
* Le serveur node.js doit tourner en background
* Les srcipts de démarage et d'arrêt de la VNF doivent être passés en variable d'environnement dans le Dockerfile.

Nous devons ensuite rediriger le trafic de la gateway final de la zone 1 en direction de la gateway intermédiaire vers notre VNF.

Nous avons pris la décision d'identité ces flux avec uniquement les adresses IP source et destination. En effet, le seul trafic circulant sur notre réseau entre ces instances est le trafic applicatif que nous souhaitons rediriger. Si ce n'était pas le cas, nous aurions également dû utiliser les numéros de port pour identifier ces flux.

Nous devons donc :
* modifier l'addresse IP destination des paquet provennat de ```GF1``` en direction de ```GI``` *(aller)*
* modifier d'addresse IP srouce des paquets provennant de la ```GI_VNF``` en direction en direction de ```GF1``` *(retour)*

Cela est réalisé en ajoutant des *flow* dans la table SDN du switch 2 à l'aide de l'API de controller SDN  de la façon suivante (pour l'aller)
```Json
curl -X POST -d '{
  "dpid": 2,
    "table_id":0,
    "priority":11111,
    "match":{
      "nw_src": "10.1.0.11",
        "nw_dst": "10.1.0.10",
        "dl_type": "2048",

    },
    "actions":[
      {
        "type": "SET_FIELD",
            "field": "ipv4_dst",
            "value": "10.1.0.60"
        },
        {
          "type": "OUTPUT",
            "port": "NORMAL"
        }
    ]
 }' http://localhost:8080/stats/flowentry/add
```
*Extrait de  [redirect_gwi_to_vnf.sh](./GeneralController/redirect_gwi_to_vnf.sh)*
## Scénario de démonstration 

Pour notre démonstration, nous souhaitons 

1. Lancer notre topologie avec mininet
   ![](./report/asset/mininet.gif)
2. Tester la communication entre la gateway finale 1 et la gateway intermédiaire
   ![](./report/asset/ping.gif)
3. Démarrer notre general controller et voir que le monitoring se lance.
   ![](./report/asset/controller.gif)
4. Générer un fort trafic depuis la gateway finale 1 vers la gateway intermédiaire
5. Observer que le general controller détecte une dégradation des performances sur la gateway et lance une nouvelle gateway intermédiaire dans le data center.
6. Observer que le trafic généré est redirigé et n'arrive plus à la gateway intermédiaire, mais à la VNF.
7. Vérifier que ces opérations ont été transparentes au niveau applicatif.
   ![](./report/asset/final_test.gif)
   *démo pour les points 4, 5, 6 et 7*
## Axes d'améliorations

* Actuellement, lors de la redirection du trafic, le trafic de *retour* entre la VNF gateway intermédiaire et la gateway finale est addresé à la gateway intermédiaire au niveau MAC. Nous n'avons pas pu debuger ce problème qui fait que la GWI reste saturée même après la redirection de trafic effectuée.
* Il nous faudrait ensuite ajouter une stratégie pour revenir au cas nominal en supprimant la VNF déployée une fois que le trafic redevient normal.
* Il pourrait également être intéressant de monitorer la VNF déployer pour s'assurer que celle-ci ne soit pas non plus en surcharge et possiblement déployer une nouvelle gateway intermédiaire avec un load balancer en cas de problème.

## Conclusion

Ce projet a été l'occasion de nous familiariser avec les concepts de l'autonomus computing dans un contexte IoT où les applications ont des besoins en QoS et génèrent un trafic variable. 
Nous avons pu développer et déployer dynamiquement des VNFs en charge de surveiller l'état d'instances sur le réseau et d'assurer des performances suffisantes aux applications.
Grâce à SDN, nous avons pu dynamiquement modifier le routage au sein de notre réseau de manière transparente pour les applications.

Nous aurions cependant aimé pouvoir approfondir la partie SDN pour pouvoir définir plus finement les flux de communications et aller plus loin dans les stratégies mise en œuvre pour s'adapter à la dégradation de l'état du middleware.
