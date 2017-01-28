from django import forms


class addRestaurant(forms.Form):
	rname = forms.CharField(label='Enter Name of Restaurant', max_length=100)
	rcuisine = forms.CharField(label='Enter type of Food', max_length=100)
	rborough = forms.CharField(label='Enter City', max_length=100)
	rstreet = forms.CharField(label='Enter the street', widget=forms.TextInput(attrs={'id': 'address'}), max_length=100)
	rcoordy = forms.CharField(label='Enter Y coord or localize', widget=forms.TextInput(attrs={'id': 'add_coordy'}), max_length=100)
	rcoordx = forms.CharField(label='Enter X coord or localize', widget=forms.TextInput(attrs={'id': 'add_coordx'}), max_length=100)

class modifyRestaurant(forms.Form):
	rname = forms.CharField(label='Name', widget=forms.TextInput(attrs={'id': 'rname'}), max_length=100)
	rcuisine = forms.CharField(label='Food', widget=forms.TextInput(attrs={'id': 'rcuisine'}), max_length=100)
	rborough = forms.CharField(label='City', widget=forms.TextInput(attrs={'id': 'rborough'}), max_length=100)
	rstreet = forms.CharField(label='Street', widget=forms.TextInput(attrs={'id': 'address'}), max_length=100)
	rcoordy = forms.CharField(label='Y coord', widget=forms.TextInput(attrs={'id': 'add_coordy'}), max_length=100)
	rcoordx = forms.CharField(label='X coord', widget=forms.TextInput(attrs={'id': 'add_coordx'}), max_length=100)