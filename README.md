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
ilya@erth ~/Р/v/prometheus_grafana (main) [1]> kompose convert
WARN Restart policy 'unless-stopped' in service grafana is not supported, convert it to 'always' 
WARN Restart policy 'unless-stopped' in service prometheus is not supported, convert it to 'always' 
WARN File don't exist or failed to check if the directory is empty: stat :/var/lib/grafana: no such file or directory 
WARN File don't exist or failed to check if the directory is empty: stat :/prometheus: no such file or directory 
INFO Kubernetes file "blackbox-service.yaml" created 
INFO Kubernetes file "grafana-service.yaml" created 
INFO Kubernetes file "prometheus-service.yaml" created 
INFO Kubernetes file "blackbox-deployment.yaml" created 
INFO Kubernetes file "grafana-deployment.yaml" created 
INFO Kubernetes file "grafana-data-persistentvolumeclaim.yaml" created 
INFO Kubernetes file "grafana-cm0-configmap.yaml" created 
INFO Kubernetes file "prometheus-deployment.yaml" created 
INFO Kubernetes file "prom-data-persistentvolumeclaim.yaml" created 
INFO Kubernetes file "prometheus-cm0-configmap.yaml" created 
```
```
ilya@erth ~/Р/v/prometheus_grafana (main)> kompose convert --chart
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
- 
