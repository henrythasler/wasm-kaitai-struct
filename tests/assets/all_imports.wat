(module
  ;; Import a function with no parameters and no return value
  (import "env" "log" (func $log))
  
  ;; Import a function with parameters and return value
  (import "env" "add" (func $add (param i32 i32) (result i32)))
  
  ;; Import a function with multiple return values (multi-value proposal, but part of Wasm 1.0)
  (import "env" "divide" (func $divide (param i32 i32) (result i32 i32)))
  
  ;; Import a table (for indirect function calls)
  (import "env" "table" (table 10 funcref))
  
  ;; Import memory
  (import "env" "memory" (memory 1))
  
  ;; Import an immutable global
  (import "env" "globalConst" (global $globalConst i32))
  
  ;; Import a mutable global
  (import "env" "globalMut" (global $globalMut (mut i32)))
  
  ;; Export a function that uses all the imports
  (func (export "useImports") (result i32)
    ;; Call the log function
    call $log
    
    ;; Call the add function
    i32.const 5
    i32.const 10
    call $add
    
    ;; Store result in memory at offset 0
    i32.const 0
    ;; local.get 0
    i32.store
    
    ;; Get the immutable global
    global.get $globalConst
    
    ;; Add it to the mutable global
    global.get $globalMut
    i32.add
    
    ;; Set the mutable global
    global.set $globalMut
    
    ;; Call divide function (returns quotient and remainder)
    i32.const 17
    i32.const 5
    call $divide
    
    ;; Add quotient and remainder together
    i32.add
    
    ;; Return the final result
  )
  
  ;; Function that uses the table for indirect calls
  (func (export "callIndirect") (param i32) (result i32)
    ;; Call function at table index 0 with parameter
    local.get 0
    i32.const 0
    call_indirect (param i32) (result i32)
  )
  
  ;; Function that reads from memory
  (func (export "readMemory") (result i32)
    i32.const 0
    i32.load
  )
  
  ;; Function that writes to memory
  (func (export "writeMemory") (param i32)
    i32.const 0
    local.get 0
    i32.store
  )
)