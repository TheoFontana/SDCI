<div align="center">
  <a href="https://jodorganistaca/exploratory_analysis_dataviz">
    <img src="https://www.insa-toulouse.fr/skins/Insa-v2/resources/img/logo-insa.jpg" alt="Logo" >
  </a>
  <br/>
  <br/>
  <h3 align="center"> Software Defined Communication Infrastructure </h3>
  <h4 align="center"> Distribued System and Big Data - INSA Toulouse - 2022 </h3>
  <a href="https://www.github.com/TheoFontana">Théo Fontana</a>
  <span>, </span>
  <a href="https://www.github.com/jodorganistaca">Jose Organista</a>
</div>

<!-- ABOUT THE PROJECT -->
## Presentation du Projet

### Objectifs 

* Déployer dynamiquement et de façon transparente des fonctions de réseau virtuelles (VNF) 
  * permettant de répondre aux besoins fonctionnels et/ou non fonctionnels d’applications distribuées relevant d’une activité de l’Internet des objets (IoT)
  * en appliquant les concepts et techniques relevant de la virtualisation de fonctions de réseau (NFV) et des réseaux pilotables par le logiciel (SDN)
* Développer une approche de gestion autonome de la mise en œuvre des VNF ciblées via le concept de l’Autonomic Computing (AC)

### Activité IoT ciblée

Activité de supervision/intervention à distance sur differentes zones dotées de capteurs / actionneurs, par le biais d’applications

![](./report/asset/IoT_environnement.png)

En cas d'incident dans une zone du trafic supplémentaore est généré par ses capteurs / actionneurs.
Ceci peut entrainer la saturation de la gateway intermediaire (GI) génerant ainsi une baisse de performances incompatible avec les besoins en QoS des applications.

Une phase d'adapation est alors necessaire pour retablir les performances. Plusieur stratégies peuvent être adopté :
* Déployer une seconde gateway sous forme de VNF et rediriger le trafaic provenant de la zone 1 (ou des zone 2 et 3) vers cette gateway.
* Déployer d'une VNF d'ordonnancement différencié priorisant le trafic issu de GF1.
* Supprimmer les flux de données en provenance de la zone 2 et 3.
* Déployer d'un loadbalancer sous forme de VNF.

### Vision IT de l'activité ciblée

Hypotèse sur l'infrastuture IT 

* GI, GF et DC sont connectés via un réseau grande distance (WAN) géré par un opérateur dont la portée d’action inclut : les noeuds internes du réseau (switch), les noeuds MW (GI et GF) et le DC
* Un orchestrateur de VNF (VNF-ORCH) est connecté au WAN : il permet de déployer des VNF sur le DC et de gérer leur cycle de vie.
* Le WAN est doté de capacités SDN :
  * Ses noeuds internes sont des switch SDN programmables via Open Flow
  * Il inclut un contrôleur SDN interagissant avec les switch SDN via Open Flow

![](./report/asset/IT_vision.png)

### Plateforme et outils mis à disposition 

* Plateforme d’émulation de réseau : [ContainerNet](https://github.com/containernet/containernet)
* Controlleur SDN : [RYU](https://ryu-sdn.org)
* MANO standardisé ETSI NFV : [OSM](https://osm.etsi.org)
* Middleware IoT/M2M en NodeJS (see [Middelware](https://github.com/TheoFontana/SDCI/tree/main/middleware))

### Travail demandé

Mettre en place l'adaptation requise lorsque la gateway intermediaire est saturée, suivant le cadre de l’Autonomic Computing