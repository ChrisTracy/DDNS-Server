import requests

hostname = "test1.example.com"
clientID = "[ID]"
clientSecret = "[Secret]"

zone = ".".join(hostname.rsplit(".")[-2:])
pubIP = requests.get('https://domains.google.com/checkip').text

class cloudflare:
    def get_zones(hostname: str) -> str:
        headers = {"Authorization": f"Bearer {clientSecret}"}
        zone_list = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers, params={"name": zone})
        return zone_list    

    def get_records(hostname, zoneID):
        headers = {"Authorization": f"Bearer {clientSecret}"}
        records = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zoneID}/dns_records", headers=headers, params={"name": hostname})
        return records

    def setRecord(hostname):
        zones = (cloudflare.get_zones(hostname=hostname)).json()
        zoneID = zones['result'][0]['id']
        records = (cloudflare.get_records(hostname=hostname, zoneID=zoneID)).json()
        recordID = records['result'][0]['id']
        recordType = records['result'][0]['type']

        uri = f'https://api.cloudflare.com/client/v4/zones/{zoneID}/dns_records/{recordID}'

        payload = {
            'type': recordType,
            'name':hostname,
            'content':pubIP,
            'ttl': 1
        }

        headers = {"Authorization": f"Bearer {clientSecret}", "Content-type": "application/json" }
        r = requests.put(uri, headers=headers, json=payload)
        print (r.content)

class google:
    def setRecord(hostname):
        uri = f'https://{clientID}:{clientSecret}@domains.google.com/nic/update?hostname={hostname}&myip={pubIP}'
        r = requests.get(uri)
        print(r.content)

service = google
service.setRecord(hostname)
