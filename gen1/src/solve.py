class game:

	def __init__(self):
		self.cards = []

	def __repr__(self):
		return str(self.cards)
	
	def addCard(self, card):
		self.cards.append(card)
	
	def removeCard(self, card):
		del self.cards[self.cards.index(card)]

	def removeCardId(self, card_id):
		del self.cards[card_id]
	

	def getCardId(self, card):
		return self.cards.index(card)

	def findSets(self):
		found = []
		for i, ci in enumerate(self.cards):
			for j, cj in enumerate(self.cards[i+1:], i+1):
				for k, ck in enumerate(self.cards[j+1:], j+1):
					if ci.is_set(cj,ck):
						found.append((ci,cj,ck))
		return found
	
	def findSetsId(self):
		found = []
		for i, ci in enumerate(self.cards):
			for j, cj in enumerate(self.cards[i+1:], i+1):
				for k, ck in enumerate(self.cards[j+1:], j+1):
					if ci.is_set(cj, ck):
						found.append((self.getCardId(ci), self.getCardId(cj), self.getCardId(ck)))
		return found



class card:
	def __init__(self, *attrs):
		self.attrs = attrs
	
	def __eq__(self,other):
		return self.attrs == other.attrs

	def __hash__(self):
		return hash(self.attrs)

	def __repr__(self):
		return 'Card{}'.format(self.attrs)

	#Checking if 3 cards are a set
	def is_set(self, card1, card2):
		return all((val0+val1+val2) % 3 == 0 for val0, val1, val2 in zip(self.attrs, card1.attrs, card2.attrs))
	
