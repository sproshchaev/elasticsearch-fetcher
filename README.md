# elasticsearch-fetcher

`1.` Проверка доступности кластера X.X.X.X:YYYY
```bash
curl http://X.X.X.X:YYYY/_cluster/health
```
Пример ответа:
```txt
{
  "name": "coordinator-preproduction-1",
  "cluster_name": "elasticsearch_preproduction",
  "cluster_uuid": "xYz1AbCdEfGhIjKlMnOpQr",
  "version": {
    "number": "7.17.9",
    "build_flavor": "default",
    "build_type": "deb",
    "build_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "build_date": "2023-01-31T05:34:43.305517834Z",
    "build_snapshot": false,
    "lucene_version": "8.11.1",
    "minimum_wire_compatibility_version": "6.8.0",
    "minimum_index_compatibility_version": "6.0.0-beta1"
  },
  "tagline": "You Know, for Search"
}
```
