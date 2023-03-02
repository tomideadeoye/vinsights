import openai
from PyPDF2 import PdfReader
import re
import os

from memogenerator.utils import TomideBeautifulSoupUtils, google_search, TomsEmailUtilities, create_document
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_mad_memo(company_name, company_website, pitch_deck, email_to):
    
    directory = './mediafiles/Africa/'
    pitch_deck = 'Pivo Pitch Deck - Main (1).pdf'

    reader = PdfReader(f'{directory}{pitch_deck}')
    pitch_deck_content = ' '.join(
        [page.extract_text().strip() for page in reader.pages])

    print(company_name, company_website, pitch_deck, email_to)
    website_content = TomideBeautifulSoupUtils.tomide_bs4_make_soup(
        company_website, 'incognitp', False)
    print('website_content', website_content)
    dataset = pitch_deck_content + website_content[0].text.strip()

    print(
        f'Deck: {len(pitch_deck_content)} | Website: {len(website_content[0].text.strip())} | Dataset: {len(dataset)} / Token: {len(dataset) / 4}')

    dataset = ' '.join([dataset.replace(thing, '') for thing in [
                       '\n', 'all rights reserved', '©', '®', '™', ]])
    dataset = ' '.join(dataset.split()[0:1200])
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', dataset)

    founder_google_search = ''.join(founder['snippet'] + ' ' + founder['htmlSnippet']
                                    for founder in google_search(f'{company_name} startup founders'))
    founder_google_search = founder_google_search.strip().replace('<b>',
                                                                  '').replace('</b>', '')

    funding_raise_google_search = ''.join(
        funding['snippet'] + ' ' + funding['htmlSnippet'] for funding in google_search(f'{company_name} funding raise'))
    funding_raise_google_search = funding_raise_google_search.strip().replace('</b>',
                                                                              '').replace('<b>', '')

    class Prompts:
        what_they_do = "extract what the company does from the data here "

        hundred_x_justification = "based on the available data how can the company make 100x return? What will it have to be valued at to make that return? Is the market large enough to allow the company to grow to a 100x? And does the company and the team have what it takes to attain that feat?"
        traction = "extract traction from the data here Is the product at MVP or further. How far along in development are they?"

        team = "extract founders names and details from the data here"
        founder_vision = "extract founder's vision from the data here What is the founder’s vision for the company or market and why? What are the founder's motivation and what drives them?"

        business_model = "extract business model from the data here How does the company make its money?"
        funding = "extract funding from the data here"
        use_of_funds = "extract use of funds from the data here What does the team plan to use this raise for? "

        industry = "extract industry from the data here What industry is the company in?"
        market = "extract market from the data here General Market outlook What is the size of the market? How has it grown over time? What portion of the market has the company decided that they can service?"
        risks = 'What are the risks that come with this company? A risk in their product, service, or business model? What could make it fail? What do they need to get absolutely perfect to ensure they succeed?'

        products = "extract the company's product from the data here What is the Product/Service they are providing?"
        revenue = "extract revenue from the data here"
        growth = "extract growth from the data here"
        competition = "extract competition from the data here"
        exit_opp = "extract exit from the data here"

        contact = "extract contact phone and emailfrom the data here"
        website = "extract website from the data here"
        location = "extract the company's location from the data here"

    class QueryGpt:
        def __init__(self, query, dataset):
            self.query = query
            self.dataset = dataset

        def query_gpt(self):
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.query + '' + self.dataset,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)
            print(response.choices[0].text.strip())
            return response.choices[0].text.strip() + '\n'

    class MemoCreator:
        def memoCreate():

            memo = f'''
<=====================INVESTMENT MEMO=====================> \n

WHAT THEY DO:
=========================================================== \n 
{QueryGpt(Prompts.what_they_do, dataset).query_gpt()}  

DECK | WEBSITE 
=========================================================== \n 
{company_website if company_website else QueryGpt(Prompts.website, dataset).query_gpt()}

ROUND DETAILS
===========================================================  \n
Terms: How much are we investing and what valuation?
Stage: Pre-Seed/Seed/Series ABC?
Co-Investors: If any?
Information Rights: 
Pro-Rata:
City: {QueryGpt(Prompts.location, dataset).query_gpt()}
Sex:
Industry: {QueryGpt(Prompts.industry, dataset).query_gpt()}   

TRACTION AND PROGRESS SO FAR:
=========================================================== \n 
{QueryGpt(Prompts.traction, dataset).query_gpt()}

Founders: Founder Info from Linkedin and Execution Ability
Are they repeat founders? Do they have other things going on? Do they have what it takes to achieve their vision?
# pull data from Linkedin previously listed companies 
{QueryGpt(Prompts.team, founder_google_search).query_gpt()}

BUSINESS MODEL
=========================================================== \n
{QueryGpt(Prompts.business_model, dataset).query_gpt()} 

FOUNDER'S VISION
=========================================================== \n
{QueryGpt(Prompts.founder_vision, founder_google_search).query_gpt()} 

FUNDING:
=========================================================== \n
{QueryGpt(Prompts.funding, funding_raise_google_search).query_gpt()} 

USE OF FUNDS:
=========================================================== \n
{QueryGpt(Prompts.use_of_funds, dataset).query_gpt()}

PRODUCT/SERVICE:
=========================================================== \n
{QueryGpt(Prompts.products, dataset).query_gpt()} 

CONTACTS:
=========================================================== \n
{QueryGpt(Prompts.contact, dataset).query_gpt()} 
emails: {' | '.join(emails)}

MARKET OUTLOOK:
=========================================================== \n
{QueryGpt(Prompts.market, dataset).query_gpt()}

COMPETITION & DEFENSIBILITY:
=========================================================== \n
Who is their competition? How do they compare against each other? What is unique about this company that makes them stand out in the market? Feel free to use a table here to help compare
# go online to fetch the data here and use exiting companies in the database

RISKS:
=========================================================== \n
{QueryGpt(Prompts.risks, dataset).query_gpt()}

SOCIALS:
=========================================================== \n
{' | '.join(website_content[1]['social_media_links'])}

OTHER LINKS:
=========================================================== \n
{' | '.join(website_content[1]['internal_links'])}

    '''

            return memo

    response = MemoCreator.memoCreate()
    if email_to:
        subject = f'Investment Memo for {company_name}'

        document_name = create_document(
            f'''{company_name.upper()} Investment Memo Draft''', subject)

        # TomsEmailUtilities.send_email(email_to, subject, response, [document_name])

    return MemoCreator.memoCreate()
