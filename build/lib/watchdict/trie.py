class TrieNode:
    def __init__(self):
        self.children = {}
        self.indexes = []

class PrefixTree:
    def __init__(self, words):
        # Store all words, including strings and integers
        self.words = words  
        self.prefix_trie = TrieNode()   # Trie for prefix search
        self.suffix_trie = TrieNode()   # Trie for suffix search (reversed words)

        # Filter the words list to include only strings for trie construction
        self._build_prefix_trie([word for word in words if isinstance(word, str)])
        self._build_suffix_trie([word for word in words if isinstance(word, str)])

    def _build_prefix_trie(self, words):
        for index, word in enumerate(words):
            node = self.prefix_trie
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.indexes.append(index)

    def _build_suffix_trie(self, words):
        for index, word in enumerate(words):
            node = self.suffix_trie
            reversed_word = word[::-1]
            for char in reversed_word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.indexes.append(index)

    def _search_prefix(self, query):
        node = self.prefix_trie
        for char in query:
            if char not in node.children:
                return []
            node = node.children[char]
        return set(node.indexes)  # Return a set of indexes matching the prefix

    def _search_suffix(self, query):
        node = self.suffix_trie
        for char in query[::-1]:  # Reverse the query to search in suffix trie
            if char not in node.children:
                return []
            node = node.children[char]
        return set(node.indexes)  # Return a set of indexes matching the suffix

    def _search_contains(self, query):
        indexes = set()
        for index, word in enumerate(self.words):
            if isinstance(word, str) and query in word:
                indexes.add(index)
        return indexes  # Return a set of indexes matching the contains query

    def _search_exact(self, query):
        # Look for an exact match in the list of words (string)
        if query in self.words:
            return {self.words.index(query)}  # Return the index of the exact match
        return set()  # Return an empty set if no match found

    def _search_exact_integer(self, value):
        indexes = {index for index, word in enumerate(self.words) if isinstance(word, (int, float)) and word == value}
        return indexes  # Return a set of indexes for integers that are exactly equal to the value

    def _search_greater_than(self, value):
        indexes = {index for index, word in enumerate(self.words) if isinstance(word, (int, float)) and word > value}
        return indexes  # Return a set of indexes for integers greater than value

    def _search_less_than(self, value):
        indexes = {index for index, word in enumerate(self.words) if isinstance(word, (int, float)) and word < value}
        return indexes  # Return a set of indexes for integers less than value

    def search(self, query):
        if not isinstance(query, str):  # Check if the input query is a string
            return []  # If not, return an empty result

        queries = query.split('|')  # Split the input string by '|'
        overall_results = set()  # To hold the results of OR queries

        for sub_query in queries:
            sub_query = sub_query.strip()
            if '&' in sub_query:  # If there's an AND condition
                and_queries = sub_query.split('&')
                result_sets = []  # To hold the sets of results for each AND query

                for q in and_queries:
                    if q.startswith('$') and q.endswith('$'):  # Exact match query
                        exact_query = q[1:-1]  # Remove the $ symbols
                        result_sets.append(self._search_exact(exact_query))
                    elif q.startswith('$'):  # Prefix query
                        prefix = q[1:]
                        result_sets.append(self._search_prefix(prefix))
                    elif q.endswith('$'):  # Suffix query
                        suffix = q[:-1]
                        result_sets.append(self._search_suffix(suffix))
                    elif q.startswith('*'):  # Contains query
                        substring = q[1:]
                        result_sets.append(self._search_contains(substring))
                    elif q.startswith('>'):  # Greater than query
                        try:
                            value = float(q[1:].strip())  # Convert to float
                            result_sets.append(self._search_greater_than(value))
                        except ValueError:
                            continue  # Ignore invalid number formats
                    elif q.startswith('<'):  # Less than query
                        try:
                            value = float(q[1:].strip())  # Convert to float
                            result_sets.append(self._search_less_than(value))
                        except ValueError:
                            continue  # Ignore invalid number formats
                    elif q.startswith('='):  # Exact integer match query
                        try:
                            value = float(q[1:].strip())  # Convert to float
                            result_sets.append(self._search_exact_integer(value))
                        except ValueError:
                            continue  # Ignore invalid number formats
                    else:
                        continue  # Ignore invalid query formats

                # Find the intersection of all result sets for AND
                if result_sets:
                    matching_indexes = set.intersection(*result_sets)
                    overall_results.update(matching_indexes)

            else:  # Handle single queries (or as a single query)
                if sub_query.startswith('$') and sub_query.endswith('$'):  # Exact match query
                    exact_query = sub_query[1:-1]  # Remove the $ symbols
                    overall_results.update(self._search_exact(exact_query))
                elif sub_query.startswith('$'):  # Prefix query
                    prefix = sub_query[1:]
                    overall_results.update(self._search_prefix(prefix))
                elif sub_query.endswith('$'):  # Suffix query
                    suffix = sub_query[:-1]
                    overall_results.update(self._search_suffix(suffix))
                elif sub_query.startswith('*'):  # Contains query
                    substring = sub_query[1:]
                    overall_results.update(self._search_contains(substring))
                elif sub_query.startswith('>'):  # Greater than query
                    try:
                        value = float(sub_query[1:].strip())  # Convert to float
                        overall_results.update(self._search_greater_than(value))
                    except ValueError:
                        continue  # Ignore invalid number formats
                elif sub_query.startswith('<'):  # Less than query
                    try:
                        value = float(sub_query[1:].strip())  # Convert to float
                        overall_results.update(self._search_less_than(value))
                    except ValueError:
                        continue  # Ignore invalid number formats
                elif sub_query.startswith('='):  # Exact integer match query
                    try:
                        value = float(sub_query[1:].strip())  # Convert to float
                        overall_results.update(self._search_exact_integer(value))
                    except ValueError:
                        continue  # Ignore invalid number formats
                else:
                    continue  # Ignore invalid query formats

        return [(self.words[i], i) for i in sorted(overall_results)]  # Return sorted results as a list

