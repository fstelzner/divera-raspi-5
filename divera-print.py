#!/usr/bin/python3
# Depeche als PDF anlegen

import requests
from fpdf import FPDF
from datetime import datetime

def fetch_json_data(url, accesskey):
  params = {
      'accesskey': accesskey
  }
  try:
      response = requests.get(url, params=params)
      response.raise_for_status()
      json_data = response.json()
      return json_data
  except requests.exceptions.HTTPError as http_err:
      print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.RequestException as req_err:
      print(f"Request error occurred: {req_err}")
  except ValueError as json_err:
      print(f"JSON decoding error: {json_err}")



def check_log_for_pdf(log_file_path, search_string):
    try:
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
            if search_string in log_content:
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"Log file {log_file_path} not found.")
        return False


# Beispiel-URL und Access-Key
url = "https://app.divera247.com/api/last-alarm"
accesskey = "[DEIN DIVERA API KEY]"

data = fetch_json_data(url, accesskey)

if data['success']==True:
  dt = datetime.fromtimestamp(data['data']['ts_create'])
  time = dt.strftime('%d.%m.%Y %H:%M:%S')

  text = str(data['data']['text']).replace('\n', '<br><br>')


  class PDF(FPDF):
    pass

  depeche="""
  <p align="center">
  Alarmdepeche<br>
  VS - NUR FÜR DEN DIENSTGEBRAUCH<br>
  Divera API / Kooperative Leitstelle West<br>
  </p><br>
  <p align="center">------------------------</p>
  <p>&nbsp;</p>
  <table width="100%">
  <tr>
  <th width="33%" align="center">Alarmierungszeit</th>
  <th width="33%" align="center">Einsatznummer</th>
  <th width="33%" align="center">Author-ID</th>
  </tr>
  <tr>
  <td align="center">"""+str(time)+"""</td>
  <td align="center">"""+str(data['data']['foreign_id'])+"""</td>
  <td align="center">"""+str(data['data']['author_id'])+"""</td>
  </tr>
  </table><br>
  <p align="center">------------------------</p>
  <p>
  Einsatzszenario: """+str(data['data']['title'])+"""<br>
  Einsatzinfo: """+text+"""
  </p>
    <p>
  Adresse: """+str(data['data']['address'])+"""<br><br>
  Lat: """+str(data['data']['lat'])+"""<br>
  Lng: """+str(data['data']['lng'])+"""<br>
  </p>

  """
  log_file_path = '/home/pi/divera/depechen/archive/depeche.log'
  pdfpath = '/home/pi/divera/depechen/'
  pdffilename = dt.strftime('%Y-%m-%d')+'-'+str(data['data']['id'])+'-depeche.pdf'
  already_printed = True
  already_printed = check_log_for_pdf(log_file_path, pdffilename)

  if not already_printed:
    pdf = PDF()
    pdf.add_page()
    pdf.write_html(depeche)
    pdf.output(pdfpath+pdffilename)
#else:
#  print('Kein Alarm zum Drucken')
