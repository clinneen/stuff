import pandas as pd
import matplotlib.pyplot as plt
import graphs as g
import numpy as np
import statsmodels.api as sm
from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

def dis():
	data=pd.read_csv('~/Projects/price_drop/data/data_pull_20180612.csv')
	#clean up dataset
	funnel_labels=['vdp_before_window','vdp_in_window','vdp_after_window','sp','lock','ds','green','sale']

	for fun in funnel_labels:
		data.loc[data[fun].isnull(),'has_{}'.format(fun)]=0
		data.loc[data[fun].notnull(),'has_{}'.format(fun)]=1

	return data

def reg(data=dis()):
	data_subset=data[['has_sale','vdp_before_window']].dropna().copy()
	logit_model=sm.Logit(data_subset.has_sale,data_subset.vdp_before_window)
	result=logit_model.fit()
	print(result.summary())

def explore(data=dis()):
	bin_labels=['low_vdp','high_vdp']

	measure='vdp'
	measure_intervals=pd.qcut(data[measure],8)

	print(data.groupby([measure_intervals,'holdout'])[['has_sale',measure]].mean())
	print(data.groupby([measure_intervals,'holdout'])[['has_sale',measure]].sum())
	print(data.groupby([measure_intervals,'holdout'])[['has_sale',measure]].count())

def level_chart(data=dis()):
	bin_labels=['1st','2nd','3rd','4th','5th','6th','7th','8th']

	measure='vdp_before_window'
	measure_intervals=pd.qcut(data[measure],8,labels=bin_labels)

	split='template'
	counts=data.groupby([split,measure_intervals])[['has_sale',measure]].count()
	rates=data.groupby([split,measure_intervals])[['has_sale',measure]].mean()

	for temp in data[split].unique():
		
		g.groupby_chart(counts.loc[(temp),[measure]])
		plt.title('Count of {} for {}'.format(g.generate_label(measure),g.generate_label(temp)))
		plt.tight_layout()
		plt.show()

		g.groupby_chart(rates.loc[(temp),:])
		plt.tight_layout()
		plt.show()

#explore(data)
#level_chart()
#reg(data)
#dis()
