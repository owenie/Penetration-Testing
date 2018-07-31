#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
from http import cookiejar
from bs4 import BeautifulSoup
import re

class HtmlDownloader():

	def download(self,url):
		if url is None:
			return

		req = urllib.request.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
		response = urllib.request.urlopen(req)
		if response.getcode() != 200:
			return None
		html = response.read().decode('utf-8')
		return html