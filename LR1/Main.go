package main

import (
	"fmt"
	"math"
)

func calculateStats(numbers[]float64) (float64, float64) {
	if len(numbers) == 0 {
		return 0.0, 0.0
	}
	sum := 0.0
	for i := 0; i < len(numbers); i++ {
		sum += numbers[i]
	}
	avg := sum / float64(len(numbers))
	return sum, avg
}

func findMax(numbers[]float64) float64 {
	if len(numbers) == 0 {
		return 0.0
	}
	maxVal := numbers[0]
	for _, val := range numbers {
		if val > maxVal {
			maxVal = val
		}
	}
	return maxVal
}

func factorial(n int) int {
	if n <= 1 {
		return 1
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result
}

func processMatrix(rows, cols int) {
	matrix := make([][]int, rows)
	for i := range matrix {
		matrix[i] = make([]int, cols)
		for j := range matrix[i] {
			matrix[i][j] = i + j
		}
	}

	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			fmt.Printf("%d ", matrix[i][j])
		}
		fmt.Println()
	}
}

func main() {
	fmt.Println("--- Metrology Lab Analysis Program ---")

	data :=[]float64{12.5, 45.2, 8.9, 99.1, 3.4}
	fmt.Println("Input data:", data)

	totalSum, average := calculateStats(data)
	fmt.Printf("Total Sum: %.2f\n", totalSum)
	fmt.Printf("Average: %.2f\n", average)

	maxItem := findMax(data)
	fmt.Printf("Maximum value: %.2f\n", maxItem)

	limit := 5
	for k := 1; k <= limit; k++ {
		fact := factorial(k)
		power := math.Pow(float64(k), 2)
		fmt.Printf("Number: %d, Factorial: %d, Square: %.2f\n", k, fact, power)
	}

	flagA := true
	flagB := false
	if flagA && !flagB {
		fmt.Println("Logical AND passed")
	} else {
		fmt.Println("Logical condition failed")
	}

	choice := 2
	switch choice {
	case 1:
		fmt.Println("Choice is 1")
	case 2:
		processMatrix(3, 3)
	default:
		fmt.Println("Unknown choice")
	}
}