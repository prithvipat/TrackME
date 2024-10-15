from .models import Profile, Transactions, Subscriptions

class Helper():
    def __init__(self, profile, request):
        self.profile = profile
        self.request = request

    def get_pie_graph(self):
        transactions = Transactions.objects.filter(profile=self.profile)
        categories = {'Food': 0, 'Utilities':0, 'Groceries':0, 'Others':0, 'Clothing':0, 'Transportation':0}

        for i in transactions:
            if i.category == 'Food':
                categories[i.category] += 1
        
        return categories
    
    def get_bar_graph(self):
        transactions = Transactions.objects.filter(profile=self.profile)
        months = {'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sept':0, 'Oct':0, 'Nov':0, 'Dec':0}
        l_of_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

        for i in transactions:
            months[l_of_months[i.date.month - 1]] += 1
        
        return months
    
    def get_budget(self):
        pass
        