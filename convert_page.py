from html.parser import HTMLParser


def readstr_from_file(fn):
    fp = open(fn, "r", encoding='utf-8')
    lines = fp.readlines()
    fp.close()
    return "/n".join(lines)


class JoomlaHTMLParser(HTMLParser):
    simple_tags = ['u', 'i']
    # excluded_attrs = ['style']
    # excluded_class = "MsoNormal"
    # special_tags = ["br", "img"]

    def __init__(self):
        super(JoomlaHTMLParser, self).__init__()

        self.tag_stack = list()
        self.ps = list()
        self.p = ""

    def attr_to_str(self, attrs):
        s = ""
        for k, v in attrs:
            if k in self.excluded_attrs:
                continue
            if k == "class" and v == self.excluded_class:
                continue

            if v.find('"') >= 0:
                s += " {}='{}'".format(k, v)
            else:
                s += ' {}="{}"'.format(k, v)
        return s

    def handle_starttag(self, tag, attrs):
        if tag in self.simple_tags:
            self.p += "<{}>".format(tag)
        self.tag_stack.append([tag, attrs])

    def stack_has(self, check_tag):
        for tag, attrs in self.tag_stack:
            if tag == check_tag:
                return True
        return False

    def get_mode(self):
        if self.stack_has("h1"):
            return 1
        if self.stack_has("h2"):
            return 2
        return 0

    def handle_endtag(self, tag):
        if tag in self.simple_tags:
            self.p += "</{}>".format(tag)

        if len(self.p) > 0:
            self.ps.append([self.p, self.get_mode()])
            self.p = ""

        del self.tag_stack[len(self.tag_stack) - 1]

    def handle_data(self, data):
        data = data.strip()
        if len(data) > 0:
            self.p += data

    def to_html(self):
        s = ""
        for p, m in self.ps:
            tag = "p"
            if m == 1:
                tag = "h1"
            if m == 2:
                tag = "h2"
            if m == 3:
                tag = "h3"

            s += "<{}>{}</{}>\n".format(tag, p, tag)
        return s

# html_str = "<div><h1>test test</h1></div>"
# html_str_intro = readstr_from_file("art_intro.html")
# html_str_text = readstr_from_file("art_fulltext.html")
#
# parser = JoomlaHTMLParser()
# parser.feed(html_str_intro)
# html_str_intro = parser.to_html()
# print(html_str_intro)
#
# parser = JoomlaHTMLParser()
# parser.feed(html_str_text)
# html_str_text = parser.to_html()
# print(html_str_text)
