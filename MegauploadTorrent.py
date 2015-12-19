import html5lib
import urllib

#http://www.megaupload-torrent.com/index.php?f=telecharger-film

def Connect2Web():
  aResp = urllib.request.urlopen("http://www.megaupload-torrent.com/index.php?f=telecharger-film");
  web_pg = aResp.read();
  
  domTree = html5lib.parse(web_pg, treebuilder="dom")
  tables = domTree.getElementsByTagName("table")  
  
  for t in tables:
    if t.hasAttribute("class") and t.getAttribute("class") == "tfilm":
      for c in t.childNodes:
        rows = c.childNodes
        rows2dict(rows)
#      print(rows[1].firstChild.nodeValue)

def rows2dict(rows):
  for row in rows:
    cells = row.childNodes
    print(row.lastChild)
    print("***********************")
    print(row.toprettyxml())
    for cell in cells:
      print(">>>>>")
      print(cell.toprettyxml())
      return
      
#    print(row.toprettyxml())

Connect2Web()
