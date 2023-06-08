
/////////////////////////////////////// preprocessor hacks

// #define EXPAND(...) __VA_ARGS__
#define CONCAT(a, b) a ## b

/////////////////////////////////////// instructions

#define lbl(name) Lbl name
#define jmp(label) Goto label

#define put(text) Disp text

/////////////////////////////////////// programs

#define push(var) CONCAT(prgmPUSH, var)
#define pop(var)  CONCAT(prgmPOP,  var)

///////////////////////////////////////
