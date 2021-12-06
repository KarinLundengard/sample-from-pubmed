
# python main.py (email)  > sample_abstracts.txt


import sys

import entrezpy.esearch.esearcher
import entrezpy.log.logger
import entrezpy.efetch.efetcher
# import random

import numpy as np
import pandas as pd



# entrezpy.log.logger.set_level('DEBUG')


# def select_sample(uids, size):
#     return random.sample(uids, size)

def select_sample(uids, size):
    return uids[::size]

def execute_search(toolname, email, query_string):
    es = entrezpy.esearch.esearcher.Esearcher(toolname, email)
    analyzer = es.inquire({
        'db': 'pubmed',
        'term': query_string,
        'rettype': 'uilist'
    })
    count = analyzer.result.count
    print(f'Number of results: {count}')
    uids = analyzer.result.uids
    if count != len(uids):
        print(f'Should have {count} UIDs but there are {len(uids)}.')
        exit(-1)
    return uids


if __name__ == '__main__':

    toolname = 'esearcher-sampler'
    tool = 'efetcher-sampler'
    email = sys.argv[1]

    query = '("last 10 years"[dp] AND english[la] NOT review[pt])' \
            ' AND ' \
            '("Computer Simulation"[MH] OR "Computer Simulation"[TIAB] OR "Mathematical Computing "[MH] OR "Mathematical Computing "[TIAB] OR "Systems Biology"[MH] OR "Systems Biology"[TIAB] OR "Models, Theoretical"[MH] OR "Theoretical Model"[TIAB] OR "Models, Biological"[MH] OR "Biological Model"[TIAB] OR "Computational Model"[TIAB])' \
            ' AND ' \
            '("Cells"[MH] OR "Cell"[TIAB])'

    #print(query)
    uids = execute_search(toolname, email, query)

    sample_uids = select_sample(uids, 200000)   #Number here means every 200000th article
    print(f'Selected sample of Pubmed IDs to check: {sample_uids}')
    n=len(sample_uids)
    print(f'Number of IDs in smaple: {n}')

    numSampleIDs = np.array(sample_uids)
    reshaped = numSampleIDs.reshape(n,1)
    pd.DataFrame(reshaped, columns=['PubMedID'])
    
    with open('sample_IDs.txt', 'w') as f:
        for item in sample_uids:
            f.write("%s\n" % item)
	    # info_sample.write("%s\n" % item)

    e = entrezpy.efetch.efetcher.Efetcher(tool,
                                          email,
                                          apikey=None,
                                          apikey_var=None,
                                          threads=None,
                                          qid=None)
    analyzer = e.inquire({'db' : 'pubmed',
                          'id' : sample_uids,
                          'retmode' : 'text',
                          'rettype' : 'abstract'})
    
    #sample_abstracts = open('sample_abstracts.txt', 'w') 
    #sample_abstracts.write(str({analyzer}))
    #sample_abstracts.close
  



