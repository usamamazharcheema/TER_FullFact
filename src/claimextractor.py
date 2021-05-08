import sys
import pandas as pd
import csv
import Criteria as criteria


def get_claims(criteria):
	if (criteria.website):
		module = __import__(criteria.website)
		func = getattr(module, "get_all_claims")
		pdf = func(criteria)
		pdf.to_csv(criteria.output, encoding="utf8")