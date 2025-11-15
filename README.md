# Подюков Илья. ФИТ-2-2024 НМ. Методы и инструменты DevOps. ЛР по лекции 10

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
- В grafana-service.yaml добавляю ip ПК
```
externalIPs:
    - 192.168.22.10
```
- Упаковываю чарт
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> helm package promgra
Successfully packaged chart and saved it to: /home/ilya/Desktop/3 семестр/Методы и инструменты DevOps/10/vparanoid10/prometheus_grafana/promgra-0.0.1.tgz
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
- Запускаю
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
```
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> kubectl get pods
NAME                         READY   STATUS    RESTARTS      AGE
blackbox-6bfb4bcdbd-gkxfd    1/1     Running   2 (75s ago)   2m39s
grafana-5dbbb4b74b-cbjrm     1/1     Running   2 (65s ago)   2m39s
prometheus-c65b88647-prxn7   1/1     Running   2 (75s ago)   2m39s
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> minikube image load grafana/grafana
ilya@msi ~/D/3/М/1/v/prometheus_grafana (main)> 
```
- 
