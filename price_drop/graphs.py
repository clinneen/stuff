import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys

def main(file='../data/data_pull_20180612.csv'):
	data=pd.read_csv(file)

	#clean up dataset
	funnel_labels=['vdp_before_window','vdp_in_window','vdp_after_window','sp','lock','ds','green','sale']

	for fun in funnel_labels:
		data.loc[data[fun].isnull(),'has_{}'.format(fun)]=0
		data.loc[data[fun].notnull(),'has_{}'.format(fun)]=1

	bin_labels=['1st','2nd','3rd','4th','5th','6th','7th','8th']

	#measures=input('Enter measure (x,y,...): ').split(',')
	measure=input('Enter measure: ')
	measure_intervals=pd.qcut(data[measure],8,labels=bin_labels)

	metrics=input('Enter metrics (x,y,...): ').split(',')
	metrics.append(measure)

	plt.figure(figsize=(10,10))

	data_group=data.groupby(measure_intervals)[metrics]
	print(data_group.mean())
	groupby_chart(data_group.mean())

	plt.tight_layout()
	plt.show()

def groupby_chart(data):
	dct={}
	for i in range(len(data.columns)):
		dct[data.columns[i]]=plt.subplot(len(data.columns),1,i+1)

	for col in data.columns:
		dct[col].bar(data.index,data[col])
		if col!=data.index.name:
			dct[col].set_title('{0} Conversion %'.format(generate_label(col)))
			dct[col].set_ylabel('Sales%')
			dct[col].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
		else:
			dct[col].set_title('{0}'.format(generate_label(col)))

		dct[col].set_xlabel('{0} Octiles'.format(generate_label(data.index.name)))

def generate_label(label):
	return {
		'has_vdp_in_window': 'VDP',
		'has_sp': 'Soft Pull',
		'has_lock': 'Lock',
		'has_ds': 'Scheduled Delivery',
		'has_green': 'Green',
		'has_sale': 'Sale',
		'price_drop_rel': 'Relative Price Drop',
		'price_drop_abs': 'Price Drop',
		'vdp_before_window': 'VDP Before Email Send',
		'income': 'Annual Income',
		'age': 'Age',
		'car_fico': 'Carvana FICO Comp',
		'One Vehicle - New User': 'One Vehicle Template',
		'Three Vehicle - New User': 'Three Vehicle Template'
	}.get(label,label)

def bayes_test(data):
	#takes dataframe and returns dataframe of results
	pass

if __name__=="__main__":
	if len(sys.argv) > 1:
		pass
	else:

		main()
