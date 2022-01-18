def get_claims(criteria):
	if (criteria.website):
		module = __import__(criteria.website)
		func = getattr(module, "get_all_claims")
		pdf = func(criteria)
		pdf.to_csv(criteria.output, encoding="utf8")

def get_claimskg(criteria):
	if (criteria.websitekg):
		module = __import__(criteria.websitekg)
		func = getattr(module, "get_all_claimskg")
		pdf = func(criteria)
		pdf.to_csv(criteria.output, encoding="utf8")

def get_claimsAssign(criteria):
	if (criteria.websiteAssign):
		module = __import__(criteria.websiteAssign)
		func = getattr(module, "get_all_claimsAssign")
		pdf = func(criteria)
		pdf.to_csv(criteria.output, encoding="utf8")