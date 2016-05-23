import model
import pickle
import pca_visualize

ListOfUserNames = ['Rashik', 'RodionFartov', 'tangriz']
M = model.Model()
M.modelUpdate(ListOfUserNames)

pickle.dump(M.Vmtx, open('Vmtx.p', 'w'))
pickle.dump(M.Umtx, open('Umtx.p', 'w'))
pickle.dump(M.Users_dict, open('Users_dict.p', 'w'))

#last post users are depicted
pca_visualize.pca_plot(pca_visualize.getMtxFromUserNames(ListOfUserNames), ListOfUserNames)

