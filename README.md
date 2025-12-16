# Подюков Илья. ФИТ-2-2024 НМ. Методы и инструменты DevOps. ЛР по лекции 10
### helm
- Перед началом работы удаляю старые ресурсы из кластера
```
ilya@erth ~> kubectl get deployments
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-app   5/5     5            5           27m
redis       1/1     1            1           30m
```
```
ilya@erth ~> kubectl delete all --all
pod "flask-app-79b8d5d949-rqz5x" deleted from default namespace
pod "flask-app-79b8d5d949-twbqz" deleted from default namespace
pod "flask-app-79b8d5d949-vjlpq" deleted from default namespace
pod "flask-app-79b8d5d949-vrxlk" deleted from default namespace
pod "flask-app-79b8d5d949-w754q" deleted from default namespace
pod "redis-59bd98c78b-xscfv" deleted from default namespace
service "kubernetes" deleted from default namespace
service "redis" deleted from default namespace
service "service-devops" deleted from default namespace
deployment.apps "flask-app" deleted from default namespace
deployment.apps "redis" deleted from default namespace
```
- Из pacman'а устанавливаю helm и kompose
- Конвертирую docker-compose в ресурсы k8s
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> kompose convert --chart
WARN Restart policy 'unless-stopped' in service prometheus is not supported, convert it to 'always' 
WARN Restart policy 'unless-stopped' in service grafana is not supported, convert it to 'always' 
WARN File don't exist or failed to check if the directory is empty: stat :/var/lib/grafana: no such file or directory 
WARN File don't exist or failed to check if the directory is empty: stat :/prometheus: no such file or directory 
INFO Kubernetes file "docker-compose/templates/blackbox-service.yaml" created 
INFO Kubernetes file "docker-compose/templates/grafana-service.yaml" created 
INFO Kubernetes file "docker-compose/templates/prometheus-service.yaml" created 
INFO Kubernetes file "docker-compose/templates/blackbox-deployment.yaml" created 
INFO Kubernetes file "docker-compose/templates/grafana-deployment.yaml" created 
INFO Kubernetes file "docker-compose/templates/grafana-data-persistentvolumeclaim.yaml" created 
INFO Kubernetes file "docker-compose/templates/grafana-cm0-configmap.yaml" created 
INFO Kubernetes file "docker-compose/templates/prometheus-deployment.yaml" created 
INFO Kubernetes file "docker-compose/templates/prom-data-persistentvolumeclaim.yaml" created 
INFO Kubernetes file "docker-compose/templates/prometheus-cm0-configmap.yaml" created 
INFO chart created in "docker-compose/"
```
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> tree docker-compose
docker-compose
├── Chart.yaml
├── README.md
└── templates
    ├── blackbox-deployment.yaml
    ├── blackbox-service.yaml
    ├── grafana-cm0-configmap.yaml
    ├── grafana-data-persistentvolumeclaim.yaml
    ├── grafana-deployment.yaml
    ├── grafana-service.yaml
    ├── prom-data-persistentvolumeclaim.yaml
    ├── prometheus-cm0-configmap.yaml
    ├── prometheus-deployment.yaml
    └── prometheus-service.yaml

2 directories, 12 files
```
- Изменил название чарта в файле Chart.yaml на promgra и переименовываю каталог "docker-compose" в "promgra"
- В grafana-service.yaml добавляю ip ВМ
```
externalIPs:
    - 10.101.249.250
```
- Упаковываю чарт
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> helm package promgra
Successfully packaged chart and saved it to: /home/ilya/Desktop/3 семестр/Методы и инструменты DevOps/10/vparanoid10/prometheus_grafana/promgra-0.0.1.tgz
```
- Запускаю minikube
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main) [1]> minikube start
😄  minikube v1.37.0 на Arch 
✨  Используется драйвер docker на основе существующего профиля
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.48 ...
🏃  Обновляется работающий docker "minikube" container ...
🐳  Подготавливается Kubernetes v1.34.0 на Docker 28.4.0 ...
🔎  Компоненты Kubernetes проверяются ...
    ▪ Используется образ gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Включенные дополнения: default-storageclass, storage-provisioner
🏄  Готово! kubectl настроен для использования кластера "minikube" и "default" пространства имён по умолчанию
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> kubectl get deployments.apps
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
blackbox     1/1     1            1           107s
grafana      1/1     1            1           107s
prometheus   1/1     1            1           107s
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> kubectl get services
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP     PORT(S)    AGE
blackbox     ClusterIP   10.111.26.11     <none>          9115/TCP   109s
grafana      ClusterIP   10.106.233.53    192.168.22.10   3000/TCP   109s
kubernetes   ClusterIP   10.96.0.1        <none>          443/TCP    21m
prometheus   ClusterIP   10.106.125.189   <none>          9090/TCP   109s
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> minikube tunnel --bind-address 192.168.22.10
✅  Tunnel successfully started

📌  NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...
```
- Устанавливаю релиз
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> helm install promgra ./promgra-0.0.1.tgz 
NAME: promgra
LAST DEPLOYED: Sat Nov 15 19:22:09 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> kubectl get pods
NAME                         READY   STATUS    RESTARTS      AGE
blackbox-6bfb4bcdbd-gkxfd    1/1     Running   2 (75s ago)   2m39s
grafana-5dbbb4b74b-cbjrm     1/1     Running   2 (65s ago)   2m39s
prometheus-c65b88647-prxn7   1/1     Running   2 (75s ago)   2m39s
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> minikube image load grafana/grafana
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> 
```
- Пробрасываю порты
```
ilya@podyukov-deb-2 ~/v/prometheus_grafana (main)> kubectl port-forward --address 0.0.0.0 svc/grafana 3000:3000
Forwarding from 0.0.0.0:3000 -> 3000
```
- Проверяю работу в браузере
<img width="1153" height="741" alt="изображение" src="https://github.com/user-attachments/assets/55d3d60c-8529-4af8-881b-2b1ae0afb500" />
- Добавляю values к чарту
<img width="912" height="377" alt="изображение" src="https://github.com/user-attachments/assets/fee29546-b039-4fc2-8a9d-303ff09977e4" />

- Создаю values.yaml
```
EXTERNAL_IP: 10.101.249.250
EXTERNAL_PORT: 3113
GF_ADMIN_PASSWORD: HiGrafana
```
- Провожу апгрейд релиза
```
ilya@podyukov-deb-2 ~/v/p/promgra (main)> helm upgrade promgra ./ --set EXTERNAL_PORT=3456
Release "promgra" has been upgraded. Happy Helming!
NAME: promgra
LAST DEPLOYED: Tue Dec 16 14:59:39 2025
NAMESPACE: default
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None
```
```
ilya@podyukov-deb-2 ~/v/p/promgra (main)> kubectl get services
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP      PORT(S)    AGE
blackbox     ClusterIP   10.104.59.101   <none>           9115/TCP   61m
grafana      ClusterIP   10.98.39.209    10.101.249.250   3456/TCP   61m
kubernetes   ClusterIP   10.96.0.1       <none>           443/TCP    2d22h
prometheus   ClusterIP   10.101.184.28   <none>           9090/TCP   61m
ilya@podyukov-deb-2 ~/v/p/promgra (main)> helm get values promgra
USER-SUPPLIED VALUES:
EXTERNAL_PORT: 3456
ilya@podyukov-deb-2 ~/v/p/promgra (main)> helm get values promgra --all
COMPUTED VALUES:
EXTERNAL_IP: 10.101.249.250
EXTERNAL_PORT: 3456
GF_ADMIN_PASSWORD: HiGrafana
```
- Проверяю в браузере
<img width="1024" height="720" alt="изображение" src="https://github.com/user-attachments/assets/8c79b10b-4943-432a-b095-2f66d76c2eb6" />

- Выполняю демонтаж релиза
```
ilya@podyukov-deb-2 ~/v/p/promgra (main)> helm uninstall promgra
release "promgra" uninstalled
ilya@podyukov-deb-2 ~/v/p/promgra (main)> kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   2d22h
```
### kustomize
- Переношу манифесты flask_redis в отдельный каталог base
```
ilya@podyukov-deb-2 ~/vparanoid10 (main) [127]> mkdir base
ilya@podyukov-deb-2 ~/vparanoid10 (main)> cp -r flask_redis base/
ilya@podyukov-deb-2 ~/vparanoid10 (main)> cd base/
ilya@podyukov-deb-2 ~/v/base (main)> tree
.
├── flask_redis
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── flask-service.yml
├── flask.yml
├── redis-service.yml
└── redis.yml

2 directories, 7 files
```
- Создаю файл kustomization.yaml и проверяю
```
ilya@podyukov-deb-2 ~/v/base (main)> kubectl kustomize .
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
  name: redis
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: devops-course-2025
    svc: db
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
  name: service-devops
spec:
  ports:
  - nodePort: 30000
    port: 8000
    targetPort: 5000
  selector:
    app: devops-course-2025
    svc: front
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
  name: flask-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: devops-course-2025
      svc: front
  template:
    metadata:
      labels:
        app: devops-course-2025
        svc: front
    spec:
      containers:
      - image: flask:v1
        imagePullPolicy: IfNotPresent
        name: flask
        ports:
        - containerPort: 5000
        resources:
          limits:
            memory: 256Mi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-course-2025
  template:
    metadata:
      labels:
        app: devops-course-2025
        svc: db
    spec:
      containers:
      - image: redis:alpine
        imagePullPolicy: IfNotPresent
        name: redis
        ports:
        - containerPort: 6379
```
- Создаю каталоги dev и prod, и кладу в них kustomization.yaml и проверяю
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl kustomize dev
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: dev
  name: dev-redis
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: devops-course-2025
    environment: dev
    svc: db
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: dev
  name: dev-service-devops
spec:
  ports:
  - nodePort: 30000
    port: 8000
    targetPort: 5000
  selector:
    app: devops-course-2025
    environment: dev
    svc: front
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
    environment: dev
  name: dev-flask-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: devops-course-2025
      environment: dev
      svc: front
  template:
    metadata:
      labels:
        app: devops-course-2025
        environment: dev
        svc: front
    spec:
      containers:
      - image: flask:v1
        imagePullPolicy: IfNotPresent
        name: flask
        ports:
        - containerPort: 5000
        resources:
          limits:
            memory: 256Mi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
    environment: dev
  name: dev-redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-course-2025
      environment: dev
  template:
    metadata:
      labels:
        app: devops-course-2025
        environment: dev
        svc: db
    spec:
      containers:
      - image: redis:alpine
        imagePullPolicy: IfNotPresent
        name: redis
        ports:
        - containerPort: 6379
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl kustomize prod
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: prod
  name: prod-redis
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: devops-course-2025
    environment: prod
    svc: db
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: prod
  name: prod-service-devops
spec:
  ports:
  - nodePort: 30000
    port: 8000
    targetPort: 5000
  selector:
    app: devops-course-2025
    environment: prod
    svc: front
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
    environment: prod
  name: prod-flask-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: devops-course-2025
      environment: prod
      svc: front
  template:
    metadata:
      labels:
        app: devops-course-2025
        environment: prod
        svc: front
    spec:
      containers:
      - image: flask:v1
        imagePullPolicy: IfNotPresent
        name: flask
        ports:
        - containerPort: 5000
        resources:
          limits:
            memory: 256Mi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: devops-course-2025
    environment: prod
  name: prod-redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-course-2025
      environment: prod
  template:
    metadata:
      labels:
        app: devops-course-2025
        environment: prod
        svc: db
    spec:
      containers:
      - image: redis:alpine
        imagePullPolicy: IfNotPresent
        name: redis
        ports:
        - containerPort: 6379
```
- Создаю dev/service-patch.yaml и проверяю
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl kustomize dev
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: dev
  name: dev-redis
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: devops-course-2025
    environment: dev
    svc: db
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: devops-course-2025
    environment: dev
    svc: flask-front
  name: dev-service-devops
spec:
  externalIPs:
  - 10.101.249.250
  ports:
  - name: flask-port
    nodePort: 30000
    port: 54321
    targetPort: 5000
  selector:
    app: devops-course-2025
    environment: dev
    svc: front
  type: LoadBalancer
```
- Применяю в кластер манифесты
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev/
service/dev-redis created
service/dev-service-devops created
deployment.apps/dev-flask-app created
deployment.apps/dev-redis created
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get services
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)           AGE
dev-redis            ClusterIP      10.98.214.202   <none>           6379/TCP          24s
dev-service-devops   LoadBalancer   10.103.84.34    10.101.249.250   54321:30000/TCP   24s
kubernetes           ClusterIP      10.96.0.1       <none>           443/TCP           2d23h
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get deployments
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
dev-flask-app   0/5     5            0           36s
dev-redis       1/1     1            1           36s
```
- Применяю манифесты с prod кастомизацией и получил ошибку
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod
service/prod-redis created
deployment.apps/prod-flask-app created
deployment.apps/prod-redis created
The Service "prod-service-devops" is invalid: spec.ports[0].nodePort: Invalid value: 30000: provided port is already allocated
```
- Изменил порт
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod
service/prod-redis unchanged
service/prod-service-devops created
deployment.apps/prod-flask-app unchanged
deployment.apps/prod-redis unchanged
```
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get services
NAME                  TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)           AGE
dev-redis             ClusterIP      10.98.214.202    <none>           6379/TCP          4m29s
dev-service-devops    LoadBalancer   10.103.84.34     10.101.249.250   54321:30000/TCP   4m29s
kubernetes            ClusterIP      10.96.0.1        <none>           443/TCP           2d23h
prod-redis            ClusterIP      10.96.3.117      <none>           6379/TCP          3m2s
prod-service-devops   LoadBalancer   10.105.218.211   10.101.249.250   12345:32512/TCP   107s
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
dev-flask-app-86dd94f74c-55pcv    0/1     ImagePullBackOff   0          4m36s
dev-flask-app-86dd94f74c-8fftm    0/1     ImagePullBackOff   0          4m36s
dev-flask-app-86dd94f74c-czlnp    0/1     ImagePullBackOff   0          4m36s
dev-flask-app-86dd94f74c-gl8qq    0/1     ImagePullBackOff   0          4m36s
dev-flask-app-86dd94f74c-h7bvx    0/1     ImagePullBackOff   0          4m36s
dev-redis-8cbcffcc6-4zbn6         1/1     Running            0          4m36s
prod-flask-app-5b4479b48f-dtrg6   0/1     ImagePullBackOff   0          3m9s
prod-flask-app-5b4479b48f-lzdrr   0/1     ImagePullBackOff   0          3m9s
prod-flask-app-5b4479b48f-rktgf   0/1     ImagePullBackOff   0          3m9s
prod-flask-app-5b4479b48f-tsk46   0/1     ImagePullBackOff   0          3m9s
prod-flask-app-5b4479b48f-zcwcz   0/1     ImagePullBackOff   0          3m9s
prod-redis-9f8bc7ff8-pdv52        1/1     Running            0          3m9s
```
- Кастомизирую количество реплик в dev и применяю в кластер
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev
service/dev-redis unchanged
deployment.apps/dev-flask-app configured
deployment.apps/dev-redis unchanged
The Service "dev-service-devops" is invalid: spec.ports[0].nodePort: Invalid value: 32512: provided port is already allocated
- Снова меняю порт
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev
service/dev-redis unchanged
service/dev-service-devops configured
deployment.apps/dev-flask-app unchanged
deployment.apps/dev-redis unchanged
```
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
dev-flask-app-86dd94f74c-gl8qq    0/1     ImagePullBackOff   0          10m
dev-flask-app-86dd94f74c-h7bvx    0/1     ImagePullBackOff   0          10m
dev-redis-8cbcffcc6-4zbn6         1/1     Running            0          10m
prod-flask-app-5b4479b48f-dtrg6   0/1     ImagePullBackOff   0          9m31s
prod-flask-app-5b4479b48f-lzdrr   0/1     ImagePullBackOff   0          9m31s
prod-flask-app-5b4479b48f-rktgf   0/1     ImagePullBackOff   0          9m31s
prod-flask-app-5b4479b48f-tsk46   0/1     ImagePullBackOff   0          9m31s
prod-flask-app-5b4479b48f-zcwcz   0/1     ImagePullBackOff   0          9m31s
prod-redis-9f8bc7ff8-pdv52        1/1     Running            0          9m31s
```
- Исправляю ошибку ImagePullBackOff
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> eval $(minikube docker-env)
ilya@podyukov-deb-2 ~/vparanoid10 (main)> docker images
                                                                                                                      i Info →   U  In Use
IMAGE                                             ID             DISK USAGE   CONTENT SIZE   EXTRA
gcr.io/k8s-minikube/storage-provisioner:v5        6e38f40d628d       31.5MB             0B    U
grafana/grafana:latest                            d65277dbf54f        746MB             0B
prom/blackbox-exporter:latest                     2bb660d6acaa       36.5MB             0B
prom/prometheus:latest                            20a11eec2fec        378MB             0B
redis:alpine                                      778c3ea605c2       94.7MB             0B    U
registry.k8s.io/coredns/coredns:v1.12.1           52546a367cc9         75MB             0B    U
registry.k8s.io/etcd:3.6.4-0                      5f1f5298c888        195MB             0B    U
registry.k8s.io/kube-apiserver:v1.34.0            90550c43ad2b         88MB             0B    U
registry.k8s.io/kube-controller-manager:v1.34.0   a0af72f2ec6d       74.9MB             0B    U
registry.k8s.io/kube-proxy:v1.34.0                df0860106674       71.9MB             0B    U
registry.k8s.io/kube-scheduler:v1.34.0            46169d968e92       52.8MB             0B    U
registry.k8s.io/pause:3.10.1                      cd073f4c5f6a        736kB             0B    U
ilya@podyukov-deb-2 ~/vparanoid10 (main)> cd base/flask_redis/
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)> ls
app.py  Dockerfile  requirements.txt
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)> docker images | grep flask-redis-app
WARNING: This output is designed for human readability. For machine-readable output, please use --format.
ilya@podyukov-deb-2 ~/v/b/flask_redis (main) [0|1]> docker build -t flask-redis-app .
[+] Building 38.9s (10/10) FINISHED                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                 0.0s
 => => transferring dockerfile: 238B                                                                                                 0.0s
 => [internal] load metadata for docker.io/library/python:latest                                                                     2.5s
 => [internal] load .dockerignore                                                                                                    0.0s
 => => transferring context: 2B                                                                                                      0.0s
 => [internal] load build context                                                                                                    0.0s
 => => transferring context: 388B                                                                                                    0.0s
 => [1/5] FROM docker.io/library/python:latest@sha256:492b292a9449d096aefe5b1399cc64de53359845754da3e4d2539402013c826b              27.0s
 => => resolve docker.io/library/python:latest@sha256:492b292a9449d096aefe5b1399cc64de53359845754da3e4d2539402013c826b               0.0s
 => => sha256:2981f7e8980b9f4b6605026e1c5f99b4971ebba15f626e46904554de09f324f4 49.29MB / 49.29MB                                     1.7s
 => => sha256:b22766554d6bfa95c7325b00ee002f2705a7b8605908c3eb43dbe729c412422c 25.61MB / 25.61MB                                     1.4s
 => => sha256:58f2d358b447d091790c5ef0943550bbcf57bac46c4b8bfcfc3e6dacf4cb7969 67.78MB / 67.78MB                                     4.5s
 => => sha256:492b292a9449d096aefe5b1399cc64de53359845754da3e4d2539402013c826b 10.95kB / 10.95kB                                     0.0s
 => => sha256:f59048c479e585a6ef4aef2c25883eb40556073eccb38db574d65de27b657439 2.32kB / 2.32kB                                       0.0s
 => => sha256:91b058ae471b66b4c7d19426be87e375d9f091f03e5ea08684dd808966c9ae97 6.48kB / 6.48kB                                       0.0s
 => => sha256:dd420cee8193b72cf70974a80e88896c8e58d925edd1cdc515b203ff7aa65550 235.97MB / 235.97MB                                   5.7s
 => => sha256:388c30f2dc569df381ac55ed9c7bf0a3494a7383ed09b64f8c2c4ff9439b29a1 6.08MB / 6.08MB                                       2.3s
 => => extracting sha256:2981f7e8980b9f4b6605026e1c5f99b4971ebba15f626e46904554de09f324f4                                            3.4s
 => => sha256:5f3f8a41ae1eca164f1c6ac9c8b0f444f478e31ceece03a5283b4e9eaec9513e 29.40MB / 29.40MB                                     3.3s
 => => sha256:56d5b01339430c5cd5004ca11b1673730eaf84ff0d2aedf058500d76ae7a1c03 249B / 249B                                           3.8s
 => => extracting sha256:b22766554d6bfa95c7325b00ee002f2705a7b8605908c3eb43dbe729c412422c                                            1.2s
 => => extracting sha256:58f2d358b447d091790c5ef0943550bbcf57bac46c4b8bfcfc3e6dacf4cb7969                                            4.1s
 => => extracting sha256:dd420cee8193b72cf70974a80e88896c8e58d925edd1cdc515b203ff7aa65550                                           13.4s
 => => extracting sha256:388c30f2dc569df381ac55ed9c7bf0a3494a7383ed09b64f8c2c4ff9439b29a1                                            0.5s
 => => extracting sha256:5f3f8a41ae1eca164f1c6ac9c8b0f444f478e31ceece03a5283b4e9eaec9513e                                            1.4s
 => => extracting sha256:56d5b01339430c5cd5004ca11b1673730eaf84ff0d2aedf058500d76ae7a1c03                                            0.0s
 => [2/5] WORKDIR /code                                                                                                              0.3s
 => [3/5] COPY requirements.txt requirements.txt                                                                                     0.0s
 => [4/5] RUN pip install -r requirements.txt                                                                                        8.4s
 => [5/5] COPY app.py .                                                                                                              0.0s
 => exporting to image                                                                                                               0.4s
 => => exporting layers                                                                                                              0.4s
 => => writing image sha256:42e886700ef458742f943efe7041bce0be785ceefff08d7dfad07cae5ac353d3                                         0.0s
 => => naming to docker.io/library/flask-redis-app                                                                                   0.0s
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)> docker images
                                                                                                                      i Info →   U  In Use
IMAGE                                             ID             DISK USAGE   CONTENT SIZE   EXTRA
flask-redis-app:latest                            42e886700ef4       1.13GB             0B
gcr.io/k8s-minikube/storage-provisioner:v5        6e38f40d628d       31.5MB             0B    U
grafana/grafana:latest                            d65277dbf54f        746MB             0B
prom/blackbox-exporter:latest                     2bb660d6acaa       36.5MB             0B
prom/prometheus:latest                            20a11eec2fec        378MB             0B
redis:alpine                                      778c3ea605c2       94.7MB             0B    U
registry.k8s.io/coredns/coredns:v1.12.1           52546a367cc9         75MB             0B    U
registry.k8s.io/etcd:3.6.4-0                      5f1f5298c888        195MB             0B    U
registry.k8s.io/kube-apiserver:v1.34.0            90550c43ad2b         88MB             0B    U
registry.k8s.io/kube-controller-manager:v1.34.0   a0af72f2ec6d       74.9MB             0B    U
registry.k8s.io/kube-proxy:v1.34.0                df0860106674       71.9MB             0B    U
registry.k8s.io/kube-scheduler:v1.34.0            46169d968e92       52.8MB             0B    U
registry.k8s.io/pause:3.10.1                      cd073f4c5f6a        736kB             0B    U
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)>
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)> ls
app.py  Dockerfile  requirements.txt
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)>
ilya@podyukov-deb-2 ~/v/b/flask_redis (main)> cd ../..
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
dev-flask-app-7485888f8-hqxk4     1/1     Running            0          15m
dev-flask-app-86dd94f74c-gl8qq    0/1     ImagePullBackOff   0          36m
dev-flask-app-86dd94f74c-h7bvx    0/1     ImagePullBackOff   0          36m
dev-redis-8cbcffcc6-4zbn6         1/1     Running            0          36m
prod-flask-app-5b4479b48f-dtrg6   0/1     ImagePullBackOff   0          35m
prod-flask-app-5b4479b48f-lzdrr   0/1     ImagePullBackOff   0          35m
prod-flask-app-5b4479b48f-rktgf   0/1     ImagePullBackOff   0          35m
prod-flask-app-5b4479b48f-tsk46   0/1     ImagePullBackOff   0          35m
prod-flask-app-5b4479b48f-zcwcz   0/1     ImagePullBackOff   0          35m
prod-redis-9f8bc7ff8-pdv52        1/1     Running            0          35m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl delete deployment dev-flask-app prod-flask-app
deployment.apps "dev-flask-app" deleted from default namespace
deployment.apps "prod-flask-app" deleted from default namespace
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
dev-redis-8cbcffcc6-4zbn6    1/1     Running   0          37m
prod-redis-9f8bc7ff8-pdv52   1/1     Running   0          35m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -f base/flask.yml
deployment.apps/flask-app created
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev/
service/dev-redis unchanged
service/dev-service-devops unchanged
deployment.apps/dev-flask-app created
deployment.apps/dev-redis unchanged
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod/
service/prod-redis unchanged
deployment.apps/prod-flask-app created
deployment.apps/prod-redis unchanged
The Service "prod-service-devops" is invalid: spec.ports[0].nodePort: Invalid value: 32522: provided port is already allocated
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> kubectl get pods
NAME                              READY   STATUS              RESTARTS   AGE
dev-flask-app-86dd94f74c-nvnll    0/1     ContainerCreating   0          10s
dev-flask-app-86dd94f74c-pgpmx    0/1     ContainerCreating   0          10s
dev-redis-8cbcffcc6-4zbn6         1/1     Running             0          37m
flask-app-79b8d5d949-6m89p        0/1     ErrImagePull        0          14s
flask-app-79b8d5d949-b56hj        0/1     ErrImagePull        0          13s
flask-app-79b8d5d949-dfs8d        0/1     ContainerCreating   0          13s
flask-app-79b8d5d949-r5t44        0/1     ContainerCreating   0          13s
flask-app-79b8d5d949-zsbfk        0/1     ErrImagePull        0          13s
prod-flask-app-5b4479b48f-498w6   0/1     ContainerCreating   0          4s
prod-flask-app-5b4479b48f-56bmz   0/1     ContainerCreating   0          4s
prod-flask-app-5b4479b48f-l25mm   0/1     ContainerCreating   0          4s
prod-flask-app-5b4479b48f-s4lml   0/1     ContainerCreating   0          4s
prod-flask-app-5b4479b48f-zjkk6   0/1     ContainerCreating   0          4s
prod-redis-9f8bc7ff8-pdv52        1/1     Running             0          36m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                              READY   STATUS              RESTARTS   AGE
dev-flask-app-86dd94f74c-nvnll    0/1     ErrImagePull        0          18s
dev-flask-app-86dd94f74c-pgpmx    0/1     ErrImagePull        0          18s
dev-redis-8cbcffcc6-4zbn6         1/1     Running             0          37m
flask-app-79b8d5d949-6m89p        0/1     ImagePullBackOff    0          22s
flask-app-79b8d5d949-b56hj        0/1     ImagePullBackOff    0          21s
flask-app-79b8d5d949-dfs8d        0/1     ErrImagePull        0          21s
flask-app-79b8d5d949-r5t44        0/1     ErrImagePull        0          21s
flask-app-79b8d5d949-zsbfk        0/1     ErrImagePull        0          21s
prod-flask-app-5b4479b48f-498w6   0/1     ContainerCreating   0          12s
prod-flask-app-5b4479b48f-56bmz   0/1     ContainerCreating   0          12s
prod-flask-app-5b4479b48f-l25mm   0/1     ContainerCreating   0          12s
prod-flask-app-5b4479b48f-s4lml   0/1     ErrImagePull        0          12s
prod-flask-app-5b4479b48f-zjkk6   0/1     ContainerCreating   0          12s
prod-redis-9f8bc7ff8-pdv52        1/1     Running             0          36m
ilya@podyukov-deb-2 ~/vparanoid10 (main)>
ilya@podyukov-deb-2 ~/vparanoid10 (main)>
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
dev-flask-app-86dd94f74c-nvnll    0/1     ImagePullBackOff   0          93s
dev-flask-app-86dd94f74c-pgpmx    0/1     ImagePullBackOff   0          93s
dev-redis-8cbcffcc6-4zbn6         1/1     Running            0          39m
flask-app-79b8d5d949-6m89p        0/1     ImagePullBackOff   0          97s
flask-app-79b8d5d949-b56hj        0/1     ImagePullBackOff   0          96s
flask-app-79b8d5d949-dfs8d        0/1     ErrImagePull       0          96s
flask-app-79b8d5d949-r5t44        0/1     ErrImagePull       0          96s
flask-app-79b8d5d949-zsbfk        0/1     ErrImagePull       0          96s
prod-flask-app-5b4479b48f-498w6   0/1     ImagePullBackOff   0          87s
prod-flask-app-5b4479b48f-56bmz   0/1     ImagePullBackOff   0          87s
prod-flask-app-5b4479b48f-l25mm   0/1     ImagePullBackOff   0          87s
prod-flask-app-5b4479b48f-s4lml   0/1     ImagePullBackOff   0          87s
prod-flask-app-5b4479b48f-zjkk6   0/1     ImagePullBackOff   0          87s
prod-redis-9f8bc7ff8-pdv52        1/1     Running            0          37m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl delete deployment dev-flask-app prod-flask-app
deployment.apps "dev-flask-app" deleted from default namespace
deployment.apps "prod-flask-app" deleted from default namespace
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl get pods
NAME                         READY   STATUS             RESTARTS   AGE
dev-redis-8cbcffcc6-4zbn6    1/1     Running            0          39m
flask-app-79b8d5d949-6m89p   0/1     ImagePullBackOff   0          112s
flask-app-79b8d5d949-b56hj   0/1     ImagePullBackOff   0          111s
flask-app-79b8d5d949-dfs8d   0/1     ImagePullBackOff   0          111s
flask-app-79b8d5d949-r5t44   0/1     ImagePullBackOff   0          111s
flask-app-79b8d5d949-zsbfk   0/1     ImagePullBackOff   0          111s
prod-redis-9f8bc7ff8-pdv52   1/1     Running            0          37m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl delete deployment dev-flask-app prod-flask-app
Error from server (NotFound): deployments.apps "dev-flask-app" not found
Error from server (NotFound): deployments.apps "prod-flask-app" not found
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> kubectl get pods
NAME                         READY   STATUS             RESTARTS   AGE
dev-redis-8cbcffcc6-4zbn6    1/1     Running            0          39m
flask-app-79b8d5d949-6m89p   0/1     ImagePullBackOff   0          119s
flask-app-79b8d5d949-b56hj   0/1     ImagePullBackOff   0          118s
flask-app-79b8d5d949-dfs8d   0/1     ImagePullBackOff   0          118s
flask-app-79b8d5d949-r5t44   0/1     ImagePullBackOff   0          118s
flask-app-79b8d5d949-zsbfk   0/1     ImagePullBackOff   0          118s
prod-redis-9f8bc7ff8-pdv52   1/1     Running            0          37m
ilya@podyukov-deb-2 ~/vparanoid10 (main)> sed -i 's|image: .*|image: flask-redis-app|' base/flask.yml
ilya@podyukov-deb-2 ~/vparanoid10 (main)> sed -i '/image:/a\        imagePullPolicy: IfNotPresent' base/flask.yml
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -f base/flask.yml
deployment.apps/flask-app configured
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev/
error: map[string]interface {}(nil): yaml: unmarshal errors:
  line 26: mapping key "imagePullPolicy" already defined at line 25
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> kubectl apply -k prod/
error: map[string]interface {}(nil): yaml: unmarshal errors:
  line 26: mapping key "imagePullPolicy" already defined at line 25
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> nano base/flask.yml
ilya@podyukov-deb-2 ~/vparanoid10 (main)> nano base/flask.yml
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k dev/
service/dev-redis unchanged
service/dev-service-devops unchanged
deployment.apps/dev-flask-app created
deployment.apps/dev-redis unchanged
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod/
service/prod-redis unchanged
deployment.apps/prod-flask-app created
deployment.apps/prod-redis unchanged
The Service "prod-service-devops" is invalid: spec.ports[0].nodePort: Invalid value: 32522: provided port is already allocated
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
dev-flask-app-7485888f8-dvm4d     1/1     Running   0          9s
dev-flask-app-7485888f8-kw2vm     1/1     Running   0          9s
dev-redis-8cbcffcc6-4zbn6         1/1     Running   0          42m
flask-app-949664468-fcr4g         1/1     Running   0          2m18s
flask-app-949664468-jbcjh         1/1     Running   0          2m18s
flask-app-949664468-kn5c2         1/1     Running   0          2m19s
flask-app-949664468-lb9jb         1/1     Running   0          2m19s
flask-app-949664468-p74f5         1/1     Running   0          2m19s
prod-flask-app-85466bd96d-6276v   1/1     Running   0          6s
prod-flask-app-85466bd96d-b8dmd   1/1     Running   0          6s
prod-flask-app-85466bd96d-djj6f   1/1     Running   0          6s
prod-flask-app-85466bd96d-qwt58   1/1     Running   0          6s
prod-flask-app-85466bd96d-rh64w   1/1     Running   0          6s
prod-redis-9f8bc7ff8-pdv52        1/1     Running   0          40m
```
- Пытаюсь запустить и получаю ошибку
```
ilya@podyukov-deb-2 ~/v/prometheus_grafana (main) [1]> kubectl port-forward --address 0.0.0.0 svc/dev-service-devops 54321:54321
Forwarding from 0.0.0.0:54321 -> 5000
Handling connection for 54321
```
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> curl http://10.101.249.250:54321
<!doctype html>
<html lang=en>
  <head>
    <title>redis.exceptions.ConnectionError: Error -2 connecting to redis:6379. Name or service not known.
 // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = false,
          EVALEX = false,
          EVALEX_TRUSTED = false,
          SECRET = "aGbfEOJ6mihIo2VGYPPR";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>redis.exceptions.ConnectionError</h1>
<div class="detail">
  <p class="errormsg">redis.exceptions.ConnectionError: Error -2 connecting to redis:6379. Name or service not known.
...
```
- Исправляю app.py, dev/deployment-patch.yaml, prod/deployment-patch.yaml, base\flask.yml
```
redis_host = os.getenv('REDIS_HOST', 'localhost')
cache = redis.Redis(host=redis_host, port=6379)
```
- Пересобираю образ
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> minikube image build -t flask-redis-app:v4 base/flask_redis/
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 238B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:latest
#2 DONE 0.6s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [1/5] FROM docker.io/library/python:latest@sha256:492b292a9449d096aefe5b1399cc64de53359845754da3e4d2539402013c826b
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 451B done
#5 DONE 0.0s

#6 [2/5] WORKDIR /code
#6 CACHED

#7 [3/5] COPY requirements.txt requirements.txt
#7 CACHED

#8 [4/5] RUN pip install -r requirements.txt
#8 CACHED

#9 [5/5] COPY app.py .
#9 DONE 0.1s

#10 exporting to image
#10 exporting layers 0.0s done
#10 writing image sha256:2e95873834308801be1bd58db48c6ec6243809e166bd901cbcc3961434991c4b done
#10 naming to docker.io/library/flask-redis-app:v4 done
#10 DONE 0.1s
```
- Применяю кастомизацию
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod
service/prod-redis unchanged
deployment.apps/prod-flask-app configured
deployment.apps/prod-redis unchanged
The Service "prod-service-devops" is invalid: spec.ports[0].nodePort: Invalid value: 32524: provided port is already allocated
ilya@podyukov-deb-2 ~/vparanoid10 (main) [1]> kubectl apply -k dev
service/dev-redis unchanged
service/dev-service-devops unchanged
deployment.apps/dev-flask-app configured
deployment.apps/dev-redis unchanged
ilya@podyukov-deb-2 ~/vparanoid10 (main)> nano base/flask-service.yml
ilya@podyukov-deb-2 ~/vparanoid10 (main)> kubectl apply -k prod
service/prod-redis unchanged
service/prod-service-devops configured
deployment.apps/prod-flask-app unchanged
deployment.apps/prod-redis unchanged
```
- Проверяю
```
ilya@podyukov-deb-2 ~/vparanoid10 (main)> curl 10.101.249.250:54321
Hello World! I have been seen 3 times. My name is: dev-flask-app-5465dc8b55-lw4mg
ilya@podyukov-deb-2 ~/vparanoid10 (main)> curl 10.101.249.250:32525
Hello World! I have been seen 1 times. My name is: prod-flask-app-697c95dc64-tnrqr
```
