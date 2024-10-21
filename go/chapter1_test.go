package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"testing"
)

func TestHelloworld1(t *testing.T) {
	fmt.Println("Hello World")
}

func TestFor1(t *testing.T) {
	// for循环经典形式
	for i := 0; i < 10; i++ {
		fmt.Println(i)
	}

	// for range，第一个参数是 index
	for idx, i := range []int{1, 2, 3} {
		fmt.Println(idx, i)
	}
}

func TestDeclear(t *testing.T) {
	// 几种声明方式都是等价的
	s := ""
	var ss string
	var sss = ""
	var ssss string = ""

	fmt.Println(s, ss, sss, ssss)
}

func TestJoin(t *testing.T) {
	// 字符串拼接
	fmt.Println(strings.Join([]string{"a", "b", "c"}, " "))
}

func TestSplit(t *testing.T) {
	// 字符串 split
	fmt.Println(strings.Split("a,b,c", ","))
}

func TestMap(t *testing.T) {
	// map有默认值。int为0
	m := make(map[string]int)
	m["a"]++
	fmt.Println(m)
}

func TestHttp(t *testing.T) {
	resp, err := http.Get("http://www.baidu.com")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	b, err := io.ReadAll(resp.Body)
	resp.Body.Close()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	fmt.Printf("%s\n", b)
}
