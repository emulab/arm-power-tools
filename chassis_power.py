import requests

p = {'start': '2015-06-24 11:01', 'end': '2015-06-25 11:01'}
f = {'cloudlab-manifest': open('manifest', 'r')}
r = requests.get("http://emmy10.casa.umass.edu:8080/CloudLabWebPortal/utah.jsp", data=p, files=f)

print r.url
print r.status_code
print r.text
