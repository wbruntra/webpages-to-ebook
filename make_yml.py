def make_yml(link):
    result = '''shortname: slatestarcodex.recent
    title: SlateStarCodex Recent Posts
    author: Scott Alexander
    content:
    '''
    for link in links:
        result = result + '- {}?comments=false\n'.format(link)
    return result
