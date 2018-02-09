class Order():
    # item = ['carrot',
    #         'beet',
    #         'orange',
    #         'coffee',
    #         'squirrels']
    #
    # prices = [1.33, 5.99, 5.44, 4.00, 0.99]
    items = [
        {'name': "carrot", 'price': 1},
        {'name': "squash", 'price': 1},
        {'name': "butt", 'price': 1},
        {'name': "stuff", 'price': 10},
    ]

    @property
    def price(self):
        return sum([i['price'] for i in self.items])


a = Order()
print(a.price)
print(Order().price)


# import pdb; pdb.set_trace()