sub = set()
urls = set()
with open('filtered_1M_webrank') as f:
    line = f.readline()
    while line:
        url = line.split()[1]
        urls.add(url)
        sub_queries = url.split('.')
        queries = list(reversed(['.'.join(sub_queries[i:]) for i in range(len(sub_queries))]))
        if len(sub_queries[-1]) == 2:
            print(sub_queries)
        for q in queries:
            sub.add(q)
        line = f.readline()

print(len(sub.difference(urls)))