// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME MyCanvasDict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Header files passed as explicit arguments
#include "MyCanvas.h"

// Header files passed via #pragma extra_include

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

namespace ROOT {
   static void delete_MyCanvas(void *p);
   static void deleteArray_MyCanvas(void *p);
   static void destruct_MyCanvas(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::MyCanvas*)
   {
      ::MyCanvas *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::MyCanvas >(nullptr);
      static ::ROOT::TGenericClassInfo 
         instance("MyCanvas", ::MyCanvas::Class_Version(), "MyCanvas.h", 8,
                  typeid(::MyCanvas), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::MyCanvas::Dictionary, isa_proxy, 4,
                  sizeof(::MyCanvas) );
      instance.SetDelete(&delete_MyCanvas);
      instance.SetDeleteArray(&deleteArray_MyCanvas);
      instance.SetDestructor(&destruct_MyCanvas);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::MyCanvas*)
   {
      return GenerateInitInstanceLocal(static_cast<::MyCanvas*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::MyCanvas*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr MyCanvas::fgIsA(nullptr);  // static to hold class pointer

//______________________________________________________________________________
const char *MyCanvas::Class_Name()
{
   return "MyCanvas";
}

//______________________________________________________________________________
const char *MyCanvas::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MyCanvas*)nullptr)->GetImplFileName();
}

//______________________________________________________________________________
int MyCanvas::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MyCanvas*)nullptr)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *MyCanvas::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MyCanvas*)nullptr)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *MyCanvas::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MyCanvas*)nullptr)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void MyCanvas::Streamer(TBuffer &R__b)
{
   // Stream an object of class MyCanvas.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(MyCanvas::Class(),this);
   } else {
      R__b.WriteClassBuffer(MyCanvas::Class(),this);
   }
}

namespace ROOT {
   // Wrapper around operator delete
   static void delete_MyCanvas(void *p) {
      delete (static_cast<::MyCanvas*>(p));
   }
   static void deleteArray_MyCanvas(void *p) {
      delete [] (static_cast<::MyCanvas*>(p));
   }
   static void destruct_MyCanvas(void *p) {
      typedef ::MyCanvas current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::MyCanvas

namespace {
  void TriggerDictionaryInitialization_MyCanvasDict_Impl() {
    static const char* headers[] = {
"MyCanvas.h",
nullptr
    };
    static const char* includePaths[] = {
"/home/ojr/root/include/",
"/tmp/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "MyCanvasDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
class __attribute__((annotate("$clingAutoload$MyCanvas.h")))  MyCanvas;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "MyCanvasDict dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "MyCanvas.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"MyCanvas", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("MyCanvasDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_MyCanvasDict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_MyCanvasDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_MyCanvasDict() {
  TriggerDictionaryInitialization_MyCanvasDict_Impl();
}
