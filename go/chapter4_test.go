package main

import (
	"fmt"
	"testing"
)

func TestArr(t *testing.T) {
	var a [3]int             // 3个整数的数组
	fmt.Println(a[0])        // 输出数组的第一个元素
	fmt.Println(a[len(a)-1]) // 输出数组的最后一个元素

	// for 循环遍历
	for i, v := range a {
		fmt.Printf("%d %d\n", i, v)
	}

	// 数组长度固定
	var q [3]int = [3]int{1, 2}
	fmt.Println(q[2])

	// 长度相同的数组可以比较，否则编译不通过
	p := [...]int{1, 2, 0}
	fmt.Println(q == p)

	// 函数参数是值传递
}

func TestSlice(t *testing.T) {
	months := [...]string{
		1:  "January",
		2:  "February",
		3:  "March",
		4:  "April",
		5:  "May",
		6:  "June",
		7:  "July",
		8:  "August",
		9:  "September",
		10: "October",
		11: "November",
		12: "December",
	}

	Q2 := months[4:7]
	summer := months[6:9]
	fmt.Println(Q2)
	fmt.Println(summer)

	// 可以获取到后面的，即使len(summer) == 3
	fmt.Println(summer[:5])

	// 声明 slice 跟数组的区别，不指定长度
	s := []int{0, 1, 2, 3, 4, 5}
	fmt.Println(s)
	// 用 make 创建指定元素类型、长度和容量的 slice。容量参数可以忽略
	ss := make([]int, 3)
	fmt.Println(ss)

	// slice 不能用 == 比较. 但可以与 nil 比较
	// fmt.Println(s == []int{0, 1, 2, 3, 4, 5})
	fmt.Println(s == nil)
}

func TestAppend(t *testing.T) {
	// 输出
	// len=1 cap=1 [0]
	// len=2 cap=2 [0 1]
	// len=3 cap=4 [0 1 2]
	// len=4 cap=4 [0 1 2 3]
	// len=5 cap=8 [0 1 2 3 4]
	// len=6 cap=8 [0 1 2 3 4 5]
	// len=7 cap=8 [0 1 2 3 4 5 6]
	// len=8 cap=8 [0 1 2 3 4 5 6 7]
	// len=9 cap=16 [0 1 2 3 4 5 6 7 8]
	// len=10 cap=16 [0 1 2 3 4 5 6 7 8 9]
	var x, y []int
	for i := 0; i < 10; i++ {
		y = append(x, i)
		fmt.Printf("len=%d cap=%d %v\n", len(y), cap(y), y)
		x = y
	}
}

func TestSliceAppend(t *testing.T) {
	// 长度和容量都是5的切片
	slice := []int{10, 20, 30, 40, 50}

	// 创建新的切片，长度2，容量4。因为跟上面切片共用底层数组
	newSlice := slice[1:3]

	// append 新元素
	newSlice1 := append(newSlice, 60)

	// 输出
	// [10 20 30 60 50]
	// [20 30]
	// [20 30 60]
	fmt.Printf("%v\n%v\n%v\n", slice, newSlice, newSlice1)

	// 当超过容量，会重新申请一个更大的切片. 底层数据不再共用
	// [10 20 100 60 50]
	// [20 100]
	// [20 30 60 70 80]
	newSlice1 = append(newSlice1, 70, 80)
	newSlice[1] = 100
	fmt.Printf("%v\n%v\n%v\n", slice, newSlice, newSlice1)
}

func TestStack(t *testing.T) {
	stack := make([]int, 0)
	// push 进栈
	stack = append(stack, 1)
	// 栈顶
	top := stack[len(stack)-1]
	// 缩减栈
	stack = stack[:len(stack)-1]
	// 输出 top=1 len=0 cap=1 []
	fmt.Printf("top=%d len=%d cap=%d %v\n", top, len(stack), cap(stack), stack)
}

func TestMap1(t *testing.T) {
	// 创建 map
	m := make(map[string]int)
	m["Answer"] = 42
	fmt.Println("The value:", m["Answer"])

	// 初始化值
	m = map[string]int{"Answer": 42}
	fmt.Println("The value:", m["Answer"])

	// 遍历
	for k, v := range m {
		fmt.Printf("key:%s val:%d\n", k, v)
	}

	// 删除元素
	delete(m, "Answer")
	fmt.Println("The value:", m["Answer"])

	// 值不存在，返回 0
	v, ok := m["Answer"]
	fmt.Println("The value:", v, "Present?", ok)
}
