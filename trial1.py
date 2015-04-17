from pytagcloud import create_tag_image, make_tags, LAYOUT_MOST_HORIZONTAL
from pytagcloud.lang.counter import get_tag_counts


text = "A tag cloud is a visual representation for text data, typically\
used to depict keyword metadata on websites, or to visualize free form text."

t= "Hi my name is Shridhar. Shridhar is my name"

j= " Note Note Note Note how the left-hand side is a white white white margin and the word 'respect' gets cut off the at right-hand side. I've also noticed this happening at the bottom side as well, particularly with words that are longer and vertically aligned"

#tags = make_tags(get_tag_counts(YOUR_TEXT), maxsize=120)

max_tags = 100
tags = make_tags(get_tag_counts(j)[:max_tags], minsize=1,  maxsize=60)
size = (1024, 500)

create_tag_image(tags, 'cloud1.png', size=(1000, 1000), background=(0,0,0,255) ,fontname='Lobster', rectangular= True, layout= LAYOUT_MOST_HORIZONTAL)

#import webbrowser
#webbrowser.open('cloud_large1.png') # see results
