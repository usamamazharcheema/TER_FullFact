# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
sys.path.append('ce')

import claimextractor as ce
import Criteria 


def main(argv):
	options={} 
	criteria = Criteria.Criteria()
	criteria.setOutput("output_got.csv")

	if len(argv) == 0:
		print("nb d'arguments non valides")
		return


	try:
		opts, args = getopt.getopt(argv, "", ("website=", "since=", "until=", "maxclaims=", "output=","language=","html="))

		
		
		for opt,arg in opts:
			if opt == '--website':
				#criteria.website= arg
				criteria.setWebsite(criteria, arg)

			elif opt == '--since':
				criteria.since= arg

			elif opt == '--until':
				criteria.until = arg

			elif opt == '--maxclaims':
				criteria.maxClaims = int(arg)

			elif opt == '--language':
				criteria.language = arg

			elif opt == '--output':
				#criteria.output = arg
				criteria.setOutput(arg)
			elif opt == '--html':
				criteria.html = True

	except:
		print('Arguments parser error, try -h')
	
	ce.get_claims(criteria)
	print('Done. Output file generated "%s".' % criteria.output)

if __name__ == '__main__':
	main(sys.argv[1:])