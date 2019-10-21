package reader

import (
	"bufio"
	"fmt"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// Read is to read a file
func Read(inputTxt string) {
	file, err := os.Open(inputTxt)
	check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	i := 0
	for scanner.Scan() {
		fmt.Println(scanner.Text())
		i++
		if i > 10 {
			break
		}
	}
}

// an example of read file
func ReadExample() {
	inputTxt := "./dbsnp/1.txt"
	fmt.Printf("hello!\n")
	Read(inputTxt)
}
