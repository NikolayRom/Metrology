package main

import "fmt"

func analyzeComplexFlow(data[]int) {
	for i := 0; i < len(data); i++ {
		val := data[i]
		
		if val > 0 {
			switch val {
			case 1:
				fmt.Println("One")
			case 2: 
				fmt.Println("Two")
			case 3: 
				fmt.Println("Three")
			default:
				fmt.Println("Other positive")
			}
		} else if val < 0 { 
			fmt.Println("Negative")
		} else { 
			fmt.Println("Zero")
		}
	}

	for index, value := range data {
		if value == 100 { 
			fmt.Printf("100 found at %d\n", index)
			break
		}
	}

	count := 0
	for count < 3 {
		count++
	}

	for {
		if count == 5 {
			break
		}
		count++
	}
}

func main() {
	testData :=[]int{1, -5, 2, 0, 100, 3}
	analyzeComplexFlow(testData)
}