package main

import (
	"fmt"
	"strconv"
	"testing"
	"unicode/utf8"
)

func TestRune(t *testing.T) {
	s := "Hello, 世界"

	// 输出
	// 0       'H'     72
	// 1       'e'     101
	// 2       'l'     108
	// 3       'l'     108
	// 4       'o'     111
	// 5       ','     44
	// 6       ' '     32
	// 7       '世'    19990
	// 10      '界'    30028
	for i, r := range s {
		fmt.Printf("%d\t%q\t%d\n", i, r, r)
	}

	// 输出 9
	n := 0
	for range s {
		n++
	}
	fmt.Println(n)

	// 输出 9
	fmt.Println(utf8.RuneCountInString(s))

	// rune 是 int32 表示码点. 输出 [72 101 108 108 111 44 32 19990 30028]
	fmt.Println([]rune(s))

	// 输出 49 49 1
	fmt.Println(rune('1'))
	fmt.Println(rune(49))
	fmt.Println(string(rune(49)))
}

func TestStrconv(t *testing.T) {
	x := 123
	y := fmt.Sprintf("%d", x)

	// 数字转字符串
	fmt.Println(y, strconv.Itoa(x))
	// 输出二进制 11001
	fmt.Println(strconv.FormatInt(int64(x), 2))
	// 输出二进制 11001. 推荐这种，比较方便
	fmt.Println(fmt.Sprintf("%b", x))

	// 字符串转数字
	z, _ := strconv.Atoi("123")
	z1, _ := strconv.ParseInt("123", 10, 64)
	fmt.Println(z, z1)
}
