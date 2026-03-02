package main

import (
	"fmt"
	"math/rand"
	"time"
)

type Number interface {
	~int | ~float64
}

func calculateSum[T Number](values ...T) T {
	var total T
	for _, val := range values {
		total += val
	}
	return total
}

func demonstrateBitwiseOps(a, b int) {
	a &= b
	a |= 2
	a ^= 1
	a <<= 1
	a >>= 1
	a &^= 3

	_ = a & b
	_ = a | b
	_ = a ^ b
	_ = a << 1
	_ = a >> 1
	_ = a &^ b
}

func demonstrateMathOps(x, y float64) {
	x -= y
	x *= y
	x /= y

	z, w := 15, 4
	z %= w
	
	z++
	z--
	
	_ = z + w
	_ = z - w
	_ = z * w
	_ = z / w
	_ = z % w
}

func demonstrateLogic(c, d int) {
	flagA, flagB := true, false
	_ = flagA && flagB
	_ = flagA || flagB
	_ = !flagA
	
	if c == d || c != d {
		_ = c < d
		_ = c > d
		_ = c <= d
		_ = c >= d
	} else if c == 0 {
		_ = c
	} else {
		_ = d
	}
}

func demonstrateChannelsAndMaps() {
	messages := make(chan string, 2)
	messages <- "Hello" 
	
	msg1 := <-messages  
	fmt.Println(msg1)

	userAges := map[string]int{"Alice": 25, "Bob": 30}
	numbers := [...]int{10, 20, 30, 40, 50}
	slice := numbers[1:4]
	
	for name, age := range userAges {
		fmt.Printf("%s is %d\n", name, age)
	}
	fmt.Println("Slice:", slice)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	fmt.Println("--- Go Advanced Operators Analysis ---")
	
	data :=[]float64{1.5, 2.5, 3.5, 4.5}
	total := calculateSum(data...)
	fmt.Printf("Total sum: %.2f\n", total)
	
	demonstrateBitwiseOps(12, 5)
	demonstrateMathOps(10.5, 2.0)
	demonstrateLogic(rand.Intn(10), 5)
	demonstrateChannelsAndMaps()
	
	switch rand.Intn(2) {
	case 0:
		fmt.Println("Zero case")
	default:
		fmt.Println("Default case")
	}
}