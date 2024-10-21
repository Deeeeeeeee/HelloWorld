package main

import (
	"fmt"
	"testing"
)

func TestFallthrough(t *testing.T) {
	// fallthrough 只会往下一次。即输出 two three
	num := 2
	switch num {
	case 1:
		t.Log("one")
	case 2:
		t.Log("two")
		fallthrough
	case 3:
		t.Log("three")
	case 4:
		t.Log("four")
	default:
		t.Log("other")
	}
}

func TestInnerFunc(t *testing.T) {
	// cap 容量
	t.Log(cap([]int{1, 2, 3}))

	// copy 拷贝. 输出 [1 2 3] [1 2 3 0]
	a := []int{1, 2, 3}
	b := make([]int, 4)
	copy(b, a)
	t.Log(a, b)

	// complex 构造复数，real 获取实部，imag获取虚部. 输出 3 4
	num := complex(3.0, 4.0)
	realValue := real(num)
	imagValue := imag(num)
	fmt.Printf("The real part is: %v\n", realValue)
	fmt.Printf("The imaginary part is: %v\n", imagValue)
}

func TestRecover(t *testing.T) {
	// recover 捕获异常
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("recovered from ", err)
		}
	}()
	panic("panic")

	// 这一句不会执行
	fmt.Println("after panic")
}

func TestDeclear1(t *testing.T) {
	// 多个变量声明
	var a, b int = 1, 2
	// 变量交换
	a, b = b, a
	t.Log(a, b)
}
