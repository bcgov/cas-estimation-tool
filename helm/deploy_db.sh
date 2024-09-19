
set -euo pipefail

echo "Installing database chart: cas-postgres/cas-postgres-cluster..."

helm repo add cas-postgres https://bcgov.github.io/cas-postgres/
helm repo update

helm upgrade --install --atomic --timeout 1800s \
  --namespace "599f0a-dev" \
  --values ./database/values.yaml \
  cas-estimation-db cas-postgres/cas-postgres-cluster --version 1.1.1
