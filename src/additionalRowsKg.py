import sys
import kgClaim as claim_obj

#Fonction qui récupère les claims (ainsi que leurs métadonnées) additionnelles se trouvant sur la même page et ayant été traités par la même revue.
def briefAdditionalRowsKg(claimReview_Reviewed, url, t):

	if claimReview_Reviewed :
		claim_ =  claim_obj.kgClaim()
		claim_.setClaimReviewUrl(url)
		claim_.setClaim(claimReview_Reviewed)
		claim_.setTitle(t)
		# claim_.setCreativeWorkName("empty")
		# claim_.setRating_alternateName("empty")
		return claim_
	else:
		return "empty"