from scipy.stats import beta
from scipy.special import betaln
import pandas as pd
import numpy as np


def bayes_test(df,a,b,user_count_col='const'):
	def h(a,b,c,d):
		total=0.0 
		for i in range(1,c):
			total+=np.exp(betaln(a+i,b+d)-np.log(i)-betaln(a,b)-betaln(i,d))
		return 1-(np.exp(betaln(a,b+d)-betaln(a,b)))-total

	def prob_test_greater_than_control(a,b,c,d):
		return h(a,b,c,d)

	def expected_effect(a,b,c,d):
		#var for total prob decomp
		expected_effect_given_test_greater_than_control=np.exp(betaln(a+1,b)-betaln(a,b))*h(a+1,b,c,d)-np.exp(betaln(c+1,d)-betaln(c,d))*h(a,b,c+1,d)
		expected_effect_given_control_greater_than_test=np.exp(betaln(a+1,b)-betaln(a,b))*h(c,d,a+1,b)-np.exp(betaln(c+1,d)-betaln(c,d))*h(c+1,d,a,b)
		
		return prob_test_greater_than_control(a,b,c,d)*expected_effect_given_test_greater_than_control+(1-prob_test_greater_than_control(a,b,c,d))*expected_effect_given_control_greater_than_test

	def expected_effect_relative(a,b,c,d):
		#var for total prob decomp
		expected_effect_relative_given_test_greater_than_control=np.exp(betaln(a+1,b)+betaln(c-1,d)-betaln(a,b)-betaln(c,d))*h(a+1,b,c-1,d)-h(a,b,c,d)
		expected_effect_relative_given_control_greater_than_test=np.exp(betaln(a+1,b)+betaln(c-1,d)-betaln(a,b)-betaln(c,d))*(1-h(a+1,b,c-1,d))-(1-h(a,b,c,d))

		return (expected_effect_relative_given_test_greater_than_control*prob_test_greater_than_control(a,b,c,d)+expected_effect_relative_given_control_greater_than_test*(1-prob_test_greater_than_control(a,b,c,d)))

	result={'a_size':[],'b_size':[],'probability':[],'expected_effect_abs':[],'expected_effect_rel':[], 'a_conversion':[], 'b_conversion':[], 'expected_incremental_effect':[]}
	ind=[]
	for col in df.columns:
		a_size=int(df.loc[a,user_count_col])
		b_size=int(df.loc[b,user_count_col])
		if col!=user_count_col:
			a_success=int(df.loc[a,col])+1
			a_failure=int(a_size-df.loc[a,col])+1
			b_success=int(df.loc[b,col])+1
			b_failure=int(b_size-df.loc[b,col])+1
			a_conversion=float(a_success)/(a_success+a_failure)
			b_conversion=float(b_success)/(b_success+b_failure)
			exp_effect=expected_effect(a_success,a_failure,b_success,b_failure)

			result['probability'].append(prob_test_greater_than_control(a_success,a_failure,b_success,b_failure))
			result['expected_effect_abs'].append(exp_effect)
			result['expected_effect_rel'].append(expected_effect_relative(a_success,a_failure,b_success,b_failure))
			result['a_conversion'].append(a_conversion)
			result['b_conversion'].append(b_conversion)
			result['expected_incremental_effect'].append((a_size+b_size)*exp_effect)
			result['a_size'].append(a_size)
			result['b_size'].append(b_size)
			ind.append(col)

	return pd.DataFrame(result,index=ind)