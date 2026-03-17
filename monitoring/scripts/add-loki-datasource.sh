#!/bin/bash
# Скрипт для добавления Loki datasource в Grafana через API

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3002}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin123}"
LOKI_URL="${LOKI_URL:-http://loki:3100}"

echo "Waiting for Grafana to be available..."
for i in {1..30}; do
  if curl -s "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
    echo "Grafana is available!"
    break
  fi
  echo "Waiting for Grafana... ($i/30)"
  sleep 2
done

echo "Adding Loki datasource..."
curl -X POST "$GRAFANA_URL/api/datasources" \
  -H "Content-Type: application/json" \
  -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
  -d "{
    \"name\": \"Loki\",
    \"type\": \"loki\",
    \"access\": \"proxy\",
    \"url\": \"$LOKI_URL\",
    \"isDefault\": false,
    \"editable\": true,
    \"uid\": \"loki\",
    \"jsonData\": {
      \"maxLines\": 1000
    }
  }"

echo ""
echo "Loki datasource added!"
