import pdb


class Category:

    
    def __init__(self, name):
        self.name = name
        self.ledger = []
        

    def get_balance(self):
            total = 0
            for item in self.ledger:
                total += item['amount']
            return total
        
    def deposit(self, amount, description = ""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def transfer(self, amount, destination):
        if self.check_funds(amount):
            if self.withdraw(amount, f'Transfer to {destination.name}'):
                destination.deposit(amount, f'Transfer from {self.name}')
                return True
        return False

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def __str__(self):
        result = self.name.center(30, '*') + '\n'

        for item in self.ledger:
            description = item['description'][:23]
            amount = item['amount']
            result += f'{description:<23}{amount:>7.2f}\n'

        result += f'Total: {self.get_balance()}'
        return result


   

def create_spend_chart(categories):
    # Obliczenie wydatków każdej kategorii.
    spent = []

    for category in categories:
        category_spent = sum(
            -item['amount']
            for item in category.ledger
            if item['amount'] < 0
        )
        spent.append(category_spent)

    total_spent = sum(spent)

    # Procenty zaokrąglone w dół do wielokrotności 10.
    percentages = []

    for amount in spent:
        percentage = (amount / total_spent) * 100 if total_spent > 0 else 0
        percentages.append(int(percentage) // 10 * 10)

    result = 'Percentage spent by category\n'

    # Oś procentowa i słupki.
    for level in range(100, -1, -10):
        result += f'{level:>3}| '

        for percentage in percentages:
            result += 'o  ' if percentage >= level else '   '

        result += '\n'

    # Linia pod wykresem.
    result += '    ' + '-' * (len(categories) * 3 + 1) + '\n'

    # Nazwy kategorii zapisane pionowo.
    max_length = max(
        (len(category.name) for category in categories),
        default=0
    )

    for index in range(max_length):
        result += '     '

        for category in categories:
            letter = category.name[index] if index < len(category.name) else ' '
            result += letter + '  '

        if index < max_length - 1:
            result += '\n'

    return result