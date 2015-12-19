#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from httplib2 import iri2uri
from datetime import datetime
from pyquery import PyQuery as pQuery
import unicodedata
import json
import sys  # For the cmd line args
import os.path as path  # For checking the existence of the files

#######################################################
#
# This will become a generic class or library for parsing web pages
# and export them as JSON. It's meant to be used generically by
# sort of spiders or macro-style automatizing applications
#
#######################################################

## TODO for prices: finalPrice = price0[1]=="m"?+price0[0]:4.357*price0[0]
## price.textContent.replace("£", "").split("p")

DEBUG_MODE = True

def connect2Web_main(cfgFileName = "pyTest input.json"):
    """The first function/method handles the initial connection.
    To be decided how generic; maybe it can take a treatment function as parameter
    :returns: void
    :rtype: void
    """
    indexKinds = {#"INTEGER": [str(100 + i)[-2:] for i in range(10)],
                  "INTEGER": [str(i)+".html" for i in range(1,48)],
                  "ALPHABETIC": [chr(i) for i in range(ord("A"), ord("B") + 1)],
                  "QUERY_DRIVEN": []
    }

    debMsg("Loading config from file: " + cfgFileName, "connect2Web_main")
    cfg = loadConfiguration(cfgFileName)
    if cfg is None or not verifyConfigIntegrity(cfg):
        print("Unable to use loaded Configuration. Exit application.")
        return None
    mainURL = str(cfg["url_base"])
    fileName = str(cfg["output_filename"])
    urlGenerator = iteraPage(mainURL,
                             kindOfIndex=indexKinds[cfg["url_mode"]],
                             cfg = cfg)


    debMsg("Created initial values from config:" +
           "\r\n\t Web mainURL: " + mainURL +
           "\r\n\t Target fileName: " + fileName,
           "mainURL")
    connect2Web(fileName, urlGenerator, cfg = cfg)

def verifyConfigIntegrity(cfg):
    try:
        for param in ["url_mode", "jQuery_base", "jQuery_mapping"]:
            assert param in cfg
    except Exception as e:
        print("ERROR on configuration verification: <<" + str(e.message) + ">>")
    return cfg

def readElement(elem, query, attribute):
    if (attribute is None or attribute == ""):
        return (elem(query).text() or "")
    else:
        return (elem(query).attr(attribute) or "")

def connect2Web(fileName, urls, cfg):
    # Encapsulate this...
    if path.isfile(fileName):
        p, n, base = fileName.find("."), 2, fileName
        while path.isfile(fileName):
            fileName = base[:p] + "[" + str(n) + "]" + base[p:]
            n += 1

    outFile = open(fileName, 'a')  # I use append bc the above could fail during dev
    query_map = cfg["jQuery_mapping"]
    sorted_field_queries = [query_map[fieldname] for fieldname in query_map]
    outFile.write(arrayToCSV([fieldname for fieldname in query_map]).encode('ascii', 'ignore'))
    next_url = cfg["url_base"]
    while urls.incIndex(next_url):
        debMsg("Processing page: " + urls.getURL())
        webHTML = getWebHTML(urls.getURL())
        myPQ = pQuery(webHTML)
        query_next, attrib = cfg["url_jQuery_next_page"]
        next_url = "https://www.gumtree.com" + readElement(myPQ, query_next, attrib)
        for node in myPQ(cfg["jQuery_base"]).items():
            fieldValues = [readElement(node, query, attrib) for query, attrib in sorted_field_queries]
            outFile.write(arrayToCSV(fieldValues).encode('ascii', 'ignore'))
        print "Page written to file."
    outFile.close()


def loadConfiguration(cfgFileName):
    """
    I encapsulate this even if short so it is structured for future changes.

    :param cfgFileName: json config file name
    :return: data structure with the configuration
    """
    try:
        with open(cfgFileName) as json_cfg:
            cfg = json.load(json_cfg)
            return cfg
    except Exception as e:
        print("ERROR <<" + str(e.message) + ">> while trying to read configuration from file: " + str(cfgFileName))
        return None

def arrayToDictionary(rowList):
  resultStr = ''
  for row in rowList:
    resultStr += row["name"].strip()
    resultStr += ";" + row["Date sortie :"].strip()
    resultStr += ";" + row["Genre :"].strip()
    resultStr += ";" + row["Langue :"].strip()
    resultStr += ";" + row["Dureé :"].strip()
    resultStr += ";" + row["url"].strip()
    resultStr += "\r\n"
  return resultStr

def arrayToCSV(dataInList, separator=";"):
    resultStr = ''
    for value in dataInList:
        resultStr += "\"" + value + "\"" + separator
    return resultStr[0:-1] + "\r\n"

def getWebHTML(currentPage):
    try:
        aResp = urllib.urlopen(currentPage)
        web_pg = aResp.read()
        return web_pg
    except Exception as e:
        print("Error: " + str(e.message))
        return ""

def debMsg (msg, tag="debugMsg"):
    if DEBUG_MODE is False:
        return
    time = str(datetime.now().time())
    tag = "" if tag is None else str(tag) + "::"
    print(time + ":: " + str(msg))

class fieldMapping:
    """Contains needed methods (data and functions) to handle the mappings from the page into named fields."""
    def __init__(self, currentNode, sorted_field_queries):
        self.node = currentNode
        self.maps = sorted_field_queries
        self.active = True

class iteraPage:
    """Generates the first and subsequent URLs on which to iterate"""

    def __init__(self, baseURL, kindOfIndex, cfg):
        self.baseURL = baseURL  # instance variable unique to each instance
        self.index = self.firstIndex()
        self.cfg = cfg
        self.mode = cfg["url_mode"]
        self.next_url = ""

        if kindOfIndex is None:
            kindOfIndex = []
        self.kindOfIndex = kindOfIndex
        self.limit = len(self.kindOfIndex) - 1

    def firstIndex(self):
        return -1

    def incIndex(self, next_url=""):
        if self.mode == "QUERY_DRIVEN":
            self.next_url = next_url
            return next_url is not None and next_url != ""
        if self.index == self.limit:
            return False
        else:
            self.index += 1
            return True

    def getSufix(self):
        return self.kindOfIndex[int(self.index)]

    def getURL(self):
        if self.mode == "QUERY_DRIVEN":
            return self.next_url
        return self.baseURL + self.getSufix()

config = sys.argv[1] if (len(sys.argv) > 1) else None
connect2Web_main(config)
