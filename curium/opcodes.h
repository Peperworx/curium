#pragma once
#include <stdint.h>



#ifdef __cplusplus
extern "C" {
#endif


struct operation {
    uint8_t type        : 1;
    uint8_t subtype     : 7;
    uint8_t opcode      : 8;
    uint64_t padding0   : 64;
    uint64_t padding1   : 64;
    uint64_t padding2   : 64;
    uint16_t padding3   : 16;

} __attribute__((packed));

struct operation_stack {
    uint8_t type        : 1;
    uint8_t subtype     : 7;
    uint8_t opcode      : 8;
    uint64_t argument   : 64;
    uint64_t padding    : 64;
    uint64_t padding2   : 64;
    uint16_t padding3   : 16;
} __attribute__((packed));

struct operation_other {
    uint8_t type        : 1;
    uint8_t subtype     : 7;
    uint8_t opcode      : 8;
    uint8_t types       : 8;
    uint8_t sizes       : 8;
    uint64_t argument1  : 64;
    uint64_t argument2  : 64;
    uint64_t argument3  : 64;
} __attribute__((packed));




#ifdef __cplusplus
}
#endif