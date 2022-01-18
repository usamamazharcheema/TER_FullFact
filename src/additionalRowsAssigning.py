import sys
import Claim as claim_obj
import assigningIndToSummarizedClaims

#Fonction qui récupère les claims (ainsi que leurs métadonnées) additionnelles se trouvant sur la même page et ayant été traités par la même revue.
def briefAdditionalRowsAssigning(soup, url, individual_claim):
	claim = soup.find('div', {"class": "card-body card-claim-body"})
	if claim:
		claim_ = claim_obj.Claim()
		claim_.setSource("fullfact")
		claim_.setUrl(url)
		summarized_claim = claim.get_text().replace("\nWhat was claimed\n", "")
		claim_.setClaim(summarized_claim)

		claim_.setIndClaim(individual_claim)

		Jcard_similarity = assigningIndToSummarizedClaims.cosine_sim(summarized_claim,
																						 individual_claim)
		claim_.setSimilarity(Jcard_similarity)
		# claim_.setIndId(Ind_id)

		return claim_
	else:
		return "empty"