import sys
import pandas as pd
import csv
current_websites={
	"english":["fullfact","snopes"],
	"portuguese":["aosfatos","lupa","publica","efarsas"],
	"german":["mimikama"] 
}

def get_sites():
	print (current_sites)


def get_claims(criteria):
	if (criteria.website):
		module = __import__(criteria.website)
		func = getattr(module, "get_all_claims")
		pdf = func(criteria)
		print("module")
		pdf.to_csv(criteria.output, encoding="utf8")