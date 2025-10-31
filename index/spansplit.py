

with open('span.txt', 'r') as f:
    spans = f.readlines()

print(type(spans))

spansbkd = [span.split(' ') for span in spans]

print(len(spansbkd[0]) , len(spansbkd[1]))