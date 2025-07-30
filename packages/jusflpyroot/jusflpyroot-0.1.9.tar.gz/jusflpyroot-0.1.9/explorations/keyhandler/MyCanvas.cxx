#include <TObject.h>  // or other ROOT base classes

#include "MyCanvas.h"

#include <iostream>
#include <TApplication.h>


ClassImp(MyCanvas)

MyCanvas::MyCanvas(const char* name, UInt_t ww, UInt_t wh)
    : TRootCanvas(nullptr, name, ww, wh)
{}

MyCanvas::~MyCanvas() {}

Bool_t MyCanvas::HandleKey(Event_t *event) {
    if (event->fCode == 'q' || event->fCode == 'Q') {
        std::cout << "Pressed 'q', terminating application." << std::endl;
        gApplication->Terminate();
        return kTRUE;
    }
    return TRootCanvas::HandleKey(event);
}
