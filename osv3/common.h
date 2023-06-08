
/////////////////////////////////////// instructions

#define lbl(name) Lbl name
#define jmp(label) Goto label

#define put(text) Disp text

/////////////////////////////////////// programs

#define push(var) prgmPUSH ## var
#define pop(var) prgmPOP ## var

///////////////////////////////////////
