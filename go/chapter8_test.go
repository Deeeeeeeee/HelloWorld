package main

import (
	"fmt"
	"testing"
)

func TestChan(t *testing.T) {
	// 创建 chan
	ch := make(chan int)
	// 发送 send
	ch <- 1
	// 接收 receive
	<-ch
	// 关闭 close
	close(ch)

	ch1 := make(chan struct{})   // 无缓冲通道
	ch1 = make(chan struct{}, 0) // 无缓冲通道
	ch1 = make(chan struct{}, 3) // 容量为3的缓冲通道
	close(ch1)
}

func TestPipeline(t *testing.T) {
	naturals := make(chan int)
	squares := make(chan int)

	// counter
	go func() {
		for x := 0; x < 100; x++ {
			naturals <- x
		}
		close(naturals)
	}()

	// squarer
	go func() {
		for x := range naturals {
			squares <- x * x
		}
		close(squares)
	}()

	// printer(在主 goroutine 中)
	for x := range squares {
		fmt.Println(x)
	}
}
