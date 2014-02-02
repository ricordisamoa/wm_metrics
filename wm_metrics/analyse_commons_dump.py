# -*- coding: utf-8 -*-

import xml.dom.minidom
import re
import datetime


def handle_node(node, tag_name):
    """Return the contents of a tag based on his given name inside of a given node."""
    element = node.getElementsByTagName(tag_name)
    if element.length > 0:
        if element.item(0).hasChildNodes():
            return element.item(0).childNodes.item(0).data.rstrip()
    return ""


def timestamp_to_date(date):
    """Return a date object representing the given MediaWiki timestamp."""
    return datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))


def parse_xml_dump(xml_dump):
    """Return a list of the edits in a Wikimedia Commons dump."""
    edits = []
    revision_categories = {}
    doc = xml.dom.minidom.parse(xml_dump)
    for mediawiki_node in doc.childNodes:
        if mediawiki_node.localName == u'mediawiki':
            for page_node in mediawiki_node.childNodes:
                for revision_node in page_node.childNodes:
                    title = handle_node(page_node, u'title')
                    revision_categories[title] = []
                    if revision_node.localName == u'revision':
                        username = handle_node(revision_node, u'username')
                        timestamp = handle_node(revision_node, u'timestamp')
                        text = handle_node(revision_node, u'text')
                        edits.append((username, timestamp_to_date(timestamp), title))
                        #cats = get_categories_from_text(text)
                        #revision_categories[title].append(cats)
    return edits


def get_categories_from_text(edit):
    """Return the categories contained in a given wikitext."""
    cat_pattern = r"\[\[Category:(?P<cat>.+?)(\|.*?)?\]\]"
    return map(lambda x: x[0], re.findall(cat_pattern, edit))


def analyse_edits(edits, bottomDate, topDate):
    all_pages = list(set(map(lambda x: x[2], edits)))

    #print allPages
    edits_filtered = filter(lambda x: bottomDate < x[1] < topDate, edits)
    edits_filtered = edits
    usernames = set(map(lambda x: x[0], edits_filtered))
    page_edited = list(set(map(lambda x: x[2], edits_filtered)))

    text = "Sur la période considérée, %s modifications ont été effectuées" \
           "par %s utilisateurs sur %s documents distincts "
    print text % (len(edits_filtered), len(usernames), len(page_edited))
    user_contribs = {}
    for username in usernames:
        user_contribs[username] = map(lambda x: x[1], filter(lambda x: x[0] == username, edits_filtered))
    return user_contribs


def make_edits_analysis(xml_file):
    edits = parse_xml_dump(xml_file)
    start_date = datetime.datetime(2009, 1, 1)
    end_date = datetime.datetime(2013, 10, 31)
    username_blacklist = u'TrutatBot'
    user_contribs = analyse_edits(edits, start_date, end_date, username_blacklist)
    #print user_contribs
    for user in user_contribs.keys():
        print "%s : %s" % (user, len(user_contribs[user]))

def main():
    ##dummy_xml_file = "/home/jfk/Tuile/wm_metrics/tests/data/example_dump.xml"
    xml_file = "data/Wikimedia+Commons-20131208151654.xml"
    make_edits_analysis(xml_file)

if __name__ == "__main__":
    main()