from anytree import Node, RenderTree

from anytree import NodeMixin, RenderTree
from nltk.stem import PorterStemmer
porter = PorterStemmer()

from nltk.corpus import stopwords


def stem_tokens(token_words):
    stemmed_tokens = []
    filtered_words = [word for word in token_words if word not in stopwords.words('english')]

    for word in filtered_words:
        stemmed_tokens.append(porter.stem(word))
    print(stemmed_tokens)

    return stemmed_tokens


def read_file(file_name):
    product_name = open(file_name, 'r')
    list_char = [',','.','\t','\n']
    cleaned_text = [''.join([i for i in line if not i.isdigit() and i not in list_char ]) for line in product_name.readlines()]
    cleaned_text = [line.replace('_', ' ') for line in cleaned_text]
    print(cleaned_text)

    file_tokens = [line.strip().lower() for line in cleaned_text]
    file_tokens = ' '.join(file_tokens).split(' ')
    file_tokens = stem_tokens(file_tokens)
    return file_tokens



class MyBaseClass(object):  # Just an example of a base class
    foo = 4

class MyNode(MyBaseClass, NodeMixin):  # Add Node feature
    def __init__(self, name,keywords=[], question="",degree='', parent=None, children=None):
        super(MyBaseClass, self).__init__()
        self.name = name
        self.question = question
        self.degree = degree
        self.parent = parent
        self.keywords = keywords
        
        if children:
            self.children = children


lap_keywords = read_file('laptop.txt')
book_keywords = read_file('book.txt')

clothes_keywords = read_file('clothes.txt')
shoes_keywords = read_file('shoes.txt')
pants_keywords = read_file('pants.txt')
jacket_keywords = read_file('jacket.txt')
study_lap_keywords = read_file('study_lap.txt')
business_lap_keywords = read_file('business_lap.txt')
gaming_lap_keywords = read_file('gaming_lap.txt')
travel_books_keywords = read_file('Travel_books')
biographies_keywords = read_file('Biographies_keywords')
mystery_keywords = read_file('mystery_keywords')
Scifi_bookskeywords = read_file('Scifi_bookskeywords')
general_keywords = read_file('browsing')
gquestions_keywords = read_file('gquestions')
occupation_keywords = read_file('occupation')
hobbies_keywords = read_file('hobbies')

print (travel_books_keywords,biographies_keywords,mystery_keywords,Scifi_bookskeywords)




clothes_keywords = clothes_keywords + shoes_keywords + pants_keywords + jacket_keywords

lap_keywords = lap_keywords + gaming_lap_keywords + business_lap_keywords +study_lap_keywords

books_keywords= travel_books_keywords + biographies_keywords + mystery_keywords + Scifi_bookskeywords

browsing_keywords = general_keywords

questions_keywords = gquestions_keywords

products_keywords = clothes_keywords + lap_keywords + books_keywords

occupation_keywords=occupation_keywords

hobbies_keywords = hobbies_keywords


entrance= MyNode("browsing",degree='root',question="Do you have something specific in your mind?")
general = MyNode("general",parent = entrance,degree='main1',keywords=browsing_keywords,question="Lets have a general chat in order to recommend you products.")
question1=MyNode("question1",degree='question1',parent=general,keywords=questions_keywords,question="What is your occupation?")
product = MyNode("product",parent = entrance, degree='main2',keywords=products_keywords, question="What products are you interested in?" )
laptop = MyNode('laptop', parent=product,degree='category', keywords=lap_keywords, question="What will you use the laptop for?")
book = MyNode('book', parent=product, keywords=book_keywords,degree = 'category', question="What kind of books do you read?")
clothes = MyNode('clothes', parent=product, keywords=clothes_keywords,degree = 'category', question="What clothing are you looking for?")

shoes = MyNode('shoes', parent=clothes, keywords=shoes_keywords,degree = 'subcategory', question='What type of shoes are you looking for?')
pants = MyNode('pants', parent=clothes, keywords=pants_keywords,degree = 'subcategory', question='What type of pants are you looking for?')
jackets = MyNode('jackets', parent=clothes, keywords=jacket_keywords,degree = 'subcategory', question='What type of jackets are you looking for?')

question2=MyNode('question2',degree='question2',parent=question1,keywords=occupation_keywords,question='What are your hobbies?')

question3=MyNode('question3',degree='question3',parent=question2,keywords=hobbies_keywords,question='Are you married?')


gaming_lap = MyNode('gaming', parent=laptop, keywords=gaming_lap_keywords,degree = 'subcategory', question="What laptop brand are you looking for?")
business_lap = MyNode('business_lap', parent=laptop, keywords=business_lap_keywords,degree = 'subcategory', question="what laptop brand are you looking for?")
study_lap = MyNode('business_lap', parent=laptop, keywords=study_lap_keywords,degree = 'subcategory', question="what laptop brand are you looking for?")

travel_book = MyNode('travel', parent=book, keywords=travel_books_keywords,degree = 'subcategory', question="We have some travel books. Do you have something specific in mind?")
bio_book = MyNode('Bio', parent=book, keywords=biographies_keywords,degree = 'subcategory', question="We have some biographies books. Do you have something specific in mind?")
mystery_book = MyNode('mystery', parent=book, keywords=mystery_keywords,degree = 'subcategory', question="We have some mystery books. Do you have something specific in mind?")
Scifi_book = MyNode('Scifi', parent=book, keywords=Scifi_bookskeywords,degree = 'subcategory', question="We have some Scifi books. Do you have something specific in mind?")


def print_tree():
    for pre, fill, node in RenderTree(entrance):
        print("%s%s question=%s" % (pre, node.name, node.question))

def get_child_node(current_node, user_keywords, return_node=None):
    for child in current_node.children:
        for user_keyword in user_keywords:
            for token in child.keywords:
                if token == user_keyword:
                    return get_child_node(child, user_keywords, child)
    return return_node

def main():
    current_node = entrance

    print(current_node.question)
    while ( True):
        user_response = input()
        user_response = user_response.lower()
        current_node = get_child_node(current_node, stem_tokens((user_response.lower().split(' '))))
        if current_node is not None:
            print(current_node.question)
        else:
            print("Sorry we do not have this product right now, do you have other products you are interested in? ")
            current_node = entrance



if __name__ == '__main__':
    main()