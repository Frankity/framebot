from models import *
import requests


def get_alerts():
    alerts = []
    try:
        r = requests.get('https://ws.warframestat.us/pc/alerts', headers={'User-agent': 'Vector'})
        if r.status_code == 200:
            for alert in r.json():
                exists = Alerts.select().where(Alerts.id == alert['id'])
                if not exists:
                    Alerts.create(id=alert['id'])
                    alerts.append(alert)
                else:
                    pass

            return alerts
    except Exception as e:
        print(e)
