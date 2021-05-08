# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
sys.path.append('ce')

import claimextractor as ce
import Criteria 



def main(argv):
	options={} 
	criteria = Criteria.Criteria()
	criteria.setOutput("output_got.csv")

	


	try:

		opts, args = getopt.getopt(argv, "", ["website=", "maxclaims=", "output="])
		for opt, arg in opts:
			if opt == '--website':
				criteria.setWebsite(arg)


			if opt == '--maxclaims':
				criteria.setMaxClaims(int(arg))

			if opt == '--output':
				criteria.setOutput(arg)


	except:
		print('Arguments parser error, try -h')
	
	ce.get_claims(criteria)
	print('Done. Output file generated "%s".' % criteria.output)

if __name__ == '__main__':
	main(sys.argv[1:])