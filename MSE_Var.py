import os
import numpy as np
import logging
from PIL import Image
from PIL import ImageFilter

class PatchFilter(object):
    def __init__(self, MSE_thres = None, Var_thres = None, Voe_thres = None, total = 0):
        self.total = total

        self.MSE_discarded = 0
        self.Var_discarded = 0
        self.Voe_discarded = 0

        self.MSE_thres = MSE_thres
        self.Var_thres = Var_thres
        self.Voe_thres = Voe_thres

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)


    """
    The following methods returns:
        True: if the patch is discarded
        False: if the patch is saved
    """
    def filter_with_mse(self, a, b):
        if MSE(a, b) > self.MSE_thres:
            logging.debug("MSE: %f, Discarded" % MSE(a, b))
            self.MSE_discarded += 1
            return True
        else:
            return False

    def filter_with_Var(self, a):
        if Var(a) < self.Var_thres:
            self.Var_discarded += 1
            logging.debug("Clean Var: %f, Discarded" %  Var(a))
            return True
        else:
            return False

    def filter_with_Voe(self, i):
        if Var_Over_Edge(i) < self.Voe_thres:
            logging.debug("Clean Var_Over_Edge: %f, Discarded" %  Var_Over_Edge(i))
            self.Voe_discarded += 1
            return True
        else:
            return False

    def print_discarded_stat(self):
        if not self.MSE_thres is None:
            logging.debug("%d patches discarded due to high MSE. %.2f percent of total."
                % (self.MSE_discarded, self.MSE_discarded / self.total))
        if not self.Var_thres is None:
            logging.debug("%d patches discarded due to low Var. %.2f percent of total."
                % (self.Var_discarded, self.Var_discarded / self.total))
        if not self.Voe_thres is None:
            logging.debug("%d patches discarded due to low Voe. %.2f percent of total."
                % (self.Voe_discarded, self.Voe_discarded / self.total))


def MSE(a, b):
    return np.mean((a - b)**2)

def Var(a):
    return np.var(a)

def Var_Over_Edge(i):
    return np.array(i.filter(ImageFilter.FIND_EDGES)).var()

if __name__ == "__main__":

    # cpr = "/media/michael/MWTraining/patches/Clean/"
    # npr = "/media/michael/MWTraining/patches/Noisy/"

    cpr = "/home/michael/tensorflow/DenoiseNet/Utils/Clean/"
    npr = "/home/michael/tensorflow/DenoiseNet/Utils/Noisy/"

    cs = os.listdir(cpr)
    ns = os.listdir(npr)

    mse_smooth = 0
    var_smooth = 0
    voe_smooth = 0
    a = 0.9

    for i in range(len(cs)):

        ci = Image.open(os.path.join(cpr, cs[i]))
        ni = Image.open(os.path.join(npr, ns[i]))

        c = np.array(ci)
        n = np.array(ni)

        mse = MSE(c, n)
        var = Var(c)
        var_over_edge = Var_Over_Edge(ci)

        mse_smooth = mse_smooth * a + mse * (1 - a)
        var_smooth = var_smooth * a + var * (1 - a)
        voe_smooth = voe_smooth * a + var_over_edge * (1 - a)

        print (cs[i])
        print ("MSE: %f, smooth: %f, VAR: %f, smooth: %f, Var_Over_Edge: %f, smooth: %f" % (mse, mse_smooth, var, var_smooth, var_over_edge, voe_smooth))
