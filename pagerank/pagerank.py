import os
import random
import re
import sys
import numpy
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition_dict = {}
    list_key=[]
    all_pages = corpus.copy()
    for index in range(corpus.__len__()):
        k=all_pages.popitem()
        list_key.append(k[0])
    no_of_pages=list_key.__len__()
    for index in range(no_of_pages):
        transition_dict[list_key[index]]=(1-damping_factor)/no_of_pages
    q=corpus.pop(page)
    links=q.copy()
    corpus[page]=q
    k=links.__len__()
    for index in range(k):
        link=links.pop()
        link_value = transition_dict.pop(link)
        transition_dict[link]=link_value+damping_factor/k
    return transition_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank={}
    list_key = []
    all_page = corpus.copy()
    for index in range(all_page.__len__()):
        k = all_page.popitem()
        list_key.append(k[0])
    page = random.choice(list_key)
    rank[page]=1
    for index in range(n-1):
        model = transition_model(corpus, page, damping_factor)
        #print(model)
        priority=[]
        for index1 in range(list_key.__len__()):
            priority.append(model[list_key[index1]])
        #print(priority)
        k = random.choices(list_key,priority)
        page=k.pop()
        if rank.__contains__(page) == True:
            k=rank.pop(page)
            k=k+1
            rank[page]=k
        else:
            rank[page]=1

    rank2 = {}
    for index in range(rank.__len__()):
        k=rank.popitem()
        a=k[0]
        b=k[1]
        rank2[a]=b/n

    return rank2



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    rank={}
    transition_dict={}
    original_rank={}
    n = corpus.keys().__len__()
    pages = []
    all_page = corpus.copy()
    for index in range(all_page.__len__()):
        k = all_page.popitem()
        pages.append(k[0])
        rank[k[0]] = 1/n
    pages2=pages.copy()

    for index1 in range(pages.__len__()):

        use_page = pages2.pop()
        pages3=pages.copy()
        ans=[]
        for index2 in range(pages.__len__()):
            k=pages3.pop()
            if corpus.get(k).__contains__(use_page) == True:
                ans.append(k)
        transition_dict[use_page]=ans.copy()
    checker=pages.pop()

    pages.append(checker)
    k = pages.copy()

    for index in range(rank.__len__()):
        rank_of_page = (1 - damping_factor) / n
        page = k.pop()
        q = corpus.copy()
        p = q.get(page).copy()
        len = p.__len__()
        #print(page)
        for index in range(len):
            e = p.pop()
            rank_of_page = rank_of_page + (damping_factor * rank.get(e)) / corpus.get(e).__len__()
            #print(rank_of_page)
        original_rank[page] = rank_of_page

    while abs(rank.get(checker)-original_rank.get(checker)) > .0001 :
        k = pages.copy()
        if original_rank.__len__() > 0:
            rank = original_rank.copy()
            original_rank.clear()
        for index in range(rank.__len__()):
            rank_of_page = (1 - damping_factor) / n
            page = k.pop()
            q = transition_dict.copy()
            p = q.get(page).copy()
            len = p.__len__()
            for index in range(len):
                e = p.pop()
                rank_of_page = rank_of_page + (damping_factor * rank.get(e)) / corpus.get(e).__len__()
            original_rank[page] = rank_of_page

    return original_rank


if __name__ == "__main__":
    main()
