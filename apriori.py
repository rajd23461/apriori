import pandas as pd
from itertools import chain, combinations

def apriori(df, outcome_column, min_support, min_confidence):
    def subsets(arr):
        """ Returns non-empty subsets of arr"""
        return chain(*[combinations(arr, i + 1) for i, _ in enumerate(arr)])

    def join_set(itemset, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == length])

    def itemset_support(transaction_list, itemset):
        """Calculates the support for items in the itemset"""
        tl_subset = [transaction for transaction in transaction_list if itemset.issubset(transaction)]
        return float(len(tl_subset)) / len(transaction_list)



    # Convert DataFrame to list of transactions
    transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()
    

    itemset = set()
    transaction_list = list()
    freq_itemset = dict()

    # Load the dataset
    for transaction in transactions:
        transaction_set = frozenset(transaction)
        transaction_list.append(transaction_set)
        for item in transaction_set:
            itemset.add(frozenset([item]))  # Generate 1-itemSets

    # Generate frequent itemsets
    curr_itemset = set(itemset)
    k = 2
    while curr_itemset:
        # Calculate itemset support and prune itemsets that are not frequent or do not contain an Outcome item
        curr_itemset = set([item for item in curr_itemset if itemset_support(transaction_list, item) >= min_support])
        freq_itemset[k-1] = curr_itemset
        curr_itemset = join_set(curr_itemset, k)
        k += 1

    # Generate rules
    rules = list()
    for key, value in freq_itemset.items():
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = itemset_support(transaction_list, item) / itemset_support(transaction_list, element)
                    if confidence >= min_confidence:
                        rules.append(((tuple(element), tuple(remain)), confidence))
    return rules
