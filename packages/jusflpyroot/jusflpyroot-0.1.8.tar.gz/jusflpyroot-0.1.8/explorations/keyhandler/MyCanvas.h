

#ifndef MYCANVAS_H
#define MYCANVAS_H

#include <TRootCanvas.h>

class MyCanvas : public TRootCanvas {

public:
    MyCanvas(const char* name, UInt_t ww, UInt_t wh);
    virtual ~MyCanvas();

    virtual Bool_t HandleKey(Event_t *event) override;
   ClassDef(MyCanvas, 1);

};

#endif  // MYCANVAS_H
