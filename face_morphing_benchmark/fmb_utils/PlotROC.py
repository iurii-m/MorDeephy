
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

class PlotRocDefault():
    
    def __init__(self, gt_labels = None, predictions = None, title = None, FMR_compare = None):
        self.gt_labels = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 ,1])
        self.predictions = np.array([0.01058, 0.02543, 0.79634, 0.80573, 0.29474, 0.50843, 0.370573, 0.91037, 0.053913,
            0.30347, 0.80264, 0.8935, 0.02104, 0.03637, 0.050735,0.970038, 0.962312, 0.99, 
            0.8547, 0.76035, 0.872636, 0.07048, 0.12025, 0.212735, 0.00019, 1.00])
        self.title = "roc_curve"
        self.FMR_compare = [0.2, 0.1, 0.01, 0.001, 0.0001]
        
        self.gt_labels = self.gt_labels if gt_labels is None else gt_labels
        self.predictions = self.predictions if predictions is None else predictions
        self.title = self.title if title is None else title

        # metrics
        self.fpr = None
        self.tpr = None
        self.auc = None
    
    def calc_fpr_tpr(self):
        self.fpr, self.tpr, self.thresholds = roc_curve(self.gt_labels,self.predictions, pos_label=1)
        #calculate FMR and FNMR
        self.FMR = self.fpr
        self.FNMR = 1 - self.tpr

    def calc_auc(self): # area under the curve
        self.auc = roc_auc_score(self.gt_labels, self.predictions)

    def fnmr_fmr(self): # FNMR @ FMR
        size_fmr = len(self.FMR_compare)
        if size_fmr > 0:
            FNMR_results = []
            for i in range(size_fmr):
                FMR_closest, FMR_closest_index = self._find_nearest_value(self.FMR, self.FMR_compare[i])
                #print("FMR closest", FMR_closest, FMR_closest_index)
                FNMR_results.append(self.FNMR[FMR_closest_index])
            print(self.FMR_compare)
            print(FNMR_results)
    
    def _find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        closest_element = array[idx]
        return  closest_element, idx
    
    def save(self, filepath=None): # save ROC curve
        if filepath == None: filepath = self.title + ".png"
        print(f"plot saved: {filepath}")
        self.plt.savefig(filepath)
    
    def show(self): # to show the ROC plot
        self.plt.show()
    
    def print_stats(self):
        auc_res_5f =  "{:.5f}".format(self.auc)
        print("AUC ROC - ", auc_res_5f)
        print(self.FMR)
        print(self.FNMR)
        print(self.thresholds)
        print(self.predictions)
        print(self.gt_labels)
    
    def test(self):
        self.calc_fpr_tpr()
        self.calc_auc()
        self.draw()
        self.save()
        self.show()
        self.print_stats()
        self.fnmr_fmr()
    
    def draw(self): # plot ROC curve
        if self.fpr is None or self.tpr is None: self.calc_fpr_tpr()
        if self.auc is None: self.calc_auc()

        auc_res_5f =  "{:.5f}".format(self.auc)
        plt.figure()
        plt.title(self.title)
        plt.plot(self.fpr, self.tpr, color='black', lw=1, label='Default. texture. ROC curve (area = '+str(auc_res_5f)+')')
        plt.legend(loc="lower right")
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        self.plt = plt


class PlotROC(PlotRocDefault):
    def __init__(self, gt_labels = None, predictions = None, title = None, FMR_compare = None):
        super().__init__(gt_labels = gt_labels, predictions = predictions, title = title, FMR_compare = FMR_compare)
        self.title = "roc_curve2"

    def draw(self):
        plt.title(self.title)
        plt.plot(self.fpr, self.tpr, 'b', label = 'AUC = %0.2f' % self.auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        self.plt = plt


def main():
    plot_roc = PlotRocDefault()
    plot_roc.test()

    plot_roc = PlotROC()
    plot_roc.test()


if __name__ == "__main__":
    main()
