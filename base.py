from urllib.parse import  urlsplit, parse_qs

def tidy_content(doc):
  for br in doc.xpath('//p/following-sibling::br'):
    br.getparent().remove(br)

  for noscript in doc.xpath('//noscript'):
    p = noscript.getparent()
    img = noscript.getnext()
    if img.tag == 'img':
      p.remove(img)
    p.replace(noscript, noscript[0])

  for img in doc.xpath('//img[@src]'):
    attrib = img.attrib
    attrib['referrerpolicy'] = 'no-referrer'
    if 'data-original' in attrib:
      img.set('src', attrib['data-original'])
      del attrib['data-original']

    if 'class' in attrib:
      del attrib['class']
    if 'data-rawwidth' in attrib:
      del attrib['data-rawwidth']
    if 'data-rawheight' in attrib:
      del attrib['data-rawheight']

  for a in doc.xpath('//a[starts-with(@href, "https://link.zhihu.com/?target=")]'):
    href = a.get('href')
    href = parse_qs(urlsplit(href).query)['target'][0]
    a.set('href', href)

  for a in doc.xpath('//a[starts-with(@href, "https://link.zhihu.com/?target=")]'):
    href = a.get('href')
    href = parse_qs(urlsplit(href).query)['target'][0]
    a.set('href', href)

  for a in doc.xpath('//a'):
    for k in ['rel', 'class']:
      try:
        del a.attrib[k]
      except KeyError:
        pass
