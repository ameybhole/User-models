from anytree import NodeMixin, RenderTree
from nltk.stem import PorterStemmer
porter = PorterStemmer()
from nltk.corpus import stopwords
from anytree.importer import JsonImporter
from anytree import RenderTree
from anytree.exporter import DotExporter

import json


def stem_tokens(token_words):
    stemmed_tokens = []
    filtered_words = token_words

    for word in filtered_words:
        stemmed_tokens.append(porter.stem(word))
        print('stemmed word is ', porter.stem(word))
    print(stemmed_tokens)

    return stemmed_tokens


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

class Chatbot():
    def __init__(self, dir='controllers/'):

        importer = JsonImporter()

        with open(dir + 'data.json', 'r') as f:
            data = json.load(f)
            self.root = importer.import_(data)

        self.current_node = self.root

        DotExporter(self.root).to_picture("tree.png")

    def get_brand_answer(self, brand_array, user_response):
        brand = ''
        print("we are in the brand")
        user_response = user_response.lower()
        tokens = user_response.split()
        for token in tokens:
            print('token is', token)
            if token in brand_array:
                brand = token
                break
        print('brand is ', brand)
        return "do you like this product?" , 'brand', brand, self.current_node.name


    def get_child_node(self, current_node, user_keywords, return_node=None):
        print('looking for ', user_keywords)
        for child in current_node.children:
            print(child.name)
            for user_keyword in user_keywords:
                for token in child.keywords:
                    if token == user_keyword:
                        return self.get_child_node(child, user_keywords, child)
        return return_node

    def get_price(self, answer):
        price = [int(s) for s in answer.split() if s.isdigit() ]
        return price[0]

    def get_answer(self, user_response):
        user_response = user_response.lower()
        if self.current_node.name == "question3":
            print("we are in price question")
            price = self.get_price(user_response)
            return "check if you like any of the suggested products", 'price_answer', price
        current_node = self.get_child_node(self.current_node, stem_tokens((user_response.lower().split(' '))))

        print('gent answer for', self.current_node.degree )


        if self.current_node.degree =="general_child":
            print('we are in general')

            current_node = self.current_node.children[0]
            names = self.get_tree_leaves(user_response)




            self.current_node = current_node
            return current_node.question, 'general_answer', names

        if self.current_node.degree == 'subcategory':
            if self.current_node.parent.name == 'laptop':
                laptop_brands = ['asus', 'acer', 'dell', 'macbook', 'hp', 'rog', 'lenovo', 'msi']
                return self.get_brand_answer(laptop_brands, user_response)
            elif self.current_node.parent.name == 'clothes':
                clothes_brands=['adidas', 'nike', 'jeans', 'sweatpants', 'chouyatou', 'dwar', 'lock and love', 'ilovesia']
                return self.get_brand_answer(clothes_brands, user_response)
        else:
            if current_node is not None:
                degree = current_node.degree
                name = current_node.name
                self.current_node = current_node
                return current_node.question, degree, name

            else:
                self.current_node = self.root
                return "Sorry we do not have this product right now, do you have other products you are interested in? ", 'root', 'product'

    def get_tree_leaves(self, user_response):

        root_node = self.root
        user_response = user_response.lower()
        tokens = stem_tokens(user_response.split())

        names = []
        for child in root_node.children:
            if child.name == 'product':
                current_node = child
                leaves = current_node.leaves
                for leaf in leaves:
                    for token in tokens:
                        print("tokens are ", leaf.keywords , "looking for ", tokens)
                        if token in leaf.keywords:
                            print("chosen leaf is ",leaf.name)
                            names.append(leaf.name)

        return names

    def print_tree(product):
        for pre, fill, node in RenderTree(product):
            print("%s%s question=%s" % (pre, node.name, node.question))

def main():
    dir = ''

    chatbot = Chatbot(dir)
    print(chatbot.root.question)
    chatbot.get_tree_leaves('i like traveling')

    while (True):
        user_response = input()
        if chatbot.current_node.degree == 'subcategory':
            if chatbot.current_node.parent.category == 'laptop':
                brand=''
                laptop_brands = ['asus', 'acer', 'dell', 'macbook', 'hp', 'rog', 'lenovo', 'msi']
                user_response = user_response.lower()
                tokens = user_response.split()
                for token in tokens:
                    if token in laptop_brands:
                        brand = token
                        break

        response = chatbot.get_answer(user_response)
        print(response[0],response[1], response[2])


if __name__ == '__main__':
    main()