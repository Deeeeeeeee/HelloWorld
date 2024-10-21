package main

import (
	"fmt"
	"testing"
	"time"
)

func TestMemorySync(t *testing.T) {
	// 输出以下都是正常的
	// y:0 x:1
	// x:0 y:1
	// x:1 y:1
	// y:1 x:1
	// 但是还可能输出 x:0 y:0 或者 y:0 x:0
	// 1. 因为复制和 Print 对应不同的变量，所以编译器可能
	//    认为执行顺序不会影响结果，然后就交换了这两个语句
	// 2. 两个 goroutine 在不同的 CPU 上执行，每个 CPU 都
	//    有自己的缓存，那么一个 goroutine 的写入操作在同步
	//    到内存之前对另外一个 goroutine 的 Print 不可见
	var x, y int
	go func() {
		x = 1
		fmt.Print("y:", y, " ")
	}()
	go func() {
		y = 1
		fmt.Print("x:", x, " ")
	}()
	time.Sleep(1 * time.Second)
}
