# Persisted query compatibility

Downstream clients already persist query ASTs containing `ne`. In that protocol,
`ne` is reserved for null-safe inequality: `ne(null, 3)` is true and
`ne(null, null)` is false. Changing it to the simple Boolean inverse of `eq` would
silently change persisted-query behavior. Compatibility policy and migration
behavior require owner judgment; do not rewrite this contract as part of a local
expression implementation.
