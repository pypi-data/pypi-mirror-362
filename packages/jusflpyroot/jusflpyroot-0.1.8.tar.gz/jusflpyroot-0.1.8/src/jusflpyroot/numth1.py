#!/usr/bin/env python3

import numpy as np
import ROOT
ROOT.gStyle.SetOptStat(1111111)
ROOT.gStyle.SetPadGridX(True)
ROOT.gStyle.SetPadGridY(True)
import click
import datetime as dt
from console import fg, bg
import gc # garbace collect on del
import os
import math
import threading
import time

from iminuit import cost,Minuit
from scipy.stats import chi2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")


# ================================================================================
#   FIT
# --------------------------------------------------------------------------------
class PrepareLSQFit:
    cx = np.array([])
    y = np.array([])
    dy = np.array([])
    model_name = "p1"
    MODEL = None
    # --------------------- all about results
    res_chi2 = None
    res_dof = None
    res_minuit = None
    res_params = {}
    res_pars = {}
    res_valid = False # skip conclusions...
    # ---------------------
    switch_xi2_output = True
    function_map = {}

    # ---------------------
    # ================================================================================
    #   INIT
    # --------------------------------------------------------------------------------
    def __init__(self, x, y, dy):
        """
        init the cost function, it will contain the DATA: x,y,dy
        """
        self.cx = np.array(x)
        self.y = np.array(y)
        #self.dy = np.array(dy) # if dy==0!
        mindy_nz = min([x  for x in dy if x != 0 ])
        self.dy = np.array([x if x != 0 else mindy_nz for x in dy])
        self.model_name = None
        self.switch_xi2_output = True # initially functions output Xi2
        #
        self.function_map = {"p0": self.P0, "p1": self.P1, "p2": self.P2}
        #
        self.res_valid = False

    def set_model(self, mname):
        self.model_name = mname
        if mname in self.function_map.keys():
            self.MODEL = self.function_map.get(mname)
        else:
            self.MODEL = None


    def XI2(self, model_points):
        res =  np.sum( (self.y - model_points) ** 2 / self.dy ** 2)
        #print(res)
        return res

    # least-squares score function = sum of data residuals squared*********************
    def P0(self, a):
        model_points = np.zeros_like(self.cx) + a
        #print(a, model_points)
        if self.switch_xi2_output:
            return self.XI2(model_points)
        return model_points

    def P1(self, a, b):
        model_points = self.cx *  a + b
        #print(model_points)
        if self.switch_xi2_output:
            return self.XI2(model_points)
        return model_points

    def P2(self, a, b, c):
        model_points = self.cx *self.cx * a + self.cx *b + c
        if self.switch_xi2_output:
            return self.XI2(model_points)
        return model_points

    # ================================================================================
    #    ***********************      FIT       *************
    # --------------------------------------------------------------------------------
    def FIT(self, **pars):
        """
        apriori unknown number of parameters -  **kwargs
        """
        if self.MODEL is None:
            print(f"{fg.red}X... no model defined.... define model first {fg.default}")
            return
        print("_" * 70)
        print(f"        FIT: {self.model_name} ;  initial:  {pars}")
        print("_" * 70)
        self.switch_xi2_output = True #  functions will output Xi2
        m = None
        # -------- set proper LSQ --------
        if self.MODEL:
            ok = False
            try:
                m = Minuit(self.MODEL,  **pars)
                ok = True
            except:
                print(f"{fg.red}X... model init FAILED... maybe parameters do not match! {fg.default}")
            if not ok:return


        # if self.model_name == "p0" and (len(pars) == 1):
        #     m = Minuit(self.P0, **pars)
        # elif self.model_name == "p1" and (len(pars) == 2):
        #     m = Minuit(self.P1, **pars)
        # elif self.model_name == "p2" and (len(pars) == 3):
        #     m = Minuit(self.P2, **pars)
        else:
            print(f"{fg.red}X...  MODEL - {self.model_name} - with {len(pars)} is not known. STOP  {fg.default}")
        print("---------------------------------------")
        #res = m.simplex()
        res = m.migrad()

        print(res)

        if m.valid:
            self.res_valid = True
            print(f"{fg.green}i...                      VALID {fg.default}")
            res_minuit = m
            print(f"FCN={m.fval} nfcn steps={m.nfcn} npar={m.npar} dpoints={len(self.cx)}  ndofNAN={m.ndof}")
            self.res_chi2 = m.fval
            self.res_dof = len(self.cx)-m.npar
            percentile = self.chi2_percentile(self.res_chi2, self.res_dof)
            p_value = 1 - chi2.cdf(self.res_chi2, self.res_dof)
            #print(percentile)
            print(f"i... {fg.green}  ****   X^2/dof={self.res_chi2/self.res_dof:.3f}   ... Xi2 percentile= {percentile:.3f} {fg.default}  pvalue={p_value:.3f} (low p rejects)*****")
            # Example usage
            # chi2_value = your chi-square value
            # dof = degrees of freedom

            for i in m.parameters:
                #print(i)
                #print(str(i))
                print(f" {i}   {m.values[i]:.4f} +- {m.errors[i]:.4f}     ")
                val = m.values[i]
                self.res_params[i] = ( m.values[i], m.errors[i] )
                self.res_pars[i] =  m.values[i] # prepare for kwargs
        else:
            self.res_valid = False
            print(f"{fg.red}i...                      INVALID {fg.default}")
            print(f"{fg.red}X... invalid fit ............................{fg.default}")

    @staticmethod
    def chi2_percentile(chi2_value, dof):
        p_value = chi2.cdf(chi2_value, dof)
        return p_value

    # ================================================================================
    # summary
    # --------------------------------------------------------------------------------
    def conclude(self):
        if not self.res_valid:return
        print(f"""
Conclusions:
        model:  {self.model_name}
        """)
        for i in self.res_params.keys():
            print(f"   {i} : {self.res_params[i]}")


        plt.errorbar(self.cx, self.y, self.dy, fmt='o')

        #print(self.res_pars)
        self.switch_xi2_output = False #  functions will output vector data
        y_modeled = self.y

        if self.MODEL:
            y_modeled = self.MODEL(**self.res_pars)

        # if self.model_name == "p0":
        #     y_modeled = self.P0(**self.res_pars)
        # if self.model_name == "p1":
        #     y_modeled = self.P1(**self.res_pars)
        # if self.model_name == "p2":
        #     y_modeled = self.P2(**self.res_pars)


        plt.plot( self.cx, y_modeled, 'r:')

        dify = (y_modeled - self.y) / self.dy
        plt.bar( self.cx, dify, color=[0, 0, 0, 0.2])
        plt.axhline(0, ls="-", c='k' )
        plt.axhline(1, ls=":", c='k' )
        plt.axhline(-1, ls=":", c='k' )

        plt.grid()
        plt.show()



# ================================================================================
#   HISTOGRAM INSTANCE ***************************
# --------------------------------------------------------------------------------

class NumpyTH1:
    instances = []  # class list to track objects
    color_index = 0 # class list!
    mycolors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    def __init__(self, bin_edges: np.ndarray, contents: np.ndarray, errors: np.ndarray = None):
        NumpyTH1.instances.append(self)
        self.bin_edges = bin_edges
        #
        self.contents = contents
        self.edges = bin_edges
        self.centers =  0.5 * (self.edges[1:] + self.edges[:-1])
        #
        self.errors = errors if errors is not None else np.sqrt(contents)
        self.underflow = 0.0
        self.overflow = 0.0
        self.underflow_error = 0.0
        self.overflow_error = 0.0
        #
        self.name = "name_unknown"
        self.title = "title_unknown"
        self.tstamp = dt.datetime.now()
        self.nbins = 0
        #



    def __str__(self):
        """
        print kindof a table - per object
        """
        res = ""
        res = res + f"{self.name:10s} '{self.title:35s}'  {str(self.tstamp)[:-3]}   {self.nbins:5}   "
        res = res +f"<{self.ledges.min()} - {self.redges.max()})   "
        res = res +f"[ {self.underflow} / {self.contents.sum()} / {self.overflow} ]  "
        return res

    def get_xy(self, position="center"):
        """
        get numpy vectors x and y  possible center | ledge | redge
        """
        if position.find("center") >= 0:
            return self.centers, self.contents, self.errors
        elif position.find("ledge") >= 0:
            return self.ledges, self.contents, self.errors
        elif position.find("redge") >= 0:
            return self.redges, self.contents, self.errors
        else:
            return None, None, None

    @classmethod
    def by_name(cls, name):
        """
        return histo from instances by name
        """
        for ii in range(len(cls.instances)):
            i = cls.instances[ii]
            if i.name == name:return i
            return None

    @classmethod
    def list(cls):
        """
        list local instances
        """
        for ii in range(len(cls.instances)):
            i = cls.instances[ii]
            print(f"{ii:2d}. ", end="")
            print(i)#.print()

    @classmethod
    def reset_all(cls):
        """
        delete all local instances - go backwards
        """
        for i in range(len(cls.instances) - 1, -1, -1):
            item = cls.instances[i]
            item.force_del()
        print("D... deleted all instances")
        cls.color_index = 0
        print("D... reset colors")


    @classmethod
    def from_th1(cls, hist: ROOT.TH1):
        """
        read existing TH1 and create a new object ... seems to work ......
        """
        nbins = hist.GetNbinsX()
        edges = np.array([hist.GetBinLowEdge(i) for i in range(1, nbins + 2)]) # ????

        #  like return new instance/object  cls....
        full_contents = np.array([hist.GetBinContent(i) for i in range(0, nbins + 2)])  #
        errors = np.array([hist.GetBinError(i) for i in range(0, nbins + 2)])
        obj = cls(edges, full_contents[1:-1], errors[1:-1])
        obj.underflow = full_contents[0]
        obj.overflow = full_contents[-1]
        #obj.underflow_error = errors[0]
        #obj.overflow_error = errors[-1]
        #
        #   calcualte centerrs....
        # cx = 0.5 * (xe[1:] + xe[:-1])
        #    calculate edges....
        #dx = np.diff(cx)[0] # if uniform diff
        #xe = np.concatenate(([cx[0] - dx/2], cx + dx/2))

        obj.name = hist.GetName()
        obj.title = hist.GetTitle()
        obj.nbins = nbins
        #I override previous things
        obj.contents = np.array([hist.GetBinContent(i) for i in range(1, nbins + 1)])  #
        obj.centers = np.array([hist.GetBinCenter(i) for i in range(1, nbins + 1)])  #
        obj.ledges = np.array([hist.GetBinLowEdge(i) for i in range(1, nbins + 1)])  #
        obj.redges = obj.centers + (obj.centers - obj.ledges)
        #
        # h.Fill(i, i)  makes dY == Y !   ------------------ trick ------ against bad/special  filling --- carefully
        # for j in range(i): h.Fill(i) makes dY=sqrt(Y)
        obj.errors = np.array([hist.GetBinError(i) for i in range(1, nbins + 1)] )
        #obj.errors = np.array([hist.GetBinError(i) if (hist.GetBinError(i) != hist.GetBinContent(i)) else math.sqrt(hist.GetBinContent(i)) for i in range(1, nbins + 1)] )
        #
        obj.uderflow = hist.GetBinContent(0)
        obj.overflow = hist.GetBinContent(nbins + 1)
        return obj

# ================================================================================
#   Draw
# --------------------------------------------------------------------------------

    def Draw(self, option="", draw_format="numpy", show=False, save=None):
        """
        Draw using   numpy   or   root
        """
        if draw_format == "root":
            self.local_th1 = self.to_th1()
            self.local_th1.Print()
            if option == "":
                self.local_th1.Draw("HISTOE1")
            else:
                self.local_th1.Draw(option)
        # -----------------------------------------
        elif draw_format == "numpy":
            #rcParams["axes.prop_cycle"]
            #cycler('color',
            index = 0
            index = NumpyTH1.color_index
            print(f"D....  plotting with colors    {self.mycolors[index]}   ")
            #index = 0
            #       )
            #mycol = [0.1216, 0.4667, 0.7059, 1] # default BLUE colors in matplotlib
            #mycola = mycol[:3] + [mycol[-1] * 0.5]
            ## bar is simple  1:1
            ##plt.bar( self.centers, self.contents, color=[0, 0, 0, 0.2])
            ## stairs need edges from nupy
            plt.stairs( self.contents, self.edges,
                        color=self.mycolors[index],
                        alpha=0.5,
                        ec=self.mycolors[index],
                        ls="-",
                        lw=0.75,
                        aa=False,
                        fill=True) # , hatch="//"
            # plt.step where=pre|post
            # not plt.hist ... it creates histo from data
            plt.errorbar( self.centers, self.contents, self.errors,
                          color=self.mycolors[index],
                          alpha=0.5,
                          lw=0.75,
                          fmt=".")
            plt.grid()
            if save is not None and type(save) == str:
                plt.savefig( save )
            self.color_index_inc()
            if show:
                plt.show()

# ================================================================================
#
# --------------------------------------------------------------------------------

    @classmethod
    #def from_numpy_events(cls, events: np.ndarray, bin_edges: np.ndarray):
    def from_numpy_events(cls, events: np.ndarray, bins: int, rangex=None):
        """
        organize many events to a histogram ???? ???? ????
        """
        myrange = rangex
        if myrange is None:
            myrange = (events.min(), events.max())
        #contents, _ = np.histogram(events, bins=bin_edges ) # ,range=xr (0,2)
        contents, bin_edges = np.histogram(events, bins=bins, rangex=myrange ) # ,range=xr (0,2)
        # For errors, use sqrt(contents) as default
        errors = np.sqrt(contents)
        underflow = np.sum(data < bin_edges[0]) # ???
        overflow = np.sum(data >= bin_edges[-1])
        #-----------------------------
        obj = cls(bin_edges, contents, errors)
        obj.underflow = underflow
        obj.overflow = overflow
        obj.underflow_error = np.sqrt(underflow)
        obj.overflow_error = np.sqrt(overflow)
        return obj

# ================================================================================
#
# --------------------------------------------------------------------------------
    def to_th1(self):
        """
        return TH1 histo -  also needed for saving ... seems to work
        """
        nbins = len(self.contents)
        hist = ROOT.TH1D(self.name, self.title, nbins, self.bin_edges[0], self.bin_edges[-1])
        for i in range(nbins):
            hist.SetBinContent(i + 1, self.contents[i])
            hist.SetBinError(i + 1, self.errors[i])
        hist.SetBinContent(0, self.underflow)
        hist.SetBinError(0, self.underflow_error)
        hist.SetBinContent(nbins + 1, self.overflow)
        hist.SetBinError(nbins + 1, self.overflow_error)
        return hist

# ================================================================================
#
# --------------------------------------------------------------------------------
    @classmethod
    def list_file(cls, filename: str):
        """
        show file content
        """
        res = cls.get_names_ffile(filename)
        for i in res:
            print(f"f...   ...   {i}     (TH1 in {filename})")

# ================================================================================
#
# --------------------------------------------------------------------------------
    @classmethod
    def color_index_inc(cls):
        """
        increment color index
        """
        cls.color_index += 1
        if cls.color_index > len(cls.mycolors):
            cls.color_index = 0

# ================================================================================
#
# --------------------------------------------------------------------------------
    @classmethod
    def get_names_ffile(cls, filename: str): # ROOT ONLY
        """
        get list of OBJ TH1
        """
        ok = False
        linames = []
        if not os.path.exists(filename):
            return linames
        try:
            root_file = ROOT.TFile(filename, "READ")
            keys = root_file.GetListOfKeys()
            ok = True
        except:
            print(f"{fg.red}X... file open failed: {fg.default} ", filename)
            pass
        if not ok:
            return linames
        hist = None
        cnt = 0
        for key in keys:
            #print(f" ...  ... ... ... {key} ")
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TH1):
                linames.append(key.GetName())
                cnt += 1
        #print(f"i... there is {cnt} histograms in the file")
        return linames


# ================================================================================
#
# --------------------------------------------------------------------------------
    # ----saving, self.....
    def save(self, filename: str, save_format: str = "root"):
        """
        convert to_th1 and save
        """
        print(f"i...  saving   histo '{self.name}'  into   '{filename}' ")
        save_format = save_format.lower()
        if save_format == "numpy":
            np.savez(filename,
                     bin_edges=self.bin_edges,
                     contents=self.contents,
                     errors=self.errors,
                     underflow=self.underflow,
                     overflow=self.overflow,
                     underflow_error=self.underflow_error,
                     overflow_error=self.overflow_error)
        elif save_format == "root":
            ok = False
            linames = NumpyTH1.get_names_ffile(filename)
            #print(linames)
            if self.name in linames:
                print(f"{fg.red}X...                 '{self.name}'  already exists in {filename}   - NOT saved {fg.default}")
                return
            try:
                root_file = ROOT.TFile(filename, "UPDATE")
                keys = root_file.GetListOfKeys()
                #root_file = ROOT.TFile(filename, "RECREATE")
                hist = self.to_th1()
                hist.Write()
                root_file.Close()
                ok = True
            except:
                pass
            if not ok:
                print(f"{fg.red}X... file open/write failed: {fg.default}", filename)

        else:
            raise ValueError("Unsupported save_format. Use 'numpy' or 'root'.")



# ================================================================================
#
# --------------------------------------------------------------------------------

    # --------------------------------------------------------------------- LOAD
    @classmethod
    def load(cls, filename: str, name=None, load_format: str = "root"):
        """
        create on load
        """
        print(f"i...  loading        '{name}'    from {filename} ")
        load_format = load_format.lower()
        if load_format == "numpy":
            if not os.path.exists(filename):
                print('raise FileNotFoundError(f"{filename} not found")')
            data = np.load(filename)
            obj = cls(data['bin_edges'], data['contents'], data['errors'])
            obj.underflow = data['underflow'].item()
            obj.overflow = data['overflow'].item()
            obj.underflow_error = data['underflow_error'].item()
            obj.overflow_error = data['overflow_error'].item()
            return obj
        elif load_format == "root" and name is not None:
            ok = False
            try:
                root_file = ROOT.TFile(filename, "READ")
                keys = root_file.GetListOfKeys()
                ok = True
            except:
                print(f"{fg.red}X... file open failed: {fg.default}", filename)
                pass
            if not ok:
                return None
            hist = None
            cnt = 0
            for key in keys:
                #print(f" ...  ... {key} ")
                obj = key.ReadObj()
                if isinstance(obj, ROOT.TH1):
                    cnt += 1
            print(f"i... there is {cnt} histograms total in the file")
            for key in keys:
                obj = key.ReadObj()
                if isinstance(obj, ROOT.TH1) and name == obj.GetName():
                    hist = obj
                    break  # means loads the 1st???
            if hist is None:
                root_file.Close()
                print('raise ValueError("No TH1 histogram found in ROOT file  - with the desired name")')
                return None
            obj = cls.from_th1(hist)
            root_file.Close()
            return obj
        else:
            raise ValueError("Unsupported load_format. Use 'numpy' or 'root'.")

# ================================================================================
#
# --------------------------------------------------------------------------------
    # ------------------------- deleting -------------------------------------
    def force_del(self):
        #try:
        print(f"{fg.darkslateblue}D...  deleting histo '{self.name}'  #instances  {len(NumpyTH1.instances):2d} =>", end="")
        NumpyTH1.instances.remove(self)
        print(f"  {len(NumpyTH1.instances):2d}  {fg.default}", end="\n")
        del self
        gc.collect()
        #except ValueError:
        #    print(f"{fg.red}X... something went wrong when removing the histo from instances{fg.default}")
        #    pass

# ================================================================================
#
# --------------------------------------------------------------------------------
    def __del__(self):
        """
        not sure if useful
        """
        try:
            NumpyTH1.instances.remove(self)
        except ValueError:
            pass

# ================================================================================
#
# --------------------------------------------------------------------------------
    # ---------------------  special operations
    @staticmethod
    def wait_loop():
        while True:
            maxc = ROOT.gROOT.GetListOfCanvases().GetEntries()
            vis = 0
            for i in range(maxc):
                ci = ROOT.gROOT.GetListOfCanvases().At(i)
                if ci.GetCanvasImp(): vis += 1
                ci.Modified()
                ci.Update()
            if vis <= 0:   break
            time.sleep(1)


# ================================================================================
#
# --------------------------------------------------------------------------------
# ================================================================================
#
# --------------------------------------------------------------------------------

# **************************************************************************************************************************
if __name__ == "__main__":
    # ================================================================================
    #   TESTING CODE HERE
    #                        uv run src/jusflpyroot/numth1.py
    # --------------------------------------------------------------------------------

    NumpyTH1.reset_all()
    NumpyTH1.list()
    print("i... listing file:")
    NumpyTH1.list_file("/tmp/my_temp_histograms.root") #  list the file content if exists
    #   create one ROOT  histogram
    h = ROOT.TH1F("namea", "histogram that goes to file", 100, 0, 100)

    print("i... filling-in with a binary pattern to distinguish under/ovrflow and the content")
    h.Fill(- 1 )            # underflow
    h.Fill(0, 2)            # 2x inside
    h.Fill(100 - 0.0001, 4) # 4x inside
    h.Fill(100 , 8)         # 8x overflow

    #   create THE OBJECT
    nh = NumpyTH1.from_th1(h)
    nh.save("/tmp/my_temp_histograms.root", save_format="root")
    #nh.force_del()  # brutally remove the object from instances

    # once more, but empty, I dont care about 'h'
    h = ROOT.TH1F("nameb", "histogram that also goes to file", 100, 0, 100)
    nh = NumpyTH1.from_th1(h)
    nh.save("/tmp/my_temp_histograms.root", save_format="root")
    #nh.force_del()

    print("i... LIST")
    NumpyTH1.list()
    print("X...  DELETEING")
    NumpyTH1.reset_all()
    print("X...  DELETED")
    print("i... LIST EMPTY START")
    NumpyTH1.list()
    print("i... LIST EMPTY END")

    # last time, but dont delete this time
    h = ROOT.TH1F("namec", "histogram just here", 10, 0, 10)
    for i in range(10): # for range(11) .... 10 will already go to overflows
        h.Fill(i, i)
    for i in range(10): # make some mess
        h.Fill(2)
        h.Fill(3)
        h.Fill(4)
        h.Fill(5)
    nh = NumpyTH1.from_th1(h)
    nh2 = NumpyTH1.load("/tmp/my_temp_histograms.root", "namea", load_format="root")

    # --
    nh2.Draw()
    xnh = NumpyTH1.by_name("namec")
    if xnh is not None:
        xnh.Draw("numpy", show=True, save="a.jpg")


    print(" ... _______ I expect to see 'namec' (still in memory)   and 'namea' from disk")
    NumpyTH1.list()
    print(" ... _______ on disk:")
    NumpyTH1.list_file("/tmp/my_temp_histograms.root")

    if False:
        print("... ========================= fitting ==========================")
        x, y, dy = nh.get_xy()  # Get data for fit (from histogram)
        print(x)
        print(y)
        print(dy)

        A = PrepareLSQFit(x, y, dy ) # provide data to FITTER
        A.set_model("p2")            # select mode name and function
        A.FIT( a= -0.1, b=1, c=1)    # initial values + constant names; paramater names must match
        A.conclude()


#    NumpyTH1.wait_loop()

#     ROOT.gInterpreter.Declare('''
# void exec3event(Int_t event, Int_t x, Int_t y, TObject *selected){TCanvas *c = (TCanvas *)gTQSender;
#     cout<<event<<x<<y<< selected->IsA()->GetName()<<endl;;}
# ''')
#     #exec3event = ROOT.exec3event
# #    ROOT.gInterpreter.Declare('''
# #void exec3event(Int_t event, Int_t x, Int_t y, TObject *selected){TCanvas *c = (TCanvas *)gTQSender;
# #    printf("Canvas %s: event=%d, x=%d, y=%d, selected=%s\n", c->GetName(), event, x, y, selected->IsA()->GetName());}
# #''')
#     #exec3event = ROOT.exec3event( event: ctypes.c_int, x: ctypes.c_int, y: ctypes.c_int, selected: ROOT.TObject)
#     #def exec3event(event, x, y, selected):
#     #    c = ROOT.gTQSender
#     #    print(f"Canvas {c.GetName()}: event={event}, x={x}, y={y}, selected={selected.IsA().GetName()}")


#     ROOT.gROOT.GetListOfGlobalFunctions().Delete()
#     h = ROOT.TH1F("h", "h", 100, -3, 3)
#     h.FillRandom("gaus", 1000)
#     c1 = ROOT.TCanvas("c1")
#     h.Draw()
#     c1.Update()
#     #    c1.Connect("ProcessedEvent(Int_t,Int_t,Int_t,TObject*)", 0, 0, "exec3event(Int_t,Int_t,Int_t,TObject*)")

#     # Connect using the static method with sender, signal, receiver class, receiver, slot
#     #ROOT.TQObject.Connect(c1, "ProcessedEvent(Int_t,Int_t,Int_t,TObject*)", "", ROOT.nullptr,  ROOT.exec3event() )
#     c1.Connect(c1, "ProcessedEvent(Int_t,Int_t,Int_t,TObject*)", "", ROOT.nullptr,  ROOT.exec3event() )
#     ####ROOT.TQObject.Connect(c1, "", "", None, *exec3event  )
#     NumpyTH1.wait_loop()
