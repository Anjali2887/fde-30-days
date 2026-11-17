from dataclasses import dataclass, field

@dataclass
class Account:
    id : str
    owner : str
    balance : float = 0.0
    tags : list[str] = field(default_factory=list)

    def deposit(self, amount : float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount : float) -> None:
        if self.balance < amount:
            raise ValueError("The balance is too low")


def summarise(accounts : list[Account]) -> dict[str, float]:
    return{a.owner: a.balance for a in accounts if a.balance > 0}

def top_n(accounts : list[Account], n):
    return sorted(
            accounts,
            key=lambda a: a.balance,
            reverse=True
        )[:n]

if __name__ == "__main__":
    accounts = [Account("A1", "Ravi", 1200.0), Account("A2", "Meera"), Account("A3", "Sam", 50.0)]
    accounts[1].deposit(300)
    print(summarise(accounts))
    try:
        accounts[0].deposit(-5)
    except ValueError as e:
        print(f"Rejected:{e}")

    try:
         accounts[1].withdraw(400)
    except ValueError as e:
            print(f"Rejected:{e}")

    result = top_n(accounts, 2)

    for account in result:
        print(account.owner, account.balance)

    big = [a.id for a in accounts if a.balance >= 300]
    print("Balances >= 300:", big)



def word_length(words : list[str]) -> dict[str, int]:
    return{w : len(w) for w in words}

if __name__ == "__main__":
    words = ["hi", "there"]
    print(word_length(words))


     



