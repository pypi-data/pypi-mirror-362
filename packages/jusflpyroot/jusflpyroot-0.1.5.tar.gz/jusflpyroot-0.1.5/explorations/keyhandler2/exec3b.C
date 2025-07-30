#include <TApplication.h>  // Add this line

#include <TH1.h>
#include <TCanvas.h>
#include <TQObject.h>
#include "TROOT.h"
#include <iostream>

void exec3event(Int_t event, Int_t x, Int_t y, TObject *selected)
{
    TCanvas *c = (TCanvas *) gTQSender;
    if (!c) return;

    printf("Canvas %s: event=%d, x=%d, y=%d\n", c->GetName(), event, x, y);

    if (event == 24) { // key press event
        if (x == 'q' || x == 'Q') {
            std::cout << "Pressed 'q', exiting ROOT..." << std::endl;
            gApplication->Terminate(0);
        }
    }
}

void exec3b()
{
    gROOT->GetListOfGlobalFunctions()->Delete();

    TH1F *h = new TH1F("h", "h", 100, -3, 3);
    h->FillRandom("gaus", 1000);

    TCanvas *c1 = new TCanvas("c1");
    h->Draw();
    c1->Update();

    c1->Connect("ProcessedEvent(Int_t,Int_t,Int_t,TObject*)", 0, 0, "exec3event(Int_t,Int_t,Int_t,TObject*)");
}
