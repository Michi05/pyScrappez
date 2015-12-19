import urllib
from bs4 import BeautifulSoup
from httplib2 import iri2uri
from datetime import datetime



# The last two are installed modules (a posteriori)

#http://www.megaupload-torrent.com/index.php?f=telecharger-film

def Connect2Web():
  mainURL = "http://www.megaupload-torrent.com/index.php?f=telecharger-film&p="
  f = open('movieFile.lst.csv', 'a')
  
  i = 7010
  while i < 10301:
    time = str(datetime.now().time())
    print (time + "::Page: " + mainURL + str(i))
    moviePage = parseMoviePage(mainURL + str(i))
    f.write(formatMovieList(moviePage))
    i = i + 10

  f.close()

def parseMoviePage(currentPage):
  try:
    aResp = urllib.request.urlopen(currentPage)
  except Exception:
    print("Error: page not found: " + currentPage)
    return ""
  web_pg = aResp.read()
  soup = BeautifulSoup(web_pg)
  
  tables = soup.find_all("table")
  movieList = []
  
  for t in tables:
    theClass = t.get('class')
#    if type(theClass) != 'list':
#    if isinstance(theClass, list) and theClass.count('tfilm') > 0:
    if theClass and theClass.count('tfilm') > 0:
      movieList.append(processTable(t))
    
  return movieList
	
#      print(rows[1].firstChild.nodeValue)

def processTable(table):
  # First is the name, manually:
  if not table.tr:
    print("Table Error")
    return
  movie = {"name": table.tr.get_text()}
  # Last row has the URL, manually as well:
  rows = table.find_all("tr")
  if rows[-1].td.a:
    dossierURL = rows[-1].td.a.get('href')
    movie["url"] = getDownloadURL(dossierURL)
  for r in rows:
    movie.update(processRow(r))
#    movie['url'] = extractCell(c, 'tfilm4')
  return movie

def processRow(row):
  cells = row.find_all("td")
  return ({cellText(cells, 'tfilm3'): cellText(cells, 'tfilm39')})

def cellText(cells, className):
  for c in cells:
    if c.get('class').count(className) > 0:
      return c.get_text()
  return ""

def extractURL(cell, className):
  if cell and cell.get('class').count(className) > 0 and cell.a:
#    return cell.get_text()
    return cell.a.get('href')
  return ""

def formatMovieList(movieList):
  resultStr = ''
  for movie in movieList:
    resultStr += movie["name"].strip()
    resultStr += ";" + movie["Date sortie :"].strip()
    resultStr += ";" + movie["Genre :"].strip()
    resultStr += ";" + movie["Langue :"].strip()
    resultStr += ";" + movie["Dureé :"].strip()
    resultStr += ";" + movie["url"].strip()
    resultStr += "\r\n"
    
#  print(movie)
#  print("***********")
#  print(resultStr)
  return resultStr

def getDownloadURL(dossierURL):
  dossierURL = "http://www.megaupload-torrent.com/" + iri2uri(dossierURL)
  try:
    aResp = urllib.request.urlopen(dossierURL)
  except Exception:
      return "**" + dossierURL
  web_pg = aResp.read()
  soup = BeautifulSoup(web_pg)

  all_links = soup.find_all("a")
  for link in all_links:
    if link.img and link.parent and ("Télécharger" in link.parent.get_text()):
      return link.get('href')

Connect2Web()
