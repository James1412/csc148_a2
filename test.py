prefix= ['c','a']
item_chars= ['c', 'a', 't']
if all(item_chars[i] == prefix[i] for i in range(len(prefix))):
    print('good')
else:
    print('bad')
