# Web semantic project

# Installation

1. Clone this repos and create a python virtual environment
```bash
git clone https://github.com/charlyalizadeh/ESILV_WebSemantic
cd ESILV_WebSemantic/
python3 -m venv .venv
source .venv/bin/avtivate # or for Windows .venv/Scripts/activate.bat
```
2. Install the dependencies
```bash
pip install requirements.txt
```

Next you need to setup Neo4j with the neosemantic plugin. If you have docker running using `python setup.py --docker` should do the work for you.
If you want to setup Neo4j manually see the following instructions.

## Setup Neo4j manually

### Docker

1. Pull the Neo4j images
```bash
docker pull neo4j:latest
```
2. Create a container
```bash
docker run --name neo4j_websem -p 7474:7474 -p 7687:7687 neo4j
```
3. Download Neosemantic, you can find the link [here](https://github.com/neo4j-labs/neosemantics/releases) or you can use `wget` to download it directly (at the time of writing the latest version is 4.2.0.0, you may want to update the link)
```bash
wget https://github.com/neo4j-labs/neosemantics/releases/download/4.2.0.0/neosemantics-4.2.0.0.jar
```
4. Copy neosemantics in the plugins folder
```bash
docker cp neosemantics-4.2.0.0.jar neo4j_websem:/var/lib/neo4j/plugins
```
5. Then modify the container neo4j configuration file by running the following commands
```
docker cp neo4j_websem:/var/lib/neo4j/conf/neo4j.conf ./
echo dbms.unmanaged_extension_classes=n10s.endpoint=/rdf >> neo4j.conf
docker cp neo4j.conf neo4j_websem:/var/lib/neo4j/conf/neo4j.conf
```

### Local installation

1. Download Neo4j, different downloads can be found [here](https://neo4j.com/download-center/)
2. Download Neosemantic, you can find the link [here](https://github.com/neo4j-labs/neosemantics/releases) or you can use `wget` to download it directly (at the time of writing the latest version is 4.2.0.0, you may want to update the link)
```bash
wget https://github.com/neo4j-labs/neosemantics/releases/download/4.2.0.0/neosemantics-4.2.0.0.jar
```
3. Copy neosemantics in the plugins folder
```bash
cp neosemantics-4.2.0.0.jar <NEO_HOME>/plugins/
```
4. Add the following line to `<NEO_HOME>/conf/neo4j.conf`
```
dbms.unmanaged_extension_classes=n10s.endpoint=/rdf
```
