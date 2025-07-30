 void testMyCanvas() {
 //   TApplication app("app", nullptr, nullptr);
   MyCanvas* c = new MyCanvas("MyCanvas", 800, 600);
   c->Draw();
 //   app.Run();
 }



// #include <TApplication.h>

// void testMyCanvas() {
//     if (!gApplication) {
//         int argc = 0;
//         char* argv[] = {};
//         new TApplication("app", &argc, argv);
//     }

//     MyCanvas* c = new MyCanvas("MyCanvas", 800, 600);
//     c->Draw();

//     if (gApplication) gApplication->Run();
// }
