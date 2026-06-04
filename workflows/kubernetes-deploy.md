---
name: Kubernetes Deploy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Kubernetes deployment workflow. Covers manifests, ConfigMaps, Secrets, Ingress, persistent volumes, Helm basics, and kubectl commands.
tags: [workflow, kubernetes, k8s, deployment, helm, ingress, secrets]
role: devops-engineer
---

# Kubernetes Deploy

## 1. Namespace Setup

```bash
kubectl create namespace production
kubectl config set-context --current --namespace=production
```

## 2. Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
    spec:
      containers:
        - name: app
          image: myregistry/myapp:1.0.0
          ports:
            - containerPort: 8080
              name: http
          envFrom:
            - configMapRef:
                name: myapp-config
          env:
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: db-password
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
```

## 3. ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  application.properties: |
    server.port=8080
    logging.level.root=INFO
    spring.datasource.url=jdbc:postgresql://db:5432/mydb
```

## 4. Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  db-password: cGFzc3dvcmQxMjM=  # base64 encoded
  api-key: QVBJLUtFWS0xMjM=    # base64 encoded
```

Or create imperatively:

```bash
kubectl create secret generic myapp-secrets \
  --from-literal=db-password=password123 \
  --from-literal=api-key=API-KEY-123
```

## 5. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      name: http
  type: ClusterIP
```

## 6. Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

## 7. Persistent Volume

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
```

Mount in deployment:

```yaml
volumeMounts:
  - name: storage
    mountPath: /data
volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: myapp-storage
```

## 8. Helm Basics

### Chart Structure

```
mychart/
  Chart.yaml
  values.yaml
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    _helpers.tpl
```

### Install / Upgrade

```bash
# Install
helm install myapp ./mychart

# Upgrade
helm upgrade myapp ./mychart

# Rollback
helm rollback myapp 1

# List releases
helm list
```

### values.yaml

```yaml
replicaCount: 3
image:
  repository: myregistry/myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: true
  hosts:
    - host: app.example.com
      paths:
        - /
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi
```

## 9. Common kubectl Commands

| Command | Purpose |
|---------|---------|
| `kubectl apply -f manifest.yaml` | Create/update resources |
| `kubectl get pods` | List pods |
| `kubectl logs -f pod-name` | Stream logs |
| `kubectl exec -it pod-name -- /bin/sh` | Shell into container |
| `kubectl port-forward svc/myapp 8080:80` | Local port forwarding |
| `kubectl scale deployment myapp --replicas=5` | Scale replicas |
| `kubectl rollout restart deployment/myapp` | Rolling restart |
| `kubectl rollout status deployment/myapp` | Check rollout status |
| `kubectl top pods` | Resource usage |
