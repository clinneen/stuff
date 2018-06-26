import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generate_label(label):
	return {
		'has_send': 'Send',
		'has_delivery': 'Delivery',
		'has_open': 'Open',
		'has_click': 'Click',
		'has_unsub': 'Unsubcription',
		'has_vdp': 'VDP',
		'has_sp': 'Soft Pull',
		'has_lock': 'Lock',
		'has_ds': 'Scheduled Delivery',
		'has_green': 'Green',
		'has_sale': 'Sale',
		'vdp_before_send': 'VDP Before Email Send',
		'income': 'Annual Income',
		'age': 'Age',
		'car_fico': 'Carvana FICO Comp',
	}.get(label,label)

# takes pandas series and plots values against index. Supports all pyplot keyword arguments
def series_plot(ser,kind='plot',**kwargs):
	plot_kind=getattr(plt,kind)

	return plot_kind([str(dis) for dis in ser.index],ser,**kwargs)


def groupby_chart(data):
	dct={}
	for i in range(len(data.columns)):
		dct[data.columns[i]]=plt.subplot(len(data.columns),1,i+1)

	for col in data.columns:
		dct[col].plot(data.index,data[col])
		if col!=data.index.name:
			dct[col].set_title('{0} Conversion %'.format(generate_label(col)))
			dct[col].set_ylabel('Sales%')
			dct[col].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
		else:
			dct[col].set_title('{0}'.format(generate_label(col)))

		dct[col].set_xlabel('{0} Octiles'.format(generate_label(data.index.name)))
		

# takes dataframe with date col and indicator col (e.g.'sale_datetime' and 'has_sale'),
# labels, date range, and agg function then returns a dataframe with agg done across date range
# labels is a dict of indicator col of df and datetime col of df (e.g. labels={'has_sale':'sale_datetime',...})
def metrics_over_time(df,labels,dates=pd.date_range('2018-05-24',freq='1D',periods=30),agg=pd.DataFrame.mean):
	results={}
	for l in labels:
		results[l]=[]

	for l in labels:
		for d in dates:
			results[l].append(agg(df.loc[(df[labels[l]]<=d) | (df[labels[l]].isnull()),l]))

	results['date']=dates
	return pd.DataFrame(results)
