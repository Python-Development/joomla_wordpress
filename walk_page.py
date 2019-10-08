
from lxml import etree
import lxml.html

t = lxml.html.fromstring("<div><h1 class='h11'>test test</h1></div>")
s = t.text_content()
print(s)

html_str = "<div><h1 class='h11'>test test</h1></div>"
html_str2 = "<div><img src='/images/image1.jpg'/><p><img src='/images/image1.jpg'/>tes btest </p></div>"

# wp_content/images

tree = etree.fromstring(html_str)
root = tree

tree2 = etree.fromstring(html_str2)


def tag_attribs(tag):
    s = ""
    for k in tag.attrib:
        s += k+":"+tag.attrib[k]
    return s


def walk_tags(html_tags):
    ll = list()
    if html_tags.getchildren():
        for child in html_tags:
            ll.append(walk_tag(child))
    return ll


def walk_tag(html_tag):
    sub_list = walk_tags(html_tag)
    if len(sub_list) > 0:
        return {html_tag.tag: sub_list}
    return {html_tag.tag: html_tag.text+" attr:"+tag_attribs(html_tag)}


print(walk_tag(root))

tags_img = tree2.xpath('//img')
for t in tags_img:
  t.attrib["src"] = t.attrib["src"].replace("images", "wp_content/images")

print(etree.tostring(tree2))  # , pretty_print=True
