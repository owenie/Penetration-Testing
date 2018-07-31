#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
from http import cookiejar
from bs4 import BeautifulSoup
import re

class HtmlOutputer():

	def __init__(self):
		self.data = []

	def collect_data(self, data):
		if data is None:
			return
		self.data.append(data)

	def output_html(self):
		fout = open('output.html', 'w')
		fout.write('<html>')
		fout.write('<body>')
		fout.write('<table>')
		#ascii
		for data in self.data:
			fout.write('<tr>')
			fout.write('<td>%s</td>' % data['url'])
			fout.write('<td>%s</td>' % data['title'])
			fout.write('<td>%s</td>' % data['summary'])
			fout.write('</tr>')
		fout.write('</table>')
		fout.write('</body>')
		fout.write('</html>')
		fout.close()