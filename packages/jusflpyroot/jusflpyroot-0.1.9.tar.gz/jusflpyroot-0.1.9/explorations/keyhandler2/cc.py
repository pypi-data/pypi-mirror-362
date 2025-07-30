
import ROOT

# Disable implicit multi-threading
ROOT.EnableImplicitMT(0)

# Load and run the C++ macro
ROOT.gROOT.ProcessLine(".L exec3b.C+")
ROOT.exec3b()

# Retrieve canvas and histogram if needed, keep references
canvas = ROOT.gROOT.FindObject("c1")
hist = ROOT.gROOT.FindObject("h")

# Start ROOT event loop (keeps the GUI alive)
ROOT.gApplication.Run()
