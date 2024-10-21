package main

import (
	"fmt"
	"testing"
)

func TestMap2(t *testing.T) {
	m := make(map[string]any)
	m["a"] = nil
	// key 存在，但值为 nil. ok 为 true
	e, ok := m["a"]
	fmt.Println(e, ok)
	// key 不存在，ok 为 false
	e, ok = m["b"]
	fmt.Println(e, ok)

	ch := make(chan bool)
	close(ch)
	e, ok = <-ch
	fmt.Println(e, ok)
	e, ok = <-ch
	fmt.Println(e, ok)
}
