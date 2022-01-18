from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.error
# import Claim as claim_obj

class IndividualClaimExtraction:


    def getIndClaims(soup):


        # try:
        #     p = urlopen(url).read()
        # except urllib.error.URLError as e:
        #     print(e.__dict__)
        # soup = BeautifulSoup(p, 'html.parser')
        block_quote = soup.find_all(lambda tag: tag.name == 'blockquote' and not tag.attrs)
        # claim_ = claim_obj.Claim()
        return_list=[]
        if block_quote:

            for claim in block_quote:
                concat = ""
                paragraphs = claim.find_all('p')
                len_paragraph = len(paragraphs)
                for link in paragraphs:

                    concat_text = link.get_text()

                    concat = concat + '\n' + concat_text

                    if link.select('a'):
                        if len_paragraph < 2:

                            if ('—') in concat_text:
                                individual_claim = "\n".join(concat.split('—')[0:-1])
                                link_content = concat.split('—')[-1]

                            elif ('”') in concat_text:
                                individual_claim = "\n".join(concat.split('”')[0:-1])
                                link_content = concat.split('”')[-1]
                            else:
                                individual_claim = "\n".join(concat.split('"')[0:-1])
                                link_content = concat.split('"')[-1]

                            if individual_claim:

                                return_list.append(individual_claim[1:])
                                # claim_.setIndClaim(individual_claim[1:])

                            a_link = [a['href'] for a in link.select('a')]


                            individual_claim_source = link_content + ' \n' + a_link[0]
                            if individual_claim_source:
                                # claim_.setIndClaimSource(individual_claim_source)
                                return_list.append(individual_claim_source)

                            concat = ""

                        elif len_paragraph%2==1:
                            individual_claim = "\n".join(concat.split('”')[0:-1])

                            if individual_claim:
                                #   print(individual_claim)
                                return_list.append(individual_claim[1:])

                                # claim_.setIndClaim(individual_claim[1:])
                                a_link = [a['href'] for a in link.select('a')]
                                link_content = concat.split('”')[-1]
                                individual_claim_source = link_content + ' \n' + a_link[0]
                                if individual_claim_source:
                                    # claim_.setIndClaimSource(individual_claim_source)
                                    return_list.append(individual_claim_source)
                                concat = ""



                        else:
                            individual_claim = "\n".join(concat.split('\n')[0:-1])

                            if individual_claim:
                                #   print(individual_claim)
                                return_list.append(individual_claim[1:])

                                # claim_.setIndClaim(individual_claim[1:])

                            a_link = [a['href'] for a in link.select('a')]
                            link_content = concat.split('\n')[-1]
                            individual_claim_source = link_content + ' \n' + a_link[0]
                            if individual_claim_source:
                                # claim_.setIndClaimSource(individual_claim_source)
                                return_list.append(individual_claim_source)
                            concat = ""
                    elif len_paragraph==1:
                            if concat_text:
                                footer = claim.find('footer')
                                if not footer:
                                    return_list.append(concat_text[1:-1])
                                    # claim_.setIndClaim(concat_text[1:-1])
                                    # claim_.setIndClaimSource("empty")
                                    return_list.append("empty")




                        #print(concat_text[1:-1])


                footer = claim.find('footer')
                if footer:
                    link = footer.find('a')
                    if link:

                        if concat:
                            individual_claim = concat[1:]
                            # print(individual_claim)
                            return_list.append(individual_claim)
                            # claim_.setIndClaim(individual_claim)
                            individual_claim_source = footer.get_text() + " \n" + link['href']
                            return_list.append(individual_claim_source)

                            # claim_.setIndClaimSource(individual_claim_source)
                    else:
                        if concat_text:
                                return_list.append(concat_text[1:-1])
                                # claim_.setIndClaim(concat_text[1:-1])
                                # claim_.setIndClaimSource("empty")
                                return_list.append("empty")


            return return_list
        else:
            return "empty"

    #
    # aa=getIndClaims("https://fullfact.org/education/research-doesnt-prove-short-breaks-school-cause-poorer-pupil-attainment/")
    # print(aa)
