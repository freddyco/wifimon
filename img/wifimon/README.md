# WIFIMON

~~~
El proyecto WIFIMON realiza consultas de variables SNMP, por el momento, a controladores WLC.
El proyecto toma dos archivos de input {data_oids.json, data_wlc.json} ubicados en /config_files.
El proyecto viene incorporado con Mibs compilados {ubicados en mib_files}  para que puedan traducirce las variables mibs consultadas.
El proyecto viene incorporado con Mibs en plano {ubicados en mib_files/sources} que fueron utilizadas para obtener los Mibs compilados.
El proyecto se puede ejecutar desde ambiente Docker mediante variables de entorno (e internamente se pasan estas variables a argumentos python).
El proyecto se puede ejecutar directamente desde python usando argumentos.

~~~



## 1) Compilar MIBs a archivos python 

_Se debe crear un nuevo ambiente Conda y principalmente tener instalado dos modulos:_
- pysnmp  4.4.12
- pysmi   0.3.4

_Nota: Estas versiones no funcionan para el codigo de Wifimon, sólo es para compilar._

_El pip list en este ambiente (compilación) es:_



                        (wifimon_v2) D:\img>pip list
                        Package         Version
                        --------------- -----------
                        attrs           24.2.0
                        jsonschema      4.17.3
                        netaddr         0.8.0
                        numpy           1.26.3
                        pandas          2.0.0
                        pip             24.2
                        ply             3.11
                        pyasn1          0.6.0
                        pyasyncore      1.0.3
                        pycryptodomex   3.20.0
                        pyrsistent      0.20.0
                        pysmi           0.3.4
                        pysnmp          4.4.12
                        python-dateutil 2.9.0.post0
                        pytz            2024.1
                        setuptools      72.1.0
                        six             1.16.0
                        tzdata          2024.1
                        wheel           0.43.0

               

- Las MIB fuentes usadas son:


                    | Nombre                    | LAST-UPDATED              |
                    | ---                       | ---                       |
                    |  BRIDGE-MIB               |No hay dato
                    |  CISCO-LWAPP-AP-MIB       |201809300000Z
                    |  CISCO-LWAPP-DOT11-MIB    |201005060000Z
                    |  CISCO-LWAPP-RF-MIB       |201111010000Z
                    |  CISCO-LWAPP-SI-MIB       |201505180000Z
                    |  CISCO-LWAPP-TC-MIB       |201109130000Z
                    |  CISCO-LWAPP-WLAN-MIB     |201504230000Z
                    |  CISCO-SMI                |201601150000Z
                    |  CISCO-TC                 |201506090000Z
                    |  ENTITY-MIB               |201304050000Z
                    |  IANA-ENTITY-MIB          |201507160000Z
                    |  IANAifType-MIB           |201703300000Z
                    |  INET-ADDRESS-MIB         |200502040000Z
                    |  RFC-1212                 |No hay dato
                    |  RFC-1215                 |No hay dato
                    |  RFC1155-SMI              |No hay dato
                    |  RFC1213-MIB              |No hay dato
                    |  SNMP-FRAMEWORK-MIB       |200210140000Z
                    |  SNMPv2-CONF              |No hay dato
                    |  SNMPv2-MIB               |200210160000Z
                    |  SNMPv2-SMI               |No hay dato
                    |  SNMPv2-TC                |No hay dato
                    |  UUID-TC-MIB              |201304050000Z
                    |  AIRESPACE-WIRELESS-MIB   |201002090000Z
                    |  AIRESPACE-REF-MIB        |200512190000Z


- Al compilar CISCO-LWAPP-SI-MIB, se compilan/generan todos los Mib que son dependencia y se guarda en PySNMP Configuration:

                    | Archivos compilados           |
                    | ---                           |
                    |  CISCO-LWAPP-AP-MIB.py
                    |  CISCO-LWAPP-DOT11-MIB.py
                    |  CISCO-LWAPP-RF-MIB.py
                    |  CISCO-LWAPP-SI-MIB.py
                    |  CISCO-LWAPP-TC-MIB.py
                    |  CISCO-LWAPP-WLAN-MIB.py
                    |  CISCO-SMI.py
                    |  CISCO-TC.py
                    |  ENTITY-MIB.py
                    |  IANA-ENTITY-MIB.py
                    |  IANAifType-MIB.py
                    |  UUID-TC-MIB.py         

```
Notas:
- Se debe usar script {compile_mib.py}
- Se deja de respaldo el otro compilador {compile_pysnmi.py} pero no me dio resultado al compilar.
- Es posible compilar {CISCO-LWAPP-DOT11-MIB, CISCO-TC, CISCO-LWAPP-RF-MIB, CISCO-LWAPP-AP-MIB}, pero todos derán compilados ya incluidos en CISCO-LWAPP-SI-MIB. 
- Todos los compilados que se generan en PySNMP Configuration se deben copiar al proyecto en /mib_files
```

- Al compilar AIRESPACE-WIRELESS-MIB, se compilan/generan todos los Mib que son dependencia y se guarda en PySNMP Configuration:

                    | Archivos compilados           |
                    | ---                           |
                    |  AIRESPACE-REF-MIB.py
                    |  AIRESPACE-WIRELESS-MIB.py


## Correcciones a Mib

Al compilar CISCO-LWAPP-SI-MIB (2017 o 2018) genera errores del tipo: 
```
pyasn1.error.PyAsn1Error: Duplicate name byte\n']caused by <class 'pyasn1.error.PyAsn1Error'>: Duplicate name byte
```
Esto es provocado porque el Mib tiene asociado mismo nombre 'byte' a varios valores, y su corrección es la siguiente por ahora:

```
cLSiD11IdrTrapDeviceList OBJECT-TYPE
    SYNTAX          BITS {
                        byte0(0),
                        byte1(1),
                        byte2(2),
                        byte3(3),
                        byte4(4),
                        byte5(5),
                        
                        ETC...

```

## 2) Ejecutando WIFIMON

### 2.1) Archivos de input 

- WIFIMON tiene dos archivos de input (en /config_files) :

    oids_bsnAPEntry.json -> se tiene todas las variables OID a consultar de esta tabla.

    data_wlc.json -> se tiene todas las IPs de los WLC a consultar.


### 2.1.1) Preparando SQLite (en caso de usar) 

- WIFIMON tiene dos archivos de input (en /config_files) :

    model_diagram.mwb (worksbench) -> Exportar diagrama en script -> esto generará el script en formato mysql, hay q convertirlo en formato SQLite (usando chatGPT u otro). El archivo script SQLite se llama: model_sqlite.sql
    
    
    model_sqlite.sql -> se debe mapear este script a clases SQLAlchemy, usando sqlacodegen:

```

    (wifimon) D:\img>sqlite3 wifimon.db < wifimon/database/model_sqlite3.sql

    (wifimon) D:\img>sqlacodegen sqlite:///wifimon.db --outfile wifimon/mapTables2.py 

```






### 2.2) Ejecutando WIFIMON sin Docker:

con debug y salida a csv:

```

/wifimon/python.exe d:/img/wifimon/app.py -snmp_c {comunidad_string} [-nms_token {token_string}] -write_csv -debug 

/ifimon/python.exe d:/img/wifimon/app.py -snmp_c {comunidad_snmp} -presenters {syslog/csv/console} -syslog_h {host_syslog} [-nms_token {token_string}] -debug 



OBS: 
 - parámetro nms_token es opcional


```

### 2.3) Ejecutando WIFIMON con Docker:


En Docker (dentro de directorio /img/):

Previamente:
- debe existir archivo Dockerfile 
- debe existir requirements.txt en /img/wifimon/wifimon/

a) Crear imagen docker:
```
docker build -t wifimon_img .
```

b) Ejecutar Contenedor usando run (se puede quitar debug y write_csv):
```
(version 1)
docker run -it --rm --name wifimon_app -v "%cd%"/output:/wifimon/output  -e snmp_community={comunidad} -e debug=true -e write_csv=true -e TZ=America/Santiago -e nms_token={token} wifimon_img

(version 2, sin NMS, con Syslog)

docker run -it --rm --name wifimon_app -v "%cd%"/output:/wifimon/output  -e snmp_community={comunidad}  -e presenters=syslog -e syslog_host={ip_syslog} -e TZ=America/Santiago wifimon_img
```

c) Ejecutar Contenedor usando compose:

```
docker compose up
```


## 3) Subiendo a GIT:

Por si se parte de nuevo repositorio:

```
\img\wifimon>git init

\img\wifimon>git add .
\img\wifimon>git commit -m "Primer commit"

```


se genera nuevo branch (y se salta a esta nueva rama):
```
\img\wifimon>git branch update_2

\img\wifimon>git checkout update_2
```

se añade los archivos a la nueva rama

```
\img\wifimon>git add .
```

se genera commit
```
\img\wifimon>git commit -m "se genera vesion 1.4.1 de wifimon"
```

se valida que repositorio local esté conectado a repositorio remoto
```
\img\wifimon>git remote -v
```

para eliminar enlace a repositorio remoto:
```
git remote remove origin
```

OBS: si no sale nada se debe agregar enlace:
```
para Git UC

git remote add origin https://git.uc.cl/srs/docker-images/wifimon.git
git remote set-url origin https://freddy.condori:{token}git.uc.cl/srs/docker-images/wifimon.git

para Git Hub
\img\wifimon>git remote add origin https://github.com/usuario/repo.git


```


OBS: 
- El token debe ser generador desde git/User/Preference/Access Token
- El Sync con los cambios se realiza desde vscode
Si no funciona en vscode, ejecutar desde consola:

```

git push origin update_7
```

## 4) Buscando devices en NMS

Para buscar un device_id/switch en NMS se realiza copiando en browser el link de LibreNMS. Esto para buscar cuales son los switches que tienen description duplicados
Los cuales son arrojados en csv duplicados

```

https://nms.noc.uc.cl/device/{device_id}

Ejemplo:

https://nms.noc.uc.cl/device/4167
```


## Versiones 📌

Version "Update 8".  [link a repositorio](https://git.uc.cl/srs/docker-images/wifimon).


```
Detalles:

- Se agrega filtro de busqueda para APs que empiezan por "CC0" 20241003

```

