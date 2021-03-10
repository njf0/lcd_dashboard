import requests
import datetime
import xml.etree.ElementTree as ET
import data

def get_buses():
    
    request_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    message_ref = '13245'
    
    stop_monitoring_request = ET.Element('Siri', {
        'version' : "1.0",
        'xmlns'   : "http://www.siri.org.uk"
        })
    
    sr = ET.SubElement(stop_monitoring_request, 'ServiceRequest')
    ET.SubElement(sr, 'RequestTimestamp').text = request_timestamp
    ET.SubElement(sr, 'RequestorRef').text = data.NEXTBUSES_API_USER
    smr = ET.SubElement(sr, 'StopMonitoringRequest', {"version":"1.0"})
    ET.SubElement(smr, 'RequestTimestamp').text = request_timestamp
    ET.SubElement(smr, 'MessageIdentifier').text = message_ref
    ET.SubElement(smr, 'MonitoringRef').text = data.NEXTBUSES_STOP_ID
    
    request_post_body = ET.tostring(stop_monitoring_request).decode()
    
    headers = {'Content-Type':'application/xml'}
    
    r = requests.post(data.NEXTBUSES_BASE_URL,
                      data = request_post_body,
                      headers = headers,
                      auth = requests.auth.HTTPBasicAuth(data.NEXTBUSES_API_USER, data.NEXTBUSES_API_PASS))
    
    print(r.text)
    
    return r

get_buses()
    
    


