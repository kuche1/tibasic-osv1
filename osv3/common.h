
/////////////////////////////////////// preprocessor hacks

#define EXPAND(...) __VA_ARGS__
#define CONCAT(a, b) a ## b

/////////////////////////////////////// control flow

#define lbl(name) Lbl name

#define jmp(label) Goto label

/////////////////////////////////////// IO

#define put(text) Disp text

/////////////////////////////////////// string
///// string are 0-indexed

#define str_len(str) length(str)

#define str_tail(str, first_tail_item_idx) sub(str,first_tail_item_idx+1,str_len(str)-first_tail_item_idx)

#define str_head(str, last_head_item_idx) sub(str,1,last_head_item_idx+1)

#define str_cut_idx(str, start_idx, end_idx) sub(str,start_idx+1,end_idx-start_idx+1)

/////////////////////////////////////// stack

#define push(var) CONCAT(prgmPUSH, var)

#define pop(var) CONCAT(prgmPOP,  var)

///////////////////////////////////////
