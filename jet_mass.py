import numpy as np
import matplotlib.pyplot as plt
import os 
import glob

path = "./projects/qgtag/decompressed_output/"
url = "/users/dshutong/.energyflow/datasets/QG_jets_0.npz"
data = []
name = []
for i in glob.glob('/users/dshutong/.energyflow/datasets/QG_jets_*.npz'):
    print("loading original data:",i)
    X = np.load(i)["X"]
    n_pythia_pad = 150-X.shape[1]
    X = np.lib.pad(X , ((0,0), (0,n_pythia_pad),(0,0)), mode='constant', constant_values=0)
    data.append(X)
    y = np.load(i)["y"]
    name.append(y)
    print("data appended")
    break

data = np.array(data)
data = np.concatenate(data, axis=0)
name = np.array(name)
name = np.concatenate(name, axis=0)

X = data
y = name

qmask, gmask = (y==1)[:len(y)], (y==0)[:len(y)]
#print(qmask,gmask)
#print("Done loading data!\nThere are "+str(len(y[qmask]))+" q jets, and "+str(len(y[gmask]))+" g jets.")

#print(X[qmask].shape)
#print(X[gmask].shape)

qmults = np.array([len(i[~np.all(i==0,axis=1)]) for i in X[qmask]])
gmults = np.array([len(i[~np.all(i==0,axis=1)]) for i in X[gmask]])
#print(qmults,gmults)

bins = np.linspace(0,150,150)

plt.hist(qmults, bins=bins,density=True, histtype='step', color='blue', label='uncompressed Quark jets')
plt.hist(gmults, bins=bins,density=True, histtype='step', color='red', label='uncompressed Gluon jets')
#plt.xlim(0,100)
#plt.ylim(0,0.05)

data_de = []
name_de = []

for i in glob.glob(path + "decompressed_*.npz"):
    print("loading data:",i)
    X_de = np.load(i)["data"]
    X_de = np.squeeze(X_de)
    X_de = X_de.transpose(0,2,1)
    n_pythia_pad = 150-X_de.shape[1]
    X_de = np.lib.pad(X_de , ((0,0), (0,n_pythia_pad),(0,0)), mode='constant', constant_values=0)
    #print(X.shape)
    data_de.append(X_de)
    y_de = np.load(i)["names"]
    name_de.append(y_de)
    print("data appended")
    break

data_de = np.array(data_de)
data_de = np.concatenate(data_de, axis=0)
#print(data_de.shape)
name_de = np.array(name_de)
name_de = np.concatenate(name_de, axis=0)

print(X.shape)
pt = X[:,:139,0]
print(pt)
pad_start_indices = np.argmax(pt == 0, axis=1)
print(pad_start_indices)

for i in range(X.shape[2]):
    for j, start in enumerate(pad_start_indices):
        data_de[j, start:,i] = 0
#print(data_de[0,:,:])


#print(data_de.shape)
#print(name_de.shape)
X_de = data_de
y_de = name_de

qmask_de, gmask_de = (y_de==1)[:len(y_de)], (y_de==0)[:len(y_de)]
#print(qmask_de,gmask_de)
#print("Done loading data!\nThere are "+str(len(y_de[qmask_de]))+" q jets, and "+str(len(y_de[gmask_de]))+" g jets.")

#print(X_de[qmask_de].shape)
#print(X_de[gmask_de].shape)

qmults_de = np.asarray([len(i[~np.all(i==0,axis=1)]) for i in X_de[qmask_de]])
gmults_de = np.asarray([len(i[~np.all(i==0,axis=1)]) for i in X_de[gmask_de]])
#print(qmults_de,gmults_de)

bins = np.linspace(0,150,150)

plt.hist(qmults_de, bins=bins,density=True,  color='green', label='decompressed Quark jets')
plt.hist(gmults_de, bins=bins,density=True,  color='orange', label='decompressed Gluon jets')

plt.legend(loc='upper right', frameon=False)
plt.xlabel('Constituent multiplicity')
plt.ylabel(r'Cross Section (Normalized)')
plt.savefig("multiplicity.pdf")


# try to make jet_mass figure



