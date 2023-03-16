helm repo add tsuru https://tsuru.github.io/charts
helm repo update
helm install tsuru ./charts/tsuru-stack --create-namespace --namespace tsuru-system 
kubectl exec -it -n tsuru-system deploy/tsuru-api -- tsurud root user create admin@ipaas.site
export TSURU_HOST=$(kubectl get svc -n tsuru-system tsuru-api -o 'jsonpath={.status.loadBalancer.ingress[].ip}')
tsuru target-add bke http://$TSURU_HOST -s
tsuru login
tsuru team create admin
tsuru platform add static
tsuru platform add python
tsuru platform add go
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install promtail grafana/promtail --set "loki.serviceName=loki" --set "config.clients[0].url=http://123.30.234.100/loki/api/prom/push"
