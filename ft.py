from numpy import *
import math
import os.path
import numpy as np
import pandas as pd
from itertools import islice
from scipy.fft import fft, ifft,fftfreq

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.interpolate import make_interp_spline,BSpline
import matplotlib.patches as m_patches


ifile="../../PEO10/tgg/run3-dipole/dipole-iat.dat"


head_label=['atom','X','Y','Z','px','py','pz','charge','M']

seq='box'

nat=3636
iline=nat+2
nframe=2000
## data reading
list_of_rows=linspace(0,nframe,nframe+1) #*iline
#print(list_of_rows)
df=pd.read_csv(ifile,skiprows=[0],keep_default_na=False,header=None) #,delimiter=r"\s+") 
nrows=df.shape[0]
nf=int(ceil(nrows/iline))
lin=linspace(0,nf,nf)
rows=np.array(linspace(0,nf-1,nf)*iline)
rows2=np.array(linspace(0,nf-1,nf)*iline)+1
r_int1=rows.astype(int)
r_int2=rows2.astype(int)
row_all=np.concatenate((r_int1,r_int2))
row=np.sort(row_all)
dataset=df.drop(df.index[row])
boxdim=df.iloc[row]
#print(dataset.head)
sd=dataset[0].str.split(expand=True)
sd.columns=head_label
sd[["X","Y","Z","px","py","pz"]]=sd[["X","Y","Z","px","py","pz"]].apply(pd.to_numeric)
#print(sd.info)
#print(sd["X"])

## end of data reading

## data analysis
pp=sd[["px","py","pz"]].values#.T
#print(pp.shape)
pp=pp.reshape((-1,nat,3),order='C')
#print(pp[:,0,1])
nf,na,nd=pp.shape
#print([nf,na,nd])   # number of frame; number of atom; number of dimension
px=np.array(pp[:,:,0])
py=np.array(pp[:,:,1])
pz=np.array(pp[:,:,2])
#print(px.shape)
#print(py.shape)
#print(pz.shape)
##  end of datalysis
acf_mumu=np.zeros((na,nf))
#print(acf_mumu.shape)
print(['nf', nf])
for ii in range(1,nf-1):
    jend=nf-ii
    for jj in range(0,jend):
        j0=jj
        j1=j0+ii
        mat_f=np.array(pp[j0,:,:])
        mat_e=np.array(pp[j1,:,:])
        mat_fe=mat_f * mat_e
        if ii==1 and jj==0:
            s_fe=np.sum(mat_fe,axis=1)
        else:
            s_fe+=np.sum(mat_fe,axis=1)

    s_fe=s_fe/(float(jend)-1.0)
    #print(s_fe.shape)
    acf_mumu[:,ii]=s_fe
fft_sum=[]
for ii in range(nd):
    tmp=fft(acf_mumu[ii,:])
    print(['shape',acf_mumu[ii,:].shape])
    if ii==0:
        nn, = acf_mumu[ii,:].shape
        acfi=acf_mumu[ii,:].reshape(nn)
        fft_sum=fft(acfi)
    else:
        acfi=acf_mumu[ii,:].reshape(nn)
        fft_sum+=fft(acfi)
norml=float(nf)/2.0
#print(fft_sum)
yf=np.abs(fft_sum)/norml
T=0.15  # 
xf=fftfreq(nf,T)

indx=np.argsort(xf)
print(yf)
f2=open('ft.dat','w')
for ii in range(nf):
    f2.write('%12.5f'%xf[indx[ii]])
    f2.write('%12.5f\n'%yf[indx[ii]])
plt.xlim([0,max(xf)])
plt.plot(xf[indx],np.abs(yf)[indx]) #np.abs(fft_sum)/norml)
plt.show()
plt.savefig('ft.jpeg',dpi=1200)
