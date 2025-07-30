

# rootcling -f MyCanvasDict.cxx -c MyCanvas.h LinkDef.h
# g++ -fPIC -shared -o libMyCanvas.so MyCanvas.cxx MyCanvasDict.cxx $(root-config --cflags --libs)


import ROOT

# Load your custom canvas library
ROOT.gSystem.Load("./libMyCanvas.so")


app = ROOT.TApplication("app", 0, 0)

# Create a histogram
#histo = ROOT.TH1F("h", "h", 100, 0, 100)
#histo.FillRandom("gaus", 1000)

# Create an instance of your custom canvas
c = ROOT.MyCanvas("c1",  800, 600)
c.Draw()
#histo.Draw()
#c.Update()

# Run the ROOT application event loop
#app = ROOT.gApplication
app.Run()
