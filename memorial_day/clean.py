import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import my_utility as util
import bayes

def dis():
	df=pd.read_csv('~/Projects/memorial_day/data/data_pull_20180625_no_date_restriction.csv',low_memory=False)

	cohort_template={'A1':'2018 Memorial Day - In Market - A1 - Send 5/26.2.2018 Memorial Day - Shop by Body Style'
					,'B2':'2018 Memorial Day - Other - B2 - Send 5/26.2.2018 Memorial Day - Shop by Body Style'
					,'B3':'2018 Memorial Day - Other - B3 - Send 5/26.2.2018 Memorial Day - Shop by Body Style'
					,'B4':'2018 Memorial Day - Other - B4 - Send 5/24.3.2018 Memorial Day - Value Propositions'}

	for i in cohort_template:
		df.drop(df.loc[df.cohort==i,:].loc[df.email_template!=cohort_template[i],:].index,inplace=True)

	for col in df.columns:
		if 'datetime' in col:
			df.loc[:,col]=pd.to_datetime(df[col])
			df.loc[df[col].isnull(),'has_{0}'.format(col.split('_')[0])]=0
			df.loc[df[col].notnull(),'has_{0}'.format(col.split('_')[0])]=1

	labels=['first_web_datetime','send_datetime','delivery_datetime','open_datetime','click_datetime','unsub_datetime','account_datetime','sp_datetime','lock_datetime','ds_datetime','green_datetime','sale_datetime']

	for i in range(len(labels)):
		for j in range(len(labels)):
			if j>i:
				df['{0}_{1}_timedelta'.format(labels[i].split('_')[0],labels[j].split('_')[0])]=df[labels[j]]-df[labels[i]]

	df['const']=1

	return df


def plot_it(df1,df2):
	for col in df1.columns:
		print(col)
		if 'has_' in col:
			plt.plot(df1.date,df1[col],'r')
			plt.plot(df2.date,df2[col],'b')
			plt.title('{} Conversion Over Time'.format(util.generate_label(col)))
			plt.legend(['Treatment','Holdout'],loc='upper left')
			plt.show()


def bayes_by_segment(df,a,b,segment_level=1):
	res={}
	for l in df.index.levels[segment_level]:
		temp=bayes.bayes_test(df.xs(l,level=segment_level),a,b)
		for j in temp.index:
			if j not in res:
				res[j]=[]
			res[j].append(temp.loc[j,'expected_incremental_effect'])

	return pd.DataFrame(res,index=['1st','2nd','3rd','4th'])

#test
#data=pd.read_pickle('counts_by_fico_cohort.pkl')
#bayes_by_segment(data,'A1','A2')

