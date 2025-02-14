package main

import (
	"fmt"
	"os"
	"runtime/trace"
)

func main() {
	// 创建trace文件
	f, err := os.Create("trace.out")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	// 启动trace goroutine
	err = trace.Start(f)
	if err != nil {
		panic(err)
	}
	defer trace.Stop()

	// main
	fmt.Println("Hello World!")

	go func() {
		fmt.Println("Hello World!2")
	}()

	fmt.Println("Hello World!3")
}
